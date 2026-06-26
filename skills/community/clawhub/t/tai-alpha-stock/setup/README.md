# Tai Alpha Stock — setup and docs

This directory is the **single source of truth** for project documentation and SQL (per repository standards). The Python package lives at the repo root in `tai_alpha/`; **SQLite** is the default persistence layer (see `docs/database/SQLITE.md`).

## Quick start

```bash
cd /path/to/tai-alpha-stock
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python scripts/analyze.py AAPL --no-report
# Default DB: tai_alpha_output/tai_alpha.db (override with TAI_ALPHA_DB_PATH)
```

Override output directory (where `tai_alpha.db` is placed by default):

```bash
export TAI_ALPHA_OUTPUT_DIR=/tmp/tai_run
python scripts/analyze.py MSFT
```

## Feature / flag matrix (CLI)

| Capability | Entry | Notes |
|------------|-------|--------|
| Full analyze | `scripts/analyze.py TICKER` | Collect → backtest → score → report |
| Fast path | `--fast` | Skips ML; lighter collect (no sector ETF peer fetch) |
| Depth | `--depth lite` / `standard` / `deep` | `lite` = no ML + light collect; `deep` = ML (unless `--fast`) + geopolitical `risk_flags` |
| Dividends | `scripts/dividends.py TICKER` or `tai-alpha-dividends` | yfinance dividend history; yield proxy |
| Hot scanner | `scripts/hot_scanner.py` or `tai-alpha-hot-scanner` | Yahoo movers; `--with-crypto` adds CoinGecko trending |
| Score from DB | `tai-alpha-score --run-id N` | Optional `--deep-risk` for geopolitical keyword tier |
| Personas | `--persona id1,id2` / `--persona-all` | Overlays on base score; registry in `setup/config/personas/` |
| Market routing | `--market auto` or `us` / `hk` / `cn` | Normalizes Yahoo/yfinance symbols (HK/CN suffixes) |
| Chinese report | `--lang zh-CN` / `--lang zh-HK` | Signal translation + short disclaimer |
| Disclaimer | [docs/guides/DISCLAIMER_AND_LIMITATIONS.md](docs/guides/DISCLAIMER_AND_LIMITATIONS.md) | Not financial advice; data limits |

### Related ecosystem (attribution)

- [openclaw/skills – udiedrichsen/stock-analysis](https://github.com/openclaw/skills/tree/main/skills/udiedrichsen/stock-analysis) — OpenClaw-oriented stock workflows (ideas: `--fast`, dimensions, risk-style checks).
- [wbh604/UZI-Skill](https://github.com/wbh604/UZI-Skill) — Agent-heavy deep research (depth tiers, calibration discipline); not vendored here.

## Doc index

| Path | Purpose |
|------|---------|
| [USERFLOW.md](USERFLOW.md) | User-facing flows and CLI map |
| [MODULE_STRUCTURE.md](MODULE_STRUCTURE.md) | Modules, scripts, and dependencies |
| [docs/core/SKILL.md](docs/core/SKILL.md) | Mirror of root `SKILL.md` (agent / marketplace) |
| [docs/core/AGENTS.md](docs/core/AGENTS.md) | **Multi-tool hub** (Cursor, Claude Code, OpenClaw) |
| [docs/core/AGENT_GUIDE.md](docs/core/AGENT_GUIDE.md) | Agent orchestration and upstream pointers |
| [docs/database/SQLITE.md](docs/database/SQLITE.md) | SQLite schema and env vars |
| [docs/guides/PERSONA_ECOSYSTEM_GUIDE.md](docs/guides/PERSONA_ECOSYSTEM_GUIDE.md) | Persona registry, CLI, ensemble |
| [docs/guides/CHINESE_AUDIENCE_GUIDE.md](docs/guides/CHINESE_AUDIENCE_GUIDE.md) | zh-CN / zh-HK output |
| [docs/guides/](docs/guides/) | Strategies, scoring, quant notes, disclaimer |

## Tooling

- Tests: `scripts/run_tests.sh` or `pytest tests/unit tests/integration`
- Structure guard: `python setup/tools/check_structure.py`
- Optional: `pre-commit install` after configuring hooks (see repo `.pre-commit-config.yaml`)

## Pre-publish (ClawHub)

Before tagging or uploading the skill bundle:

1. Bump `version` in `pyproject.toml` and `tai_alpha/__init__.py` together.
2. Run `black .`, `isort .`, `flake8 tai_alpha tests scripts setup/tools`, `pytest tests/unit tests/integration`, and `python setup/tools/check_structure.py`.
3. Confirm `python -m build --wheel` succeeds; smoke `tai-alpha-analyze --help` (or `python scripts/analyze.py --help`).
4. Do not commit root scratch files (`data.json`, `backtest.json`, `_meta.json`, `test-prompts.json`); they are gitignored at repo root.

**Publish:** after `clawdhub login`, run `./setup/tools/clawdhub_publish.sh` (see [docs/deployment/CLAWDHUB_PUBLISH.md](docs/deployment/CLAWDHUB_PUBLISH.md)).

## Version

Package version is defined in `pyproject.toml` and `tai_alpha/__init__.py`.
