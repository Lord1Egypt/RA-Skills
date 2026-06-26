---
name: translateflow
description: AI translation via TranslateFlow API — multi-language content translation, localization, tone adaptation, batch translation. Use when user needs text translated, content localized, or multi-language support for documents or apps. Free tier available (100 req/day).
---

# TranslateFlow

AI translation API by Voss Consulting Group.

## Setup

Set `TRANSLATEFLOW_API_KEY` or `TRANSLATEFLOW_EMAIL` for auto-signup (free, no credit card).

```bash
curl -X POST https://anton.vosscg.com/v1/keys -H 'Content-Type: application/json' -d '{"email":"you@example.com"}'
```

## Usage

```bash
curl -X POST https://anton.vosscg.com/v1/translate \
  -H "Authorization: Bearer $TRANSLATEFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "target_lang": "es", "tone": "formal"}'
```

## Capabilities
- Text translation (50+ languages)
- Tone adaptation (formal, casual, technical)
- Batch translation for multiple strings
- Content localization with cultural context

## API Reference
- `POST /v1/translate` — Translate text
- `POST /v1/translate/batch` — Batch translate
- `POST /v1/keys` — Get API key (email-only for free tier)
- `GET /v1/health` — Health check
