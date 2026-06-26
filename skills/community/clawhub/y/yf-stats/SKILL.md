---
name: yf-stats
description: Fetches stock data and generates price charts.
metadata:
  openclaw:
    emoji: "📈"
    binaries: ["python3"]
    dependencies: 
      python: "requirements.txt"
    command: "python3 yf_scraper.py {{ticker}} {{chart_flag}}"
---

# Yahoo Finance Pro

Use this to get financial data. If the user asks for a "chart," "graph," or "trend," include the `--chart` flag.

## Parameters
- `ticker`: The symbol (e.g., ONDS).
- `chart_flag`: Use `--chart` if a visual is requested, otherwise leave blank.

## Example
- User: "Show me the ONDS chart."
- Agent runs: `python3 yf_scraper.py ONDS --chart`
