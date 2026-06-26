---
name: quorumai
description: Run multi-model AI synthesis inquiries via QuorumAI. Four AI models (Claude, GPT, Gemini, Grok) compete to answer your question from specialized perspectives, get scored by an arbiter, and the best elements are synthesized into one ultimate answer.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - QUORUMAI_API_KEY
      bins:
        - curl
    primaryEnv: QUORUMAI_API_KEY
    emoji: "🏛️"
    homepage: https://quorumai.io
---

# QuorumAI — Multi-Model AI Synthesis

Ask a question once. Four AI models (Claude, GPT, Gemini, Grok) answer simultaneously from specialized perspectives, an arbiter scores them, and you get one synthesized best answer.

## Setup

Get your free API key at https://quorumai.io/account (sign up, go to API Keys, generate one). The key starts with `qai_`.

Set it in your OpenClaw config:

```
QUORUMAI_API_KEY=qai_your_key_here
```

## Usage

When the user asks you to use QuorumAI, run a quorumai inquiry, or says "ask quorumai", send their question to the QuorumAI API.

### Quick Inquiry (default)

```bash
curl -s -X POST https://quorumai.io/api/v1/inquiry \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $QUORUMAI_API_KEY" \
  -d '{
    "thesis": "USER_QUESTION_HERE",
    "mode": "quick",
    "academy": "general"
  }'
```

### Standard Inquiry (dedicated arbiter, better scoring)

```bash
curl -s -X POST https://quorumai.io/api/v1/inquiry \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $QUORUMAI_API_KEY" \
  -d '{
    "thesis": "USER_QUESTION_HERE",
    "mode": "standard",
    "academy": "general"
  }'
```

### Deep Inquiry (Pro only — 4 rounds, 16 responses)

```bash
curl -s -X POST https://quorumai.io/api/v1/inquiry \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $QUORUMAI_API_KEY" \
  -d '{
    "thesis": "USER_QUESTION_HERE",
    "mode": "deep",
    "academy": "general",
    "dissent": true
  }'
```

## Parameters

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `thesis` | string | *required* | The question to ask (alias: `question`) |
| `academy` | string | `"general"` | Academy to use: `general`, `clinical`, `business`, `technical`, `investment` |
| `mode` | string | `"quick"` | Inquiry depth: `quick` (Free), `standard` (Free), `deep` (Pro) |
| `arbiter` | string | `"auto"` | Which model judges: `auto`, `claude`, `gpt`, `gemini`, `grok` |
| `dissent` | boolean | `false` | Enable dissent mode — models argue against themselves to stress-test claims (Pro) |

## Academies

- **general** — General-purpose inquiry with balanced perspectives
- **clinical** — Clinical Review Panel for medical and health questions
- **business** — Business Advisory Board for strategy and operations
- **technical** — Technical Review Board for engineering and architecture
- **investment** — Investment Committee for financial analysis

## Response Format

The API returns JSON. Here are the key fields to present to the user:

| Field | Description |
|-------|-------------|
| `synthesis` | The combined best answer — **always show this first** |
| `prima` | The top-scoring voice (winning model) |
| `voices` | Array of individual model responses with provider and school (role) |
| `scores` | Arbiter's scoring of each voice |
| `confidence` | Overall confidence percentage (when dissent is enabled) |
| `consensus_claims` | Claims all models agreed on (dissent mode) |
| `vulnerable_claims` | Claims that didn't survive adversarial analysis (dissent mode) |
| `share_url` | Public link to view the full inquiry result |

## How to Present Results

1. **Always lead with the synthesis** — this is the main answer
2. Show the prima (winning voice) and its score
3. If the user wants detail, show individual voice responses
4. If dissent was enabled, highlight consensus vs vulnerable claims
5. Always include the share_url so the user can view the full result on quorumai.io

### Example output formatting:

```
🏛️ QuorumAI Synthesis:
[synthesis text]

🏆 Top Voice: [prima provider] ([prima score])
🔗 Full result: [share_url]
```

If dissent mode was used, add:

```
✅ Consensus: [consensus_claims]
⚠️ Vulnerable: [vulnerable_claims]
📊 Confidence: [confidence]%
```

## Rate Limits

- **Free tier**: 5 inquiries/day (Quick and Standard modes only)
- **Pro tier ($9.99/mo)**: 50 inquiries/day, all modes, dissent, all academies

Rate limit headers are returned: `X-RateLimit-Limit` and `X-RateLimit-Remaining`.

If the user hits a rate limit, suggest upgrading at https://quorumai.io/account

## Error Handling

- **401**: Invalid or missing API key — direct user to https://quorumai.io/account
- **403**: Feature requires Pro tier — suggest upgrade
- **429**: Rate limit exceeded — show remaining reset time
- **500**: Server error — retry once, then report the issue

## Rules

- Always substitute the user's actual question for `USER_QUESTION_HERE`
- Default to `quick` mode and `general` academy unless the user specifies otherwise
- If the user says "deep dive" or "thorough analysis", use `deep` mode
- If the user mentions medical/health topics, suggest `clinical` academy
- If the user mentions business/strategy, suggest `business` academy
- If the user mentions code/engineering, suggest `technical` academy
- If the user mentions investing/finance, suggest `investment` academy
- Never expose the raw API key in messages to the user
- Responses can take 15-45 seconds depending on mode — let the user know it's processing
