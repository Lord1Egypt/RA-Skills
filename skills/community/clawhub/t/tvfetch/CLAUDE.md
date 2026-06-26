# tvfetch Skill

Claude Code skill for fetching TradingView market data — OHLCV, live streaming, indicators, analysis.

## Structure
- `tvfetch/` — Core Python library (WebSocket protocol, caching, fallback)
- `scripts/lib/` — Skill-level modules (config, validators, formatters, action scripts)
- `scripts/main.py` — Unified CLI entry point
- `SKILL.md` — Claude's instruction manifest (what Claude reads on `/tvfetch`)

## Common Commands
- `python scripts/lib/fetch.py BINANCE:BTCUSDT 1D 100 --mock` (test without network)
- `python scripts/lib/analyze.py BINANCE:BTCUSDT 1D 365` (statistical analysis)
- `python scripts/lib/indicators.py BTC 1D 100 --indicators "sma:20,rsi:14,macd"` (technical indicators)
- `cd tests && python -m pytest -x -q` (run all tests)
- `python scripts/lib/config.py --show` (show resolved config)

## Rules
- `scripts/lib/__init__.py` must remain a bare package marker
- All scripts must use `formatter.py` for output (tagged sections)
- All scripts must use `errors.py` for exit codes
- Never hardcode paths — use `Path.home()` everywhere
- After tvfetch/ changes: run tests before updating skill scripts
