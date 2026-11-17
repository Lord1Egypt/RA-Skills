---
name: sector-opening-note
description: "Search for current HK tech sector dynamics via public web and generate structured opening brief. USE for daily HK tech pre-market summary. NOT for: historical analysis or portfolio-specific recommendations."
homepage: https://finance.yahoo.com/sectors/technology
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "tools": ["web_search", "memory_write"] },
        "install":
          [
            {
              "id": "register",
              "kind": "register-skill",
              "label": "Register with clawhub (or local skill dir)",
            },
          ],
      },
  }
---

# Sector Opening Note

Generate structured pre-market brief for HK tech sector.

## When to Use

✅ **Daily before HK market open**

- "HK tech pre-market brief"
- "Sector opening note"
- "Today's HK tech news summary"

## When NOT to Use

❌ Historical analysis, portfolio picks, non-HK sectors

## Commands

### Generate Brief
```bash
# Run skill (OpenClaw skill entry)
openclaw sector-opening-note --date today --market hk
```

### Search For News (Under-the-hood)
```bash
# Search for current HK tech news
web_search query="HK tech sector today 2026-07-10" count=3 country=HK language=zh-hans freshness=day
```

## Parameters
- `--date`: YYYY-MM-DD (or `today`) — pulls current day
- `--market`: `hk` only (HK exchange)

## Brief Sections (Required)
1. **主题概览** — short 1-sentence headline
2. **重要新闻要点** — top 2-3 news items
3. **代表公司** — 2-3 stocks (Tencent, Alibaba, Meituan for example)
4. **情绪/风险提示** — positive/negative + 1 quick risk (e.g., regulators, earnings)
5. **后续观察点** — 2 upcoming catalysts (e.g., Fed rate, earnings release)

## Examples
`openclaw sector-opening-note --date today --market hk` → returns brief like:
> 【主题概览】HK tech mixed pre-market, Tencent leads gains
> 【重要新闻】1) Alibaba cloud revenue up 8% YoY; 2) Meituan deliveries hit record
> 【代表公司】Tencent (0700.HK), Alibaba (9988.HK), Meituan (3690.HK)
> 【情绪/风险】Mildly positive; risk = US-China trade comments
> 【后续观察点】Fed minutes, Tencent earnings (Friday)
