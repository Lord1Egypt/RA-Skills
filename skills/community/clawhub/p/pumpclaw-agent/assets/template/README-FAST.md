# FAST PATH: standalone Telegram demo bot + local billing service

You now have:
- Billing service (localhost): http://127.0.0.1:3033
- Standalone Telegram bot script: src/standalone-telegram.cjs

## 1) Put your Telegram bot token into env

Create env file:

```bash
cd /data/.openclaw/workspace/demo-billing
cp .env.standalone.example .env.standalone
nano .env.standalone
```

Set:
- TELEGRAM_BOT_TOKEN=... (from @BotFather)

## 2) Run standalone bot

```bash
cd /data/.openclaw/workspace/demo-billing
set -a && . ./.env.standalone && set +a
node src/standalone-telegram.cjs
```

Commands:
- /deposit
- /confirm <lamports>
- /balance
