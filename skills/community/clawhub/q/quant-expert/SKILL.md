---
name: quant-expert
description: Quantitative analysis skill for the Chinese A-share market using Tushare Pro data and a holiday helper. Use when the user asks for stock screening, stock diagnosis, market or sector analysis, money-flow checks, ETF or option data, macro data, trading-day queries, holiday checks, or raw Tushare data related to Chinese securities.
metadata: {"openclaw":{"emoji":"📈","primaryEnv":"TUSHARE_TOKEN","requires":{"anyBins":["python","python3","py"]},"os":["darwin","linux","win32"]}}
---

# Quant Expert

Use this skill for Chinese A-share quantitative work in OpenClaw.

## OpenClaw Setup

OpenClaw-friendly rule:

- Keep the Tushare token outside the repository.
- Prefer OpenClaw config injection over manual shell export.
- Do not auto-install Python packages.

Recommended OpenClaw config:

```json
{
  "skills": {
    "entries": {
      "quant-expert": {
        "apiKey": "your-tushare-token"
      }
    }
  }
}
```

Because `primaryEnv` is set to `TUSHARE_TOKEN`, OpenClaw can inject the token for this skill automatically.

Required Python packages for Tushare features:

- `tushare`
- `pandas`
- `requests`

Note:

- `holiday_helper.py` does not need `TUSHARE_TOKEN`.
- All other bundled scripts need `TUSHARE_TOKEN`.

## Hard Rules

1. If dependencies or `TUSHARE_TOKEN` are missing, stop and report the blocker clearly.
2. Do not install packages unless the user explicitly asks.
3. Use Tushare as the primary numeric data source.
4. Only add web research when the user wants interpretation, diagnosis, ranking, or recommendation.
5. If Tushare is blocked, report the blocker instead of silently replacing numeric facts with web data.

## Path Rule

When referencing bundled files in OpenClaw, use `{baseDir}`:

- `{baseDir}/scripts/tushare_helper.py`
- `{baseDir}/scripts/stock_screener.py`
- `{baseDir}/scripts/stock_diagnosis.py`
- `{baseDir}/scripts/holiday_helper.py`
- `{baseDir}/references/api_quick_reference.md`
- `{baseDir}/references/analysis_strategies.md`

## What To Use

### Raw Tushare query

Use `{baseDir}/scripts/tushare_helper.py`.

Example:

```bash
python {baseDir}/scripts/tushare_helper.py stock_basic '{"list_status":"L"}' -n 20
python {baseDir}/scripts/tushare_helper.py daily_basic '{"trade_date":"20260302"}' -f ts_code,pe_ttm,pb,total_mv
```

### Stock screening

Use `{baseDir}/scripts/stock_screener.py`.

- `value`: low `PE_TTM`, low `PB`, minimum market cap, minimum `ROE`, exclude ST
- `dividend`: minimum `dv_ttm`, then verify consecutive dividend years
- `growth`: revenue YoY, profit YoY, and `ROE`
- `momentum`: daily gain, volume ratio, turnover rate

Example:

```bash
python {baseDir}/scripts/stock_screener.py -s value --pe-max 20 --roe-min 15 --mv-min 100
python {baseDir}/scripts/stock_screener.py -s growth --rev-growth-min 20 --profit-growth-min 25
```

### Stock diagnosis

Use `{baseDir}/scripts/stock_diagnosis.py`.

Current built-in diagnosis is a structured snapshot, not an automatic rating model.

It covers:

- company basics
- price performance
- valuation snapshot
- income and financial-indicator trends
- top shareholders and holder-count trend
- recent money flow
- ST, pledge, and restricted-share checks

Example:

```bash
python {baseDir}/scripts/stock_diagnosis.py 600519.SH
```

### Trading day and holiday

Use `{baseDir}/scripts/holiday_helper.py`.

Example:

```bash
python {baseDir}/scripts/holiday_helper.py check
python {baseDir}/scripts/holiday_helper.py next 2026-09-30
```

## Beijing Time Rule

Always reason in Beijing time.

- Before 15:30 Beijing time, daily market data usually means the previous trading day.
- After 15:30 Beijing time, same-day daily data may be available.
- Do not hardcode dates when the helper utilities can derive them.

## OpenClaw Execution Pattern

### If the user wants raw data

- Stay on the Tushare data layer.
- Use one bundled script first.
- Return concise results without forcing event research.

### If the user wants judgment or interpretation

1. Pull numeric evidence with Tushare first.
2. Add event evidence from credible web sources.
3. Keep the final answer in this order:
   1. one-line conclusion
   2. key quantitative findings
   3. key event findings with source and URL
   4. resonance or divergence
   5. main risks
   6. investment disclaimer

Minimum event evidence target:

- 2 stock-level events
- 2 industry-level events
- 2 macro/global events

## References

- `{baseDir}/references/api_quick_reference.md`
- `{baseDir}/references/analysis_strategies.md`
