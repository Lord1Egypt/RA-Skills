---
name: trendproof
description: >
  Query TrendProof (trendproof.dev) for keyword trend velocity scores.
  Returns velocity score, trend direction (rising/stable/falling), monthly
  search volume, CPC, peak window, and action hint. Supports single keyword
  analysis, batch comparison (up to 5 keywords ranked by velocity), and
  related keyword discovery. Use when a user asks about keyword trends,
  whether a topic is rising or falling, content timing, wants to compare
  niches, or needs similar keyword suggestions.
---

# TrendProof

**Trend velocity intelligence for AI agents.** Check whether a keyword is rising, stable, or falling before you create content, run ads, or build a product.

Live at **[trendproof.dev](https://trendproof.dev)**

---

## Setup (API key)

**Before doing anything else** — check if the API key is already configured:

```bash
python3 skills/trendproof/scripts/trendproof.py configure --show
```

**If no key is found**, stop and tell the user exactly this (do not attempt any API calls):

> "To use TrendProof, you need a free API key.
> 1. Open **https://trendproof.dev/dashboard#keys** (sign up if needed — 5 free trial credits included)
> 2. Copy your key (starts with `TRND_`) and send it to me"

Once the user provides the key, save it:
```bash
python3 skills/trendproof/scripts/trendproof.py configure --api-key TRND_xxxxx
```

Or set the environment variable:
```bash
export TRENDPROOF_API_KEY=TRND_xxxxx
```

---

## Analyze a single keyword

```bash
python3 skills/trendproof/scripts/trendproof.py analyze "AI agents"
```

Example output:
```
  Keyword      ai agents
  Velocity     [████████████░░░░░░░░] +87
  Direction    🚀  RISING
  Volume       8,100 / mo
  CPC          $2.45   CPM $6.13
  Competition  0.38
  Peak window  2026-02-10 — 2026-03-03
  Hint         🚀 Strong momentum — act now before peak. High CPC = strong intent.
  Took         1243ms
```

### With location (UK example):
```bash
python3 skills/trendproof/scripts/trendproof.py analyze "rust programming" --location 2826
```

### Raw JSON output:
```bash
python3 skills/trendproof/scripts/trendproof.py analyze "prompt engineering" --json
```

---

## Batch analysis (ranked)

Compare multiple keywords and get them ranked by velocity:

```bash
python3 skills/trendproof/scripts/trendproof.py batch "AI agents" "LLM fine-tuning" "RAG pipeline" "vector search"
```

Output (sorted by velocity score):
```
Keyword                             Score  Direction    Volume     CPC
---------------------------------------------------------------------------
AI agents                           +87   🚀 rising    8,100    $2.45
RAG pipeline                        +34   🚀 rising    2,400    $1.80
LLM fine-tuning                      +8   📊 stable    5,500    $3.20
vector search                       -12   📉 falling   3,300    $1.10

  Total cost: $0.3360
```

### From a file:
```bash
python3 skills/trendproof/scripts/trendproof.py batch-file keywords.txt
```

File format (one keyword per line, `#` for comments):
```
# AI keywords
AI agents
LLM fine-tuning
RAG pipeline
```

---

## Velocity score interpretation

| Score | Meaning |
|-------|---------|
| > 50 | 🚀 Strong uptrend — act now |
| 10–50 | 🚀 Rising — good timing window |
| -10 to +10 | 📊 Stable — safe but no momentum |
| -10 to -50 | 📉 Declining — consider alternatives |
| < -50 | 📉 Sharp decline — avoid |

Score formula: `((last 4 weeks avg − prior 4 weeks avg) / prior 4 weeks avg) × 100`, capped at [-100, +200].

---

## Related keywords

Discover similar keywords with volume and CPC:

```bash
python3 skills/trendproof/scripts/trendproof.py related "AI agents"
```

Output:
```
  Similar to: AI agents

  Keyword                              Volume        CPC
  ─────────────────────────────────────────────────────────
  ai agent tools                        2,400      $3.10
  autonomous ai agents                  1,900      $4.20
  ...
```

---

## API reference (direct HTTP)

For advanced use, call the API directly:

```bash
# Analyze
curl -s https://trendproof.dev/api/analyze \
  -H "Authorization: Bearer TRND_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "AI agents"}'

# Related keywords
curl -s https://trendproof.dev/api/related \
  -H "Authorization: Bearer TRND_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "AI agents"}'

# Public leaderboard (no auth)
curl -s "https://trendproof.dev/api/leaderboard?limit=10&sort=velocity"
```

Response fields:
- `velocity_score` — -100 to +200; positive = rising
- `trend_direction` — `rising` | `stable` | `falling`
- `volume` — monthly search volume
- `cpc` — cost-per-click (USD)
- `cpm` — estimated CPM (cpc × 2.5)
- `competition` — 0–1 (DataForSEO competition index)
- `peak_window` — date range of highest trend activity
- `monthly_searches` — last 12 months of volume data
- `trend_data` — 12-week Google Trends graph (0–100 values)
- `action_hint` — human-readable recommendation

---

## Agent tool call pattern

When used as an AI agent tool, format results like:

> **"AI agents"** — velocity +87 🚀 rising, 8,100/mo, CPC $2.45. Peak: Feb–Mar 2026. **Act now before peak.**

For batch comparisons, present as a ranked list with winner highlighted.

---

## Troubleshooting

- **No key configured**: Run `configure --show`. If empty → ask user to get key at https://trendproof.dev/dashboard#keys
- **401 / unauthorized**: Key is set but invalid or revoked. Ask user to rotate at trendproof.dev/dashboard → API Keys → Rotate.
- **429 / credits exhausted**: Upgrade at trendproof.dev/dashboard → Billing.
- **Slow response (>5s)**: DataForSEO live API — expected for uncached keywords.
- **score = 0 + stable**: Likely very low-volume keyword; check `trend_data` array.
