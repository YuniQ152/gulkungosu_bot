import discord
from discord.ext import commands
import os, asyncio
from dotenv import load_dotenv
from utils import *

load_dotenv()
TOKEN=os.getenv("DISCORD_BOT_TOKEN")

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", case_insensitive=True, activity=discord.Activity(type=discord.ActivityType.playing, name="글쿤 고수"), intents=intents)

    async def setup_hook(self):
        await self.tree.sync() # 이렇게 하면 슬커가 서버에 sync 되는데까지 최대 1시간 걸립니다
        # await self.tree.sync(guild = discord.Object(id = YOUR_GUILD_ID)) # 하나의 서버에만 슬커를 사용하고 싶다면 이것을 사용하세요
        print(f"logged in as {bot.user} (ID: {bot.user.id})")
        print("------------")
    
        
bot = Bot()


@bot.hybrid_command(name="공동농장",
                    aliases=['공동', '공', 'ㄱㄷㄴㅈ', 'ㄱㄷㄵ', 'ㄱㄷ', 'ㄱ'],
                    description="서버의 공동농장 관련 정보를 보여줍니다.",
                    with_app_command=True)
async def cofarm2_command(ctx: commands.Context):
    await ctx.defer(ephemeral = True)
    
    response_code, cofarm_id_list = get_cofarm_channel_id(ctx.guild.id)
    if response_code != 200: await ctx.reply(f"오류가 발생했습니다. 오류 코드: {response_code}. ({response_code_to_text(response_code)})"); return
    
    if len(cofarm_id_list) == 0: # 서버에 공동농장이 없을 때
        await ctx.reply(f"**{ctx.guild.name}**에는 공동농장이 없습니다.")
        return

    embeds = []
    for cofarm_id in cofarm_id_list:
        await ctx.defer(ephemeral = True)
        
        response_code, farms, contributions = get_cofarm_info(ctx.guild.id, cofarm_id)
        if response_code != 200: await ctx.reply(f"오류가 발생했습니다. 오류 코드: {response_code}. ({response_code_to_text(response_code)})"); return

        channel = bot.get_channel(int(cofarm_id))

        plowable  = 0 # 밭갈기 가능 수
        waterable = 0 # 물주기 가능 수
        severe_count = 0 # 위독한 작물 수
        severe_text = ""
        score = 0 # 농장 점수
        for crop in farms:

            if crop is not None: # 작물이 심어져 있을 때
                crop_id      = crop['staticCropId'] # 작물ID
                status       = crop['status']       # 상태: 0 정상 | 1 다갈증 | 2 나쁜 곰팡이 | 3 지렁이
                health       = crop['health']       # 체력
                humidity     = crop['humidity']     # 수분
                fertility    = crop['fertility']    # 비옥도
                acceleration = crop['acceleration'] # 성장 가속
                growth       = crop['growth']       # "dirt" "germination" "maturity" "fruitage"

                score += (health                              **(3-health)   *0.75 +
                         (fertility if fertility < 0.9 else 1)**(3-fertility)*0.2 +
                         (humidity  if humidity  < 0.9 else 1)**(3-humidity )*0.05
                         ) / len(farms)

                if fertility < 0.9:
                    plowable += 1
                if humidity < 0.9:
                    waterable += 1

                if humidity < 0.2 or fertility < 0.3 or health < 0.5:
                    severe_count += 1
                    if   growth == "dirt":        severe_text += f"> 🟫"
                    elif growth == "germination": severe_text += f"> 🌱"
                    elif growth == "maturity":    severe_text += f"> 🌿"
                    elif growth == "fruitage":    severe_text += f"> {fetch_crop_info(crop_id)['icon']}"
                    severe_text += f" **{fetch_crop_info(crop_id)['name_ko']}**"

                    if fertility < 0.3: severe_text += f" | 🍔 비옥도: `{int(fertility*100)}%`"
                    if humidity < 0.2:  severe_text += f" | 💧 수분: `{int(humidity*100)}%`"
                    if health < 0.5:    severe_text += f" | 💚 체력: `{int(health*100)}%`"
                    if status == 1:     severe_text += f" | 🤒 다갈증"
                    if status == 2:     severe_text += f" | 🦠 곰팡이"

                    severe_text += "\n"

            # await asyncio.sleep(4) # <- 가스가 부족하다면 딜레이를 추가하세요

        crop_count = 0
        for crop in farms:
            if crop is not None:
                crop_count += 1

        activitible_text=""
        activitible_text += f"> 🚿 **물 뿌리기**: `{waterable}`\n"
        activitible_text += f"> ⚒️ **밭 갈기**: `{plowable}`"

        description = f">>> 🔗 바로가기: {channel.mention}\n"
        description += f"🌱 작물 수: `{crop_count}`/{len(farms)}"
        if crop_count == len(farms): description += "\n"
        else:                        description += " \❗ \n"
        description += f"💯 농장 점수: {int(score*100)}점"
        color = embed_color(score)
        embed=discord.Embed(title=f"#{channel.name} 채널의 공동농장", description=description, color=discord.Color.from_rgb(color[0], color[1], color[2]))
        if plowable != 0 or waterable != 0:
            embed.add_field(name=f"💙 활동력 소비 가능: {waterable*5+plowable*20}", value=activitible_text, inline=False)
        if severe_count != 0:
            embed.add_field(name=f"😵 위독함: {severe_count}", value=severe_text, inline=False)

        embeds.append(embed)
    await ctx.send(embeds=embeds)


bot.run(TOKEN)
