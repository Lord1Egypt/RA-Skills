# API reference

## Library

Import from the `tai_alpha` package after install (`pip install -e .`):

- `collect_ticker(ticker, db_path)` — fetch and persist `collect_json` (returns `(data, run_id)`)
- `run_backtest(db_path, run_id, strategy=...)` — VectorBT backtest; updates `backtest_json`
- `score_data(data, ml_pred=None)` — score dict (in-memory)
- `run_analyze(ticker, db_path=None, ...)` — full pipeline
- `default_db_path()` — SQLite path (`TAI_ALPHA_DB_PATH` or `default_output_dir()/tai_alpha.db`)

## CLI

See [USERFLOW.md](../../USERFLOW.md) and root `scripts/*.py` — thin wrappers. Most commands accept `--db-path` and stepwise tools require `--run-id`.

## External data

Market data via **yfinance** (network). Live tests are opt-in (`pytest --live`).
