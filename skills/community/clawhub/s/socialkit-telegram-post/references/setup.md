# Telegram setup

Generated from `docs/platforms/telegram-setup.md`; edit it there. Facts checked 2026-10-24.

1. In Telegram, message **@BotFather**, send `/newbot`, and copy the bot token.
2. Add the bot to your channel (or group) as an **administrator** with permission to post.
3. In `~/.config/social-skills/env.sh`:
   ```sh
   export TELEGRAM_BOT_TOKEN="..."
   export TELEGRAM_CHAT_ID="@yourchannel"   # or the numeric -100... id for private channels
   ```

Limits: text 4,096 characters, captions 1,024, photos 10 MB and other files 50 MB when
uploaded by a bot, albums of 2-10 items. The Bot API has no scheduling. On 429 the bot
waits the `retry_after` Telegram returns.

Keep the bot token secret: anyone with it controls the bot. Revoke it with `/revoke` in
@BotFather if it leaks.

Source: https://core.telegram.org/bots/api
