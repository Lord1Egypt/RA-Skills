# Changelog

## [1.0.0] - 2026-03-28

### Added
- Full Claude Code skill structure (SKILL.md, plugin.json, hooks)
- Natural language intent parsing in SKILL.md
- Statistical analysis module (analyze.py) — returns, volatility, Sharpe, drawdown
- Multi-symbol comparison (compare.py) — correlation, beta, relative performance
- Technical indicators (indicators.py) — SMA, EMA, RSI, MACD, BB, ATR, Stochastic, OBV, VWAP
- Hierarchical config system (env > .env > keyring > anonymous)
- Mock mode with fixture files for offline testing
- Tagged output protocol for Claude parsing
- SessionStart hook for config validation
- ClawHub marketplace metadata
- Gemini CLI extension config
- Symbol alias resolution (100+ common symbols)
- Data quality checks (gap detection, OHLCV validation)
- Alert thresholds for live streaming
- VWAP approximation during stream sessions
- Three skill variants (quant, minimal, backtesting)

### Changed
- Restructured from Python library to Claude Code skill
- Moved CLI from cli/main.py to scripts/main.py + scripts/lib/
- Updated pyproject.toml for skill layout

### From tvfetch v0.1.0
- Historical OHLCV fetching via reverse-engineered TV WebSocket
- Live price streaming
- Symbol search
- SQLite caching
- Fallback to Yahoo Finance and CCXT
- Automatic pagination for large fetches
- Exponential backoff reconnection
