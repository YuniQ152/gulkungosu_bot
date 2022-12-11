## 이것은
디스코드 봇 ｢글쿤 고수｣의 공동농장 명령어 기능입니다.

## 요구사항
- Python 3.10+
- discord.py 2.0+

## 시작하기
1. [Discord 개발자 포털](https://discord.com/developers/applications)에서, 어플리케이션을 생성하세요
2. [파란 머리 모레미 API 문서](https://farm.jjo.kr/api/help/index.html)에서, API 키를 발급받으세요
3. `.env` 파일을 열고, 다음을 수정하세요:
   - 1번 과정에서의 Discord 봇 토큰을 복사해서, `Your.Discord.Bot.Token.Here` 부분을 복사한 토큰으로 교체하세요
   - 2번 과정에서의 파머모 API 키를 복사해서, `your-bhmo-api-token-here` 부분을 복사한 키로 교체하세요. `Bearer`는 남겨두어야 합니다
   - 변경한 파일을 저장하세요 (Ctrl+S)
4. `setup.py` 파일을 실행하세요:
   - 달달소의 성력을 숫자로 입력하고 `Enter` 합니다
   - 기다립니다. 달달소의 성력에 따라 최대 40초 정도 소요됩니다
5. `bot.py` 파일을 실행하고, Discord 봇을 원하는 서버에 초대합니다.
6. 이제 명령어를 사용할 수 있습니다! 기본 공동농장 명령어는 `!공동농장` 또는 `!ㄱ`입니다
