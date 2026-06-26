---
name: qc-backtest-master
description: QuantConnect automated backtest pipeline — submit local strategies, compile, execute, monitor with early-stop, and download results in one command.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - QC_USER_ID
        - QC_API_TOKEN
        - QC_PROJECT_ID
      bins:
        - python3
    primaryEnv: QC_API_TOKEN
    emoji: "\U0001F680"
---

# QC Backtest Master

Automate the full QuantConnect backtest lifecycle from local code to cloud results, without ever opening the web UI.

## What this skill does

When the user asks to backtest a strategy, run a backtest, or submit code to QuantConnect, follow this workflow:

### 1. Submit & Compile

Upload the user's local `.py` strategy file to a QuantConnect cloud project, replacing any existing `main.py`. Trigger compilation and report any errors with line numbers.

```bash
python3 submit_backtest.py \
  --main-file <path_to_strategy.py> \
  --name "<backtest_name>" \
  --project-id $QC_PROJECT_ID
```

If the strategy has auxiliary data files (`.json`, `.txt`, `.csv`), upload those too.

### 2. Monitor with Early-Stop

Poll backtest progress in real time. If drawdown exceeds the user's threshold after 20% progress, automatically delete the backtest to save compute time.

```bash
python3 monitor_backtest.py <backtest_id> \
  --max-dd <threshold> \
  --check-after-progress 0.20 \
  --timeout 3600
```

**Exit codes:**

| Code | Meaning |
|------|---------|
| `0` | Backtest completed normally |
| `1` | Runtime error (print full stack trace) |
| `2` | Timeout |
| `3` | Early stop: drawdown exceeded threshold, backtest deleted |

### 3. Download Results

Fetch the complete backtest statistics (JSON) and all order records (CSV, paginated at 100 per call to bypass QC's limit).

```bash
python3 get_results.py <backtest_id> --output-dir ./results/<name>
```

**Output files:**
- `<backtest_id>_result.json` — Full statistics, charts, runtime data
- `<backtest_id>_orders.csv` — All orders with symbol, direction, quantity, fill price, fees, timestamps

### 4. Full Pipeline (One Command)

Run the entire submit-compile-monitor-download pipeline:

```bash
python3 run_workflow.py \
  --main-file <path_to_strategy.py> \
  --name "<backtest_name>" \
  --max-dd 40
```

### 5. List Historical Backtests

```bash
python3 list_backtests.py --limit 10
```

## QC API Client

The `qc_api/client.py` module wraps the QuantConnect REST API v2:

- `create_backtest(project_id, name, compile_id)` — Start a backtest
- `read_backtest(project_id, backtest_id)` — Get status and results
- `read_backtest_orders(project_id, backtest_id, start, end)` — Paginated order fetch
- `delete_backtest(project_id, backtest_id)` — Delete (used for early-stop)
- `update_project_file(project_id, name, content)` — Upload code
- `compile_project(project_id)` — Trigger compilation

Credentials are read from environment variables `QC_USER_ID` and `QC_API_TOKEN`.

## Rules

- **Entry file**: Local strategy files are uploaded as `main.py`. Old `Main.py` is auto-deleted to prevent conflicts. Do not manually rename files on the QC cloud project.
- **One backtest at a time**: QC free tier allows only 1 concurrent backtest per project. Never submit a second backtest while one is running — it will silently fail or queue.
- **Logs are not available via API**: QC REST API v2 does not expose `self.log()` output. View logs in the QC web UI manually.
- **Early-stop threshold**: Accepts both fraction (`0.40`) and percentage (`40`) formats. Early-stop **permanently deletes** the backtest — it cannot be recovered.
- **Environment variables `QC_USER_ID`, `QC_API_TOKEN`, and `QC_PROJECT_ID` must be set.** The skill will raise a clear error if any are missing.
- **Do not modify cloud project files outside this skill.** The skill assumes it owns `main.py` and will overwrite any manual changes on the next submission.
