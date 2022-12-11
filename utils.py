import os, requests, json, sqlite3
from dotenv import load_dotenv
from ast import literal_eval

load_dotenv()
conn = sqlite3.connect("db.sqlite3")
conn.row_factory = sqlite3.Row
cur = conn.cursor()


def get_cofarm_channel_id(server_id: int):
    url = "https://farm.jjo.kr/api/guild/" + str(server_id)
    response = requests.get(url, headers={"Authorization": os.getenv("BHMO_API_TOKEN")})
    if response.status_code == 200:
        cofarms = json.loads(response.content)["cofarms"]
        cofarm_channel_id = []
        for i in range(len(cofarms)):
            cofarm_channel_id.append(cofarms[i]["id"])
        return(response.status_code, cofarm_channel_id)
    else:
        return(response.status_code, None)

def get_cofarm_info(server_id: int, channel_id: int):
    url = "https://farm.jjo.kr/api/guild/" + str(server_id) + "/cofarm/" + str(channel_id)
    response = requests.get(url, headers={"Authorization": os.getenv("BHMO_API_TOKEN")})
    if response.status_code == 200:
        farms         = json.loads(response.content)["farms"]
        contributions = json.loads(response.content)["contributions"]
        return(response.status_code, farms, contributions)
    else:
        return(response.status_code, None, None)

def fetch_crop_info(crop_id):
    cur.execute("SELECT * FROM crop WHERE id = ?", (crop_id, ))
    row = dict(cur.fetchone())
    if row['item_link'] is not None:
        row['item_link'] = literal_eval(row['item_link'])
    return row

def embed_color(ratio: float) -> tuple:
    """1.0 = Green | 0.5 = Yellow | 0.0 = Red"""
    green  = [ 46, 204, 113]
    yellow = [241, 196,  15]
    red    = [231,  76,  60]
    generated_color = []
    if ratio > 1:
        generated_color = green
    elif ratio < 0:
        generated_color = red
    elif ratio >= 0.5: # Green ~ Yellow
        ratio = (ratio-0.5)*2
        for i in range(3):
            generated_color.append(int(green[i]*ratio + yellow[i]*(1.0-ratio)))
    else: # Yellow ~ Red
        ratio = ratio*2
        for i in range(3):
            generated_color.append(int(yellow[i]*ratio + red[i]*(1.0-ratio)))
    print(generated_color)
    return tuple(generated_color)

def response_code_to_text(response_code: int) -> str:
    if response_code == 401:
        return("인증 실패")
    elif response_code == 403:
        return("API 사용자의 계정이 아님")
    elif response_code == 404:
        return("그런 건 없음")
    elif response_code == 406:
        return("해당 여행자가 API 정보 활용을 거부함")
    elif response_code == 412:
        return("요청 형식 검증 실패")
    elif response_code == 416:
        return("내용의 길이가 범위 밖임")
    elif response_code == 429:
        return("가스 부족")
    else:
        return("알 수 없음")