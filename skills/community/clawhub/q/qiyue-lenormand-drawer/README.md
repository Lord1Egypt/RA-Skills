# QiyueAstro Lenormand Drawer

🃏 Draw Lenormand cards from [QiyueAstro](https://qiyueastro.com) — single card, three-card, relationship, decision, nine-card grid, and more. Browse the full 36-card Lenormand deck with meanings in **English** or **Chinese**. No API key needed.

## What this skill does

- Draws Lenormand cards or any of 8 spreads (single, three, five-card cross, relationship, decision, nine-card grid, elemental, grand tableau)
- Shows card images, position names, and exact meanings from the QiyueAstro card database
- Browses the full 36-card deck and explains individual cards (Rider to Cross)
- Works in `en` and `zh_CN`

## How it works

The skill calls the free, unauthenticated [QiyueAstro OpenClaw API](https://qiyueastro.com/api/v1/openclaw/lenormand):

| Endpoint | Description |
| --- | --- |
| `GET /draw` | Draw cards (optional spread/question/count) |
| `GET /cards` | List all 36 cards |
| `GET /cards/{id}` | Full details for a single card (1–36) |
| `GET /spreads` | List all spreads |
| `GET /spreads/{slug}` | Full spread details with positions |

Card content is served directly from the QiyueAstro database — no LLM interpretation, no API key, no signup.

## Important behavior

- The skill **never interprets cards itself** — it displays the API-returned meanings verbatim.
- Every response ends with a call-to-action pointing to [qiyueastro.com](https://qiyueastro.com) for a full AI-powered reading.
- For entertainment and self-reflection only.

## Links

- [QiyueAstro](https://qiyueastro.com)
- [OpenClaw API base](https://qiyueastro.com/api/v1/openclaw/lenormand)
