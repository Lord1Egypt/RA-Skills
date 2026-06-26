---
name: rednote_contacts
description: Run the installed red-crawler CLI for Xiaohongshu contact discovery. Requires the red-crawler command and Playwright browser runtime; not instruction-only.
homepage: https://github.com/Batxent/red-crawler
metadata: {"openclaw":{"runtime":"python","entry":"src/index.py","instructionOnly":false,"requiresBinaries":["red-crawler"],"requiresNetwork":true,"usesBrowserAutomation":true,"sensitiveLocalFiles":["Playwright storage state JSON"],"remoteRepositoryClone":false}}
---

# red-crawler-ops

Use this skill when you need to operate the installed `red-crawler` CLI from an OpenClaw workflow. It is the portable wrapper for the crawler runtime, not a separate crawler implementation.

## When To Use

Use `red-crawler-ops` for:

- preparing a local working directory for `red-crawler`
- crawling the default Xiaohongshu fashion homefeed
- saving a login session into Playwright storage state
- crawling a seed Xiaohongshu profile
- running nightly collection against a workspace database
- exporting a weekly report
- listing contactable creators from the SQLite database

## red-crawler CLI Commands

All crawling tasks must use the native `red-crawler` CLI commands:

### 1. crawl-homefeed (default)

Collect users from the Xiaohongshu fashion homefeed. This is the default crawl mode when `action` is omitted. It clicks card author links, not note links.

```bash
red-crawler crawl-homefeed \
  --homefeed-url "https://www.xiaohongshu.com/explore?channel_id=homefeed.fashion_v3" \
  --max-accounts 20 \
  --db-path "./data/red_crawler.db" \
  --output-dir "./output"
```

For IP rotation in local browser mode, provide `proxy` or `proxy_list` and set `rotation_mode: session`. The wrapper passes these through to `red-crawler`; after `403` or `429`, the crawler starts a new browser session using the next proxy. Each proxy maps deterministically to one browser header set, so the same outbound IP keeps the same `User-Agent`.

Bright Data Browser API mode does not use local proxy settings. Use `browser_mode: bright-data` plus `browser_auth` or `browser_endpoint`; if either value contains `{session}`, the crawler replaces it with a random session id for each browser session.

### 2. crawl-seed

Crawl a specific Xiaohongshu user profile and extract contact information.

```bash
red-crawler crawl-seed \
  --seed-url "https://www.xiaohongshu.com/user/profile/USER_ID" \
  --max-accounts 5 \
  --max-depth 2 \
  --db-path "./data/red_crawler.db" \
  --output-dir "./output"
```

**Parameters:**

- `--seed-url` (required): Target user profile URL
- `--storage-state`: Optional Playwright storage state file
- `--max-accounts`: Maximum accounts to crawl (default: 20)
- `--max-depth`: Crawl depth for related accounts (default: 2)
- `--include-note-recommendations`: Include note recommendations
- `--safe-mode`: Enable safe mode
- `--cache-dir`: Cache directory path
- `--cache-ttl-days`: Cache TTL in days (default: 7)
- `--db-path`: SQLite database path (default: ./data/red_crawler.db)
- `--output-dir`: Output directory (default: ./output)

**Outputs:**

- `accounts.csv`: Crawled account information
- `contact_leads.csv`: Extracted contact information (emails, etc.)
- `run_report.json`: Execution report

### 3. login

Optional interactive login to save browser session.

```bash
red-crawler login --save-state "./state.json"
```

**Parameters:**

- `--save-state` (required): Path to save storage state
- `--login-url`: Login page URL (default: https://www.xiaohongshu.com)

### 4. login-qr-start / login-qr-finish

QR code-based login for headless environments.

```bash
# Start QR login (generates QR code)
red-crawler login-qr-start \
  --save-state "./state.json" \
  --qr-path "./login-qr.png" \
  --session-path "./login-session.json" \
  --timeout 180

# Finish QR login after user scans
red-crawler login-qr-finish \
  --save-state "./state.json" \
  --session-path "./login-session.json"
```

### 5. collect-nightly

Run scheduled nightly data collection.

```bash
red-crawler collect-nightly \
  --db-path "./data/red_crawler.db" \
  --report-dir "./reports" \
  --crawl-budget 30 \
  --search-term-limit 4
```

**Parameters:**

- `--storage-state`: Optional storage state file
- `--db-path`: Database path (default: ./data/red_crawler.db)
- `--report-dir`: Report directory (default: ./reports)
- `--cache-dir`: Cache directory
- `--cache-ttl-days`: Cache TTL (default: 7)
- `--crawl-budget`: Crawl budget (default: 30)
- `--search-term-limit`: Search term limit (default: 4)
- `--startup-jitter-minutes`: Startup jitter
- `--slot-name`: Slot name for scheduling

### 6. report-weekly

Export weekly reports from database.

```bash
red-crawler report-weekly \
  --db-path "./data/red_crawler.db" \
  --report-dir "./reports" \
  --days 7
```

**Parameters:**

- `--db-path`: Database path (default: ./data/red_crawler.db)
- `--report-dir`: Report directory (default: ./reports)
- `--days`: Report period in days (default: 7)

**Outputs:**

- `weekly-growth-report.json`
- `contactable_creators.csv`

### 7. list-contactable

List contactable creators from database.

```bash
red-crawler list-contactable \
  --db-path "./data/red_crawler.db" \
  --lead-type "email" \
  --creator-segment "creator" \
  --min-relevance-score 0.5 \
  --limit 20 \
  --format csv
```

**Parameters:**

- `--db-path`: Database path (default: ./data/red_crawler.db)
- `--lead-type`: Lead type filter (default: email)
- `--creator-segment`: Creator segment filter (default: creator)
- `--min-relevance-score`: Minimum relevance score (default: 0.0)
- `--limit`: Result limit (default: 20)
- `--format`: Output format - table or csv (default: table)

### 8. open

Open Xiaohongshu in browser with saved session.

```bash
red-crawler open --storage-state "./state.json"
```

## Supported Actions

- `bootstrap`
- `crawl_homefeed` (default when omitted)
- `crawl_seed`
- `login`
- `collect_nightly`
- `report_weekly`
- `list_contactable`
- `job_status`
- `job_logs`
- `job_stop`
- `ack_event`

## Long Running Crawls and Heartbeat

For long crawl actions, set `run_mode: background`. The skill starts a local background wrapper, returns a `job_id` immediately, and writes OpenClaw-readable state under `heartbeat_dir` (default `./.openclaw/red-crawler`).

Background jobs write:

- `HEARTBEAT.md`: concise status and pending user updates for OpenClaw heartbeat polling
- `jobs/<job_id>.json`: machine-readable job state
- `events/<job_id>.jsonl`: completion or failure events
- `logs/jobs/<job_id>.out.log` and `.err.log`: crawler logs

Use `job_status` with the returned `job_id` to read the latest state manually. Use `job_logs` to inspect recent output and `job_stop` to request termination. If OpenClaw heartbeat polling is enabled, the agent can read `HEARTBEAT.md` and surface pending completion events to the user on a later heartbeat cycle. After surfacing an event, call `ack_event` with the `event_id` so the same update is not reported again.

## Example Prompts

- "帮我准备当前小红书爬虫项目的本地环境" (Automatically maps to `bootstrap` for an existing workspace)
- "开始爬小红书彩妆博主" / "帮我抓取一批小红书博主" (Defaults to `crawl_homefeed`)
- "我需要登录爬虫" / "我要登录小红书" (Automatically maps to `login` to fetch/refresh the Playwright session state)
- "开始执行每日夜间数据采集" / "运行自动收集任务" (Automatically maps to `collect_nightly` to continue crawling based on the database queue)
- "帮我生成一份本周的爬虫数据周报" (Automatically maps to `report_weekly` pointing to the workspace's DB)

**Crawling New Data vs Querying Database:**

- "帮我从这个博主去爬10个相关的美妆博主: https://www.xiaohongshu.com/..." (Crawls **NEW** data: Automatically maps to `crawl_seed` with `seed_url`, setting `max_accounts` to 10. _Note: crawling new data requires a seed URL._)
- "帮我从数据库/已爬取的数据中找出10个美妆/游戏/科技博主的联系方式" (Queries **EXISTING** DB: Automatically sets `action` to `list_contactable`, `limit` to 10, and `creator_segment` to "美妆" to filter the local SQLite database)

_(Also understands technical prompt variations:)_

- "Bootstrap this workspace with `install_browser: true` after I have installed the CLI."
- "Crawl this seed profile with a depth of 2 and write outputs into `output/`."
- "Export this week's report and return the generated artifacts."

## Environment Setup

### Windows (WSL2)

On Windows, red-crawler runs inside WSL2. You need:

1. **WSL2 with Ubuntu** (20.04 or 22.04 recommended)
2. **WSLg** (built-in graphics support for WSL2) - for browser GUI
3. **Dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y git python3 python3-pip
   ```
4. **red-crawler CLI**, installed from the published package.

**Known Issues & Fixes:**

1. **DISPLAY not set (WSLg)**
   - Error: `Missing X server or $DISPLAY`
   - Fix: Export DISPLAY before running:
     ```bash
     export DISPLAY=:0
     ```

2. **Headless vs Headed browser**
   - `login` command requires headed browser (GUI)
   - `crawl-seed` and other commands also require headed browser on WSL
   - Always set `DISPLAY=:0` before running any command with browser

### Linux (Native)

1. **Dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y git python3 python3-pip
   ```
2. **red-crawler CLI**, installed from the published package.
3. **X Server** (for headed browser):
   ```bash
   sudo apt-get install -y xvfb
   export DISPLAY=:99
   Xvfb :99 -screen 0 1024x768x16 &
   ```

### macOS

1. **red-crawler CLI:**
   ```bash
   uv tool install red-crawler==0.1.3
   ```
2. **Playwright browser runtime:** run `bootstrap` with `install_browser: true`.

## Prerequisites

- This skill never clones a repository. Install `red-crawler` as a package, then point `workspace_path` at a local working directory.
- Set `require_local_checkout: true` only when you intentionally want to run from a source checkout.
- `uv` is only required when `sync_dependencies: true` is used for a local source checkout.
- `bootstrap` does not create a login session. Use `login` explicitly.
- `login` creates an optional Playwright storage state explicitly.
- `crawl_seed`, `crawl_homefeed`, and `collect_nightly` can run without a storage state file.
- `report_weekly` and `list_contactable` run from the database and do not require storage state.
- The workspace must contain `pyproject.toml`.

## Safety Limits

- Do not point this skill at a directory you do not control.
- Do not create login sessions silently; call `login` only when the user asks to authenticate.
- Keep the Playwright storage state file local and out of commits, logs, and shared artifacts.
- Do not point it at production data or unknown databases.
- Do not create or require `state.json` unless the user explicitly asks to authenticate.
- Do not hard-code machine-specific paths in prompts or config.
- Prefer relative, workspace-scoped paths for outputs and reports.

## Input Shape

Provide an object with `action` plus optional fields used by the selected action. Common fields include:

- `workspace_path`
- `require_local_checkout`
- `runner_command`
- `storage_state`
- `db_path`
- `report_dir`
- `output_dir`
- `cache_dir`
- `heartbeat_dir`
- `job_log_dir`
- `run_mode` (`sync`/`background`)
- `job_id`
- `event_id`
- `tail_lines`

Action-specific fields include:

- `sync_dependencies`
- `install_browser`
- `seed_url`
- `login_url`
- `max_accounts`
- `max_depth`
- `include_note_recommendations`
- `safe_mode`
- `cache_ttl_days`
- `gender_filter` (`male`/`female` or `男`/`女`)
- `crawl_budget`
- `search_term_limit`
- `startup_jitter_minutes`
- `slot_name`
- `days`
- `lead_type`
- `creator_segment`
- `min_relevance_score`
- `limit`
- `format`
- `browser_mode`
- `browser_endpoint`
- `browser_auth`
- `proxy`
- `proxy_list`
- `rotation_mode` (`none`/`session`)
- `rotation_retries`
- `randomize_headers`

## Output Shape

Successful runs return:

- `status`
- `action`
- `command`
- `summary`
- `artifacts`
- `metrics`
- `next_step`
- `stdout`
- `stderr`
- `job_id` and `pid` when `run_mode: background` accepts a job
- `job` for job status actions

Error runs return:

- `status`
- `action`
- `error_type`
- `message`
- `suggested_fix`
- `action`, `command`, `stdout`, and `stderr` for execution-time failures
- Early validation or configuration failures may omit `action`, `command`, `stdout`, and `stderr`
