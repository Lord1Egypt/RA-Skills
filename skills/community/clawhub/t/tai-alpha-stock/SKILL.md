---
name: tai-alpha-stock
description: Tai Alpha stock analysis — collect, VectorBT backtest (RSI/MACD/BB), conviction score, optional ML. Persistence is SQLite (default tai_alpha_output/tai_alpha.db); override TAI_ALPHA_DB_PATH.
---

# Tai Alpha Stock

**Canonical docs:** `/setup` (README, USERFLOW, MODULE_STRUCTURE, guides).  
**Mirror:** [setup/docs/core/SKILL.md](setup/docs/core/SKILL.md).  
**Agents (Cursor / Claude Code / OpenClaw):** [setup/docs/core/AGENTS.md](setup/docs/core/AGENTS.md) — root stubs `AGENTS.md`, `CLAUDE.md`.

## Workflow tree

- **Single:** `python scripts/analyze.py TICKER` → pipeline; stores rows in SQLite (`--db-path` optional).
- **Personas / markets:** `--persona id` / `--persona-all`; `--market auto|us|hk|cn`; `--lang zh-CN|zh-HK` (see [setup/docs/guides/PERSONA_ECOSYSTEM_GUIDE.md](setup/docs/guides/PERSONA_ECOSYSTEM_GUIDE.md)).
- **Fast / depth:** `--fast` skips ML and uses lighter collect; `--depth lite|standard|deep` (see [setup/README.md](setup/README.md) matrix).
- **Batch:** `python scripts/batch.py TICKER1 TICKER2` (optional `--fast`, `--depth`).
- **Portfolio:** `python scripts/portfolio.py TICKER ...`
- **Cron:** `python scripts/cron.py` (`TAI_ALPHA_HOTLIST`, optional `TAI_ALPHA_TELEGRAM_WEBHOOK`)
- **Alerts:** `python scripts/alerts.py` (watchlist in SQLite)
- **Custom / ML / sector:** `scripts/custom.py`, `scripts/ml.py`, `scripts/sector.py`
- **Dividends / movers:** `scripts/dividends.py`, `scripts/hot_scanner.py` (see setup README)
- **Inspect run:** `python scripts/report.py --run-id N` / `python scripts/score.py --run-id N` (`--deep-risk` on score CLI)

## Docs

- [setup/docs/guides/DISCLAIMER_AND_LIMITATIONS.md](setup/docs/guides/DISCLAIMER_AND_LIMITATIONS.md)
- [setup/docs/guides/STRATEGIES.md](setup/docs/guides/STRATEGIES.md)
- [setup/docs/database/SQLITE.md](setup/docs/database/SQLITE.md)
- [setup/docs/core/AGENT_GUIDE.md](setup/docs/core/AGENT_GUIDE.md)
- [setup/docs/guides/PERSONA_ECOSYSTEM_GUIDE.md](setup/docs/guides/PERSONA_ECOSYSTEM_GUIDE.md)
- [setup/docs/guides/CHINESE_AUDIENCE_GUIDE.md](setup/docs/guides/CHINESE_AUDIENCE_GUIDE.md)

## Related projects (inspiration)

- [openclaw/stock-analysis skill](https://github.com/openclaw/skills/tree/main/skills/udiedrichsen/stock-analysis)
- [UZI-Skill](https://github.com/wbh604/UZI-Skill)

## Test

```bash
pip install -e ".[dev]"
pytest tests/unit tests/integration -v
python setup/tools/check_structure.py
```
