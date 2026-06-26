# 텔레그램 봇 설정 가이드

## 1. 봇 생성

1. 텔레그램에서 [@BotFather](https://t.me/BotFather) 검색
2. `/newbot` 명령어 전송
3. 봇 이름 입력 (예: `GeekNews Brief Bot`)
4. 봇 username 입력 (예: `geeknews_oss_brief_bot`)
5. 발급된 **봇 토큰**을 안전하게 저장

## 2. Chat ID 확인

### 개인 채팅
1. 생성한 봇에게 아무 메시지 전송
2. 브라우저에서 접속:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
3. JSON 응답에서 `"chat": {"id": 123456789}` 확인

### 그룹/채널
1. 봇을 그룹에 추가
2. 그룹에서 아무 메시지 전송
3. 위와 같은 방법으로 chat ID 확인 (그룹은 음수 ID)

## 3. 환경변수 설정

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
export TELEGRAM_BOT_TOKEN="your-bot-token-here"
export TELEGRAM_CHAT_ID="your-chat-id-here"

# 선택: GitHub API rate limit 완화용
export GITHUB_TOKEN="your-github-token-here"
```

설정 후:
```bash
source ~/.bashrc
```

## 4. 테스트

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d chat_id="${TELEGRAM_CHAT_ID}" \
  -d text="테스트 메시지입니다" \
  -d parse_mode="MarkdownV2"
```

메시지가 오면 설정 완료.
