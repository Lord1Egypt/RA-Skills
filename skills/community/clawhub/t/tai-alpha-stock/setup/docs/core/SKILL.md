---
name: tai-alpha-stock
description: Tai Alpha stock analysis — collect, VectorBT backtest (RSI/MACD/BB), conviction score, optional ML. Persistence is SQLite (default tai_alpha_output/tai_alpha.db); override TAI_ALPHA_DB_PATH.
---

# Tai Alpha Stock

Canonical documentation lives under **`/setup`**. This file mirrors root `SKILL.md`.  
**Agents:** [AGENTS.md](AGENTS.md) (Cursor, Claude Code, OpenClaw).

## Persistence

- Default: `tai_alpha_output/tai_alpha.db`
- Override: `TAI_ALPHA_DB_PATH`
- Schema: [../../sql/schema/tai_alpha_schema_consolidated.sql](../../sql/schema/tai_alpha_schema_consolidated.sql)

## Workflow

- Full analyze: `python scripts/analyze.py TICKER`
- Flags: `--fast`, `--depth lite|standard|deep`, `--persona`, `--persona-all`, `--market`, `--lang` (see [../../README.md](../../README.md))
- Report: `python scripts/report.py --run-id <id>`
- Score: `python scripts/score.py --run-id <id>` (optional `--deep-risk`)

See [../../USERFLOW.md](../../USERFLOW.md) and [AGENT_GUIDE.md](AGENT_GUIDE.md).

## Related ecosystem

- [openclaw/stock-analysis](https://github.com/openclaw/skills/tree/main/skills/udiedrichsen/stock-analysis)
- [UZI-Skill](https://github.com/wbh604/UZI-Skill)

## Test

```bash
pip install -e ".[dev]"
pytest tests/unit tests/integration -v
```
