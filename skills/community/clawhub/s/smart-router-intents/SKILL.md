# smart-router-intents

Route any query by intent.  
Code, analysis, creative, realtime, general.  
All routed to DeepSeek V4 Flash — the cheapest capable model for every intent.

## How it works

```
INPUT: any query
  ↓
Is it cached? → Return instantly (0 cost)
  ↓ if no
Detect intent → Route to DeepSeek V4 Flash
```

## Speed

**2ms per query.**

That's how long the classifier takes. The model answers the rest.

## Intent detection detail

```
CODE
  Keywords: write, code, debug, fix, refactor, function, class, test
  → DeepSeek V4 Flash

ANALYSIS
  Keywords: analyze, explain, compare, research, evaluate, assess
  → DeepSeek V4 Flash

CREATIVE
  Keywords: write a story, brainstorm, imagine, design, draft
  → DeepSeek V4 Flash

REALTIME
  Keywords: now, today, current, latest, news, price, weather
  → DeepSeek V4 Flash

GENERAL
  Default. Simple Q&A, translate, summarize, chat
  → DeepSeek V4 Flash
```

## What you save

| Setup | Cost per 1k queries |
|-------|-------------------|
| All on premium reasoning model | $15+ |
| All on DeepSeek V4 Flash | $0.20 |
| **With router + cache** | **$0.05 avg** (cache hits) |

## Usage

```bash
clawhub install smart-router-intents
```

## Author

Created by CertainLogic — deterministic AI infrastructure.
certainlogic.ai