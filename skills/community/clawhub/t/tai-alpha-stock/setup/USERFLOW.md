# User flow — Tai Alpha Stock

Default database: **`tai_alpha_output/tai_alpha.db`** (or `TAI_ALPHA_DB_PATH`). The output directory (`TAI_ALPHA_OUTPUT_DIR` / `tai_alpha_output/`) holds that file by default.

## Flow A — Full analyze (most common)

1. User runs `python scripts/analyze.py TICKER` (optional `--strategy`, `--rsi-low`, `--rsi-high`, `--no-report`, `--db-path`).
2. Optional speed / depth: `--fast` (skip ML, lighter collect) and `--depth lite|standard|deep` (`lite` = fast collect + no ML; `deep` = full run + geopolitical `risk_flags` unless `--fast`).
3. Optional **personas**: `--persona value_seeker` (comma-separated) or `--persona-all`; **market** `--market auto|us|hk|cn`; **Chinese report** `--lang zh-CN` or `zh-HK`.
4. Pipeline inserts a **run** row and stores `collect_json`, `backtest_json`, `score_json`, optional `ml_json`, optional `persona_json` and `meta_json` in SQLite.
5. User reads stdout report or inspects the DB (see [docs/database/SQLITE.md](docs/database/SQLITE.md)).

## Flow B — Stepwise

1. `python scripts/collect.py TICKER [--db-path PATH]` — new run with `collect_json`.
2. `python scripts/backtest.py --run-id N [--db-path PATH]` — fills `backtest_json` for that run.
3. `python scripts/score.py --run-id N [--db-path PATH]` — prints score JSON (uses `collect_json` and optional `ml_json`); add `--deep-risk` for geopolitical keyword tier in `risk_flags`.
4. `python scripts/report.py --run-id N [--db-path PATH]` — formatted text.

## Flow C — Batch / cron

- `python scripts/batch.py TICKER1 TICKER2` — runs analyze per ticker; optional `--fast`, `--depth`; reads latest `score_json` for each ticker from the shared DB.
- `python scripts/cron.py` — uses `TAI_ALPHA_HOTLIST` and optional `TAI_ALPHA_TELEGRAM_WEBHOOK`.

## Flow D — Portfolio / sector / ML / dividends / movers

- `python scripts/portfolio.py` — equal-weight simulation (temp SQLite DB per ticker).
- `python scripts/sector.py TICKER [ETF]` — sector ETF alpha proxy (no DB).
- `python scripts/ml.py TICKER` — collect + ML; stores `ml_json` on the run row.
- `python scripts/dividends.py TICKER` — dividend summary (yfinance).
- `python scripts/hot_scanner.py` — Yahoo movers; `--with-crypto` for CoinGecko trending.

## Flow E — Alerts

- `python scripts/alerts.py list|add|check [--db-path PATH]` — `watchlist` table in the same SQLite file (default DB as above).

## Disclaimer

Not financial advice — see [docs/guides/DISCLAIMER_AND_LIMITATIONS.md](docs/guides/DISCLAIMER_AND_LIMITATIONS.md).

See [MODULE_STRUCTURE.md](MODULE_STRUCTURE.md) and [docs/guides/STRATEGIES.md](docs/guides/STRATEGIES.md).
