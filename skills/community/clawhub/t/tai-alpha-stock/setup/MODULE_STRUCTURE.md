# Module structure

## Layout

```
tai-alpha-stock/
├── tai_alpha/              # Library package (importable)
├── scripts/                # Thin CLI wrappers (sys.path bootstrap + entrypoints)
├── tests/                  # unit, integration, live
├── setup/                  # All project Markdown, SQL, and structure tools
│   ├── docs/
│   │   └── deployment/     # CLAWDHUB_PUBLISH.md — ClawdHub CLI publish steps
│   ├── sql/
│   └── tools/              # check_structure.py, clawdhub_publish.sh
├── tai_alpha_output/       # Default DB directory (gitignored)
├── SKILL.md                # Agent marketplace entry (required at repo root for tooling)
├── .clawdhubignore         # Extra paths omitted from ClawdHub publish (e.g. tests/)
├── .flake8                 # Lint: 88 columns (Black), E402 ignored for scripts/ path bootstrap
└── pyproject.toml
```

## Package: `tai_alpha`

| Module | Role |
|--------|------|
| `storage_sqlite.py` | SQLite path, schema bootstrap, run + watchlist CRUD |
| `collect.py` | yfinance fetch; `collect_ticker` / `collect_ticker_routed` persist `collect_json` |
| `market_router.py` | US/HK/CN detection + Yahoo symbol normalization |
| `data_adapters/` | Yahoo adapter + `adapter_meta` provenance |
| `persona_registry.py` / `persona_engine.py` | Persona YAML + overlays / ensemble |
| `localize.py` | zh-CN/zh-HK signal labels + disclaimer |
| `backtest_engine.py` | VectorBT; `run_backtest(db_path, run_id, ...)` |
| `score_engine.py` | Conviction / signal; CLI `--db-path` + `--run-id` |
| `report_text.py` | Human-readable report; CLI `--db-path` + `--run-id` |
| `pipeline.py` | End-to-end `run_analyze(ticker, db_path)` |
| `ml_predict.py` | `predict_7d_return_from_collect` |
| `portfolio_sim.py` | Multi-ticker sim via temp DBs |
| `sector_analysis.py` | Ticker vs sector ETF |
| `alerts_store.py` | Watchlist in SQLite |
| `schema.py` | Normalization helpers |
| `yfinance_utils.py` | Series helpers |
| `runtime_paths.py` | `find_project_root`, `default_output_dir`, `ensure_output_dir` |
| `config_load.py` | Load `setup/config/score_dimensions.yaml` and `risk_keywords.json` (bundled fallback under `tai_alpha/config/`) |
| `risk_flags.py` | Structured `risk_flags` from collect fields + headline keyword scans |
| `dividends.py` | yfinance dividend summary CLI (`tai-alpha-dividends`) |
| `hot_scanner.py` | Yahoo movers + optional CoinGecko (`tai-alpha-hot-scanner`) |
| `script_entrypoints.py` | Argparse + shared CLI for analyze, custom, ml, multi_backtest, batch, cron |

## Config (calibration)

- `setup/config/score_dimensions.yaml` — conviction weights / thresholds (loaded by `score_engine`).
- `setup/config/risk_keywords.json` — crisis / geopolitical strings for `risk_flags`.
- `setup/config/personas/` — `PERSONA_REGISTRY.yaml` + per-persona YAML overlays.
- `setup/config/sources/SOURCES.yaml` — data-source policy (Yahoo primary; extensible).
- `setup/config/i18n_glossary_zh.json` — Chinese signal / label glossary.

## Scripts

All scripts under `scripts/` add the repo root to `sys.path` and delegate to `tai_alpha` (library `main` or `script_entrypoints`). Additional thin CLIs: `dividends.py`, `hot_scanner.py`.

## Documentation policy

- **Operational mirror:** root `SKILL.md` is kept for OpenClaw / marketplace tooling.
- **Agent stubs (root):** `AGENTS.md`, `CLAUDE.md` — thin pointers to [docs/core/AGENTS.md](docs/core/AGENTS.md) (Cursor, Claude Code, shared conventions).
- **Canonical copy:** [docs/core/SKILL.md](docs/core/SKILL.md) mirrors skill content under `/setup`.
- **Cursor rules:** [.cursor/rules/tai-alpha-stock.mdc](../.cursor/rules/tai-alpha-stock.mdc) (`alwaysApply`).
- Do not add new `.md` outside `/setup` except root `SKILL.md`, `AGENTS.md`, `CLAUDE.md` (enforced by `setup/tools/check_structure.py`).

## SQL

- Consolidated schema: [sql/schema/tai_alpha_schema_consolidated.sql](sql/schema/tai_alpha_schema_consolidated.sql)
- Archive: `setup/sql/archive/`.
