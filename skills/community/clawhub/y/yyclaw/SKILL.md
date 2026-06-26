# YYClaw — Pay-Per-Call AI Gateway Skill

## Description
Use YYClaw API to call 50+ AI models (Claude, Gemini) with on-chain stablecoin payments. Check balance, usage, list models, and make API calls — all with a single API key.

## Setup

### Required Environment
- `YYCLAW_API_KEY` — Your API key (starts with `sk-yy-`). Get one at https://crypto.yyclaw.cc by connecting your wallet.

### Optional
- `YYCLAW_BASE_URL` — Override gateway URL (default: `https://crypto.yyclaw.cc`)

## API Reference

Base URL: `https://crypto.yyclaw.cc`

All endpoints use `Authorization: Bearer <YYCLAW_API_KEY>` header.

### Check Balance & Remaining Credit
```
GET /v1/balance
```
Returns on-chain allowance (authorized amount), spent, remaining, call count, per-chain breakdown, and wallet address.

Response:
```json
{
  "balance": 50.00,
  "spent": 2.34,
  "remaining": 47.66,
  "calls": 28,
  "chains": { "bsc": 50.00, "base": 0 },
  "wallet": "0x..."
}
```

### Check Usage & Logs
```
GET /v1/usage?limit=20
```
Returns total calls, total spent, and recent call logs.

Response:
```json
{
  "total_calls": 28,
  "total_spent": 2.34,
  "logs": [
    { "model": "gemini-3-flash-fixed", "cost": 0.02, "status": "success:0xabc...", "created_at": "2026-03-18 12:00:00" }
  ]
}
```

### List Available Models
```
GET /v1/models
```
Returns all enabled models with per-call pricing. No auth required.

### Call a Model (OpenAI-compatible)
```
POST /v1/chat/completions
Content-Type: application/json

{
  "model": "gemini-3-flash",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}
```
The `-fixed` suffix is auto-appended if omitted. Supports streaming (`"stream": true`).

## Model Aliases (shorthand → full name)
| Short | Model | Price/call |
|-------|-------|-----------|
| gemini-3-flash | gemini-3-flash-fixed | $0.020 |
| gemini-2.5-flash | gemini-2.5-flash-fixed | $0.010 |
| gemini-3-pro-preview | gemini-3-pro-preview-fixed | $0.080 |
| claude-haiku-4.5 | claude-haiku-4.5-fixed | $0.064 |
| claude-sonnet-4-6 | claude-sonnet-4-6-fixed | $0.100 |
| claude-opus-4.6 | claude-opus-4.6-fixed | $0.160 |

## Instructions for Agent

When this skill is active, use `curl` or any HTTP client to interact with YYClaw.

### Reading API Key
```bash
echo $YYCLAW_API_KEY
```
If not set, ask the user to provide it or direct them to https://crypto.yyclaw.cc to get one.

### Check Balance
```bash
curl -s -H "Authorization: Bearer $YYCLAW_API_KEY" https://crypto.yyclaw.cc/v1/balance | python3 -m json.tool
```

### Check Usage
```bash
curl -s -H "Authorization: Bearer $YYCLAW_API_KEY" https://crypto.yyclaw.cc/v1/usage?limit=10 | python3 -m json.tool
```

### List Models
```bash
curl -s https://crypto.yyclaw.cc/v1/models | python3 -m json.tool
```

### Call a Model
```bash
curl -s -X POST https://crypto.yyclaw.cc/v1/chat/completions \
  -H "Authorization: Bearer $YYCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-3-flash","messages":[{"role":"user","content":"Hello"}]}'
```

### OpenAI SDK (Python)
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["YYCLAW_API_KEY"],
    base_url="https://crypto.yyclaw.cc/v1"
)

response = client.chat.completions.create(
    model="gemini-3-flash",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

### OpenAI SDK (JavaScript)
```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.YYCLAW_API_KEY,
  baseURL: 'https://crypto.yyclaw.cc/v1'
});

const res = await client.chat.completions.create({
  model: 'gemini-3-flash',
  messages: [{ role: 'user', content: 'Hello' }]
});
console.log(res.choices[0].message.content);
```

## Error Handling
| Code | Meaning | Action |
|------|---------|--------|
| 401 | Invalid API key | Check YYCLAW_API_KEY |
| 402 | Insufficient balance/allowance | User needs to approve more tokens at dashboard |
| 404 | Model not found | Check /v1/models for available models |
| 503 | Model upstream not configured | Contact admin |

## Triggers
- "check yyclaw balance" / "查看 yyclaw 余额"
- "yyclaw usage" / "yyclaw 用量"
- "list yyclaw models" / "yyclaw 模型列表"
- "call yyclaw model" / "用 yyclaw 调用模型"
- "yyclaw remaining credit" / "yyclaw 剩余额度"
- Any mention of calling AI models through YYClaw
