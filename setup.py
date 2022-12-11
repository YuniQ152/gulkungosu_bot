import os, requests, json, sqlite3, time
from dotenv import load_dotenv

load_dotenv()

def get_crop_info(crop_id):
    url = "https://farm.jjo.kr/api/static/crop/" + str(crop_id)
    response = requests.get(url, headers={"Authorization": os.getenv("BHMO_API_TOKEN")})
    content = json.loads(response.content)
    id_ = content['data']['id']
    icon = content['data']['icon']
    level = content['data']['level']
    strawberry = content["data"]['strawberry']
    is_tree = 1 if content["data"]["isTree"] == True else 0
    growth = content["data"]['characteristics']['growth']
    water = content["data"]['characteristics']['water']
    soil = content["data"]['characteristics']['soil']
    health = content["data"]['characteristics']['health']
    name_ko = content["names"]["ko"]
    name_en = content["names"]["en"]
    description_ko = content["descriptions"]["ko"]
    description_en = content["descriptions"]["en"]
    return id_, icon, level, strawberry, is_tree, growth, water, soil, health, name_ko, name_en, description_ko, description_en

while(True):
    try:
        print("달달소의 성력을 입력하세요: ", end="")
        libra = int(input())
    except:
        print("자연수만 입력해 주세요.\n")
    else:
        if libra < 1 or libra > 30:
            print("올바른 성력을 입력해 주세요.\n")
        elif libra <= 2:
            delay = 2
            print("OK!")
            print("경고: 2 이하의 성력에서는 ｢보유 가능한 최대 가스｣의 제한으로 인해 명령어가 작동하지 않습니다.\n")
            break
        elif libra <= 6:
            delay = 0.5
            print("OK!")
            print("주의: 6 이하의 성력에서는 명령어 사용 시 가스가 부족할 수 있습니다. 이 경우 bot.py에서 적절한 딜레이를 추가하세요.\n")
            break
        else:
            delay = 0.32
            print("OK!\n")
            break

with open("getdata.json", "rt", encoding="UTF-8") as file:
    data = json.load(file)
crops = data['crop']

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()
conn.execute("CREATE TABLE IF NOT EXISTS crop(id TEXT PRIMARY KEY, icon TEXT, level INTEGER, strawberry INTEGER, is_tree INTEGER, growth TEXT, water TEXT, soil TEXT, health TEXT, name_ko TEXT, name_en TEXT, description_ko TEXT, description_en TEXT)")
conn.commit()


print(f"앞으로 {len(crops)}개의 작물을 데이터베이스에 추가합니다.")
for i in range(len(crops)):
    crop_info = get_crop_info(crops[i])
    cur.execute("INSERT OR REPLACE INTO crop(id, icon, level, strawberry, is_tree, growth, water, soil, health, name_ko, name_en, description_ko, description_en) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (crop_info))
    conn.commit()
    print(f"[{crop_info[1]} {crop_info[9]}] 작물 추가됨. ({i+1}/{len(crops)})")
    time.sleep(delay)
print(f"완료. 모든 작물을 성공적으로 추가했습니다.\n")

conn.close()