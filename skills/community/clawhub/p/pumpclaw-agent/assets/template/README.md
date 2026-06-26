# demo-billing

Demo services for Telegram funding → per-user wallet → server pays Pump invoice → credits.

## Setup

```bash
cd demo-billing
cp .env.example .env
# edit .env and set:
# - TREASURY_SECRET_KEY_BASE58
# - API_TOKEN
npm start
```

Health check:

```bash
curl http://127.0.0.1:3033/health
```

## API
All endpoints (except /health) require header:

`x-api-token: <API_TOKEN>`

- `POST /deposit-wallet { telegramUserId }` → `{ depositAddress }`
- `POST /fund-and-credit { telegramUserId, depositLamports }`
- `POST /balance { telegramUserId }`
- `POST /spend { telegramUserId, credits }`
