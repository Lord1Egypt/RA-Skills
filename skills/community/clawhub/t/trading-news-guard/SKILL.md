---
name: "trading-news-guard"
description: "News blackout awareness for trading: local reference for high-impact events (NFP/CPI/FOMC) and blackout-window logic. The agent decides whether to trade. 100% lokal reference — ingen netværkskald, ingen API-nøgle."
metadata: {"clawbot": {"requires": {"python3": true}, "notes": "100% lokal analyse — ingen netværkskald, ingen API-nøgle."}}
---

# Trading News Guard 🛡️📰

## ⚠️ Important (read first)

- **This skill provides DATA, not enforcement.** It fetches the news status — your agent must decide whether to skip the trade. Do not assume safety is guaranteed.
- **Fail closed:** if the API is unreachable, treat it as a blackout (do not trade) rather than proceeding.

## Why it is critical

High-impact news (NFP, CPI, FOMC, ECB) can move the market 50-200+ points in seconds. Even perfect DRT/ICT setups get run over if you are in a position during a news candle. Professional traders close positions or wait — your agent should do the same.

## Command

```bash

# 2) Check news status BEFORE entry
```

## Output (example)

```json
{
  "status": "blackout" | "clear",
  "current_event": "CPI m/m — High Impact",
  "next_events": [
    {"name": "FOMC Statement", "impact": "High", "time": "19:00 UTC"}
  ]
}
```

## Use in your agent (pseudo-code)

```python
news = check_news()                      # calls the API
if news["status"] == "blackout":
    skip_trade("News blackout: " + news["current_event"])
else:
    place_trade()                        # only when the market is clear
```

## Payment

## Files

```
trading-news-guard/
├── SKILL.md
```

## Rules
- ALWAYS check news before entry — especially in London/NY windows (08:00-17:00 CET)
- Blackout = no new position. The period typically lasts 5-30 min around the event
- Exception: if your strategy explicitly trades news (not DRT/ICT) — then use this skill to KNOW when it happens
---
