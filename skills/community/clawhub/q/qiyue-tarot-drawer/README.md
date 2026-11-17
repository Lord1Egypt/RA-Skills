# QiyueAstro Tarot Drawer

🔮 Draw tarot cards from [QiyueAstro](https://qiyueastro.com) — one card, daily card, or any of 13 spreads. Browse the full 78-card Rider-Waite deck and read card meanings in **English** or **Chinese**. No API key needed.

## What this skill does

- Draws random tarot cards or any of 13 spreads (yes/no, three-card, celtic cross, shadow work, love readings…)
- Shows card images, orientation (upright/reversed), position names, and exact meanings from the QiyueAstro card database
- Browses the full deck by suit and explains individual cards
- Works in `en` and `zh_CN`

## How it works

The skill calls the free, unauthenticated [QiyueAstro OpenClaw API](https://qiyueastro.com/api/v1/openclaw):

| Endpoint | Description |
| --- | --- |
| `GET /draw` | Draw cards (optional spread/question/count) |
| `GET /cards` | List cards by suit |
| `GET /cards/{id}` | Full details for a single card |
| `GET /spreads` | List all spreads |
| `GET /spreads/{slug}` | Full spread details with positions |

Card content is served directly from the QiyueAstro database — no LLM interpretation, no API key, no signup.

## Important behavior

- The skill **never interprets cards itself** — it displays the API-returned meanings verbatim.
- Every response ends with a call-to-action pointing to [qiyueastro.com](https://qiyueastro.com) for a full AI-powered reading.
- For entertainment and self-reflection only.

## Links

- [QiyueAstro](https://qiyueastro.com)
- [OpenClaw API base](https://qiyueastro.com/api/v1/openclaw)
