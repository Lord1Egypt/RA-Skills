---
name: workflow-migrate
description: Migrate N8N/Zapier/Make workflows to production-grade Python or Node.js scripts. Given a workflow description or paste, rewrites automation logic with retry, backoff, logging, and self-healing. Billable migration deliverable.
argument-hint: [workflow description, or paste workflow JSON/steps, or type "paste" to describe inline]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch
---

# Workflow Migrate — Automation Migration Tool

## Why This Exists
N8N/Zapier/Make workflows break silently, can't be version-controlled, and cost $50-500/month in SaaS fees. This skill rewrites them as standalone scripts that run forever with zero subscription cost. Each migration is a $500-5000 billable deliverable.

## Trigger
Use when: "migrate this workflow", "convert N8N to Python", "rewrite my Zapier", "turn this automation into a script", "get off N8N"

Invoked as: `/workflow-migrate [workflow description or paste]`

---

## Process

### Step 1: Parse the Workflow Input

From `$ARGUMENTS`:
- If it's a description ("when a form is submitted, send email and update Airtable"): parse directly
- If it's N8N JSON: read and extract nodes/connections
- If it's Zapier steps: parse the trigger + action chain
- If it's Make (formerly Integromat) scenario: parse modules

Extract and document:

**Triggers:**
- Webhook (POST endpoint)
- Cron/schedule (every X minutes/hours)
- Form submission
- Email received
- File drop (S3, Google Drive, local folder)
- DB row created/updated

**Actions:**
- HTTP/API calls (list each endpoint, method, payload)
- Database reads/writes
- Email sends
- File operations
- Conditional logic (if/else branches)
- Loops over arrays
- Data transformations

**Data flow:**
- Input payload fields used
- Intermediate computed values
- Output destinations

If the workflow description is too vague, ask 2-3 targeted questions before proceeding:
- "What triggers it — webhook, schedule, or something else?"
- "Which API endpoints does it call and with what data?"
- "What counts as success? What should happen on failure?"

---

### Step 2: Choose Language

**Default to Python** unless:
- The workflow is heavily async/event-driven (prefer Node.js)
- Existing codebase is Node.js
- Kevin explicitly requests Node

Python stack: `requests`, `schedule`, `logging`, `tenacity` (retry), `python-dotenv`
Node.js stack: `axios`, `node-cron`, `winston`, `async-retry`, `dotenv`

---

### Step 3: Write the Script

Generate a complete, runnable script. Required elements:

#### Python Template Structure:
```python
#!/usr/bin/env python3
"""
[Workflow Name] — Migrated from [N8N/Zapier/Make]
Original: [brief description of what the workflow did]
Migrated: [date]

Usage:
  python workflow_[name].py                    # run once
  python workflow_[name].py --schedule         # run on schedule
  python workflow_[name].py --dry-run          # test without side effects
"""

import os
import sys
import logging
import time
import argparse
from datetime import datetime
from typing import Optional, Dict, Any

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv

load_dotenv()

# ─── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"logs/workflow_{datetime.now().strftime('%Y%m')}.log"),
    ]
)
log = logging.getLogger(__name__)

# ─── Config ────────────────────────────────────────────────────────────────────
API_KEY = os.getenv("API_KEY")         # from .env
WEBHOOK_URL = os.getenv("WEBHOOK_URL") # destination
DRY_RUN = False

# ─── Retry Decorator ───────────────────────────────────────────────────────────
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((requests.RequestException, ConnectionError)),
    before_sleep=lambda rs: log.warning(f"Retrying (attempt {rs.attempt_number})..."),
    reraise=True
)
def api_call(method: str, url: str, **kwargs) -> Dict[str, Any]:
    """Make an HTTP call with automatic retry and exponential backoff."""
    if DRY_RUN:
        log.info(f"[DRY RUN] {method.upper()} {url} payload={kwargs.get('json', {})}")
        return {"dry_run": True}
    resp = requests.request(method, url, timeout=30, **kwargs)
    resp.raise_for_status()
    return resp.json()
```

#### Node.js Template Structure:
```javascript
#!/usr/bin/env node
/**
 * [Workflow Name] — Migrated from [N8N/Zapier/Make]
 * Original: [brief description]
 * Migrated: [date]
 *
 * Usage:
 *   node workflow_[name].js            # run once
 *   node workflow_[name].js --schedule # run on schedule
 *   node workflow_[name].js --dry-run  # test without side effects
 */

require('dotenv').config();
const axios = require('axios');
const retry = require('async-retry');
const cron = require('node-cron');
const winston = require('winston');
const fs = require('fs');

// ─── Logger ────────────────────────────────────────────────────────────────────
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(winston.format.timestamp(), winston.format.json()),
  transports: [
    new winston.transports.Console({ format: winston.format.simple() }),
    new winston.transports.File({ filename: `logs/workflow_${new Date().toISOString().slice(0,7)}.log` }),
  ],
});

// ─── Config ────────────────────────────────────────────────────────────────────
const API_KEY = process.env.API_KEY;
const DRY_RUN = process.argv.includes('--dry-run');

// ─── Retry Wrapper ─────────────────────────────────────────────────────────────
async function apiCall(method, url, data = {}, headers = {}) {
  return retry(async (bail, attempt) => {
    if (DRY_RUN) {
      logger.info(`[DRY RUN] ${method.toUpperCase()} ${url}`, { data });
      return { dry_run: true };
    }
    try {
      const resp = await axios({ method, url, data, headers, timeout: 30000 });
      return resp.data;
    } catch (err) {
      if (err.response && err.response.status < 500) bail(err); // 4xx = don't retry
      logger.warn(`Retrying attempt ${attempt}...`, { error: err.message });
      throw err;
    }
  }, { retries: 3, minTimeout: 2000, maxTimeout: 30000, factor: 2 });
}
```

**For each action in the workflow, write a dedicated function:**
- One function per logical action (e.g., `fetch_leads()`, `send_notification()`, `update_database()`)
- Functions are composable and testable in isolation
- Every function logs what it's doing: start, result, any errors

**Main orchestrator:**
```python
def run(dry_run: bool = False):
    global DRY_RUN
    DRY_RUN = dry_run
    log.info("=== Workflow started ===")
    try:
        # Step 1: [action name]
        data = fetch_source_data()
        log.info(f"Fetched {len(data)} records")

        # Step 2: [action name]
        for item in data:
            result = process_item(item)
            if result:
                send_to_destination(result)

        log.info("=== Workflow completed successfully ===")
    except Exception as e:
        log.error(f"Workflow failed: {e}", exc_info=True)
        send_alert(f"Workflow [name] failed: {e}")  # self-healing alert
        raise
```

**Self-healing patterns to include:**
- Alert on failure (Telegram message via Kevin's bot token if available, else log to file)
- Idempotency: skip already-processed records (use a state file or DB flag)
- Dead-letter queue: failed items saved to `failed_[date].json` for manual review
- Heartbeat: log "still alive" every N runs for scheduled workflows

---

### Step 4: Generate .env.example

```bash
# [Workflow Name] — Environment Variables
# Copy to .env and fill in values

API_KEY=your_api_key_here
WEBHOOK_URL=https://...
DATABASE_URL=...

# Optional: Telegram alerts on failure
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=8062428674
```

---

### Step 5: Generate requirements.txt or package.json

**Python:**
```
requests>=2.31.0
tenacity>=8.2.0
python-dotenv>=1.0.0
schedule>=1.2.0  # only if cron-triggered
```

**Node.js:**
```json
{
  "dependencies": {
    "axios": "^1.6.0",
    "async-retry": "^1.3.3",
    "node-cron": "^3.0.3",
    "winston": "^3.11.0",
    "dotenv": "^16.3.1"
  }
}
```

---

### Step 6: If the Workflow is Recurring — Generate a SKILL.md

If the workflow runs on a schedule or will be reused:
- Generate a `SKILL.md` in the same output directory
- Name it after the workflow function
- Description: "Run [workflow name] — [what it does in 10 words]"
- Instructions: path to script, how to run it, what env vars are needed

---

### Step 7: Save Outputs and Print Migration Summary

**Output location:** Ask Kevin where to save, default to `./workflow_[name]/`

Create:
- `workflow_[name].py` (or `.js`)
- `.env.example`
- `requirements.txt` (or `package.json`)
- `SKILL.md` (if recurring)
- `README.md` (quick usage guide — 20 lines max)

**Print migration summary:**
```
Migration complete.

Original: [N8N/Zapier/Make] workflow — [X] nodes/steps
Output:   ./workflow_[name]/workflow_[name].py

What changed:
  - [X] N8N nodes → [Y] lines of Python
  - Added: retry with exponential backoff (3 attempts, 2s-30s)
  - Added: rotating log file (monthly)
  - Added: dry-run mode (--dry-run flag)
  - Added: failure alerts via [Telegram/log]
  - Removed: $XX/month SaaS subscription

To run:
  cd workflow_[name]/
  cp .env.example .env   # fill in your keys
  pip install -r requirements.txt
  python workflow_[name].py --dry-run   # test first
  python workflow_[name].py             # run for real
```

---

## Error Handling

- **Ambiguous workflow**: ask 2-3 targeted questions, don't guess at API endpoints
- **Proprietary N8N nodes** (e.g., OpenAI node): rewrite using the raw API — include API docs link in comments
- **Very complex workflow (>15 nodes)**: break into multiple scripts with a coordinator, document the dependency order
- **No credentials visible**: generate .env.example with clear placeholders, add comments explaining where each key comes from
- **Webhook trigger**: generate a Flask/Express endpoint stub that receives the webhook and calls the workflow function

## Notes
- Always test with `--dry-run` before running for real
- State file for idempotency: `./state/processed_ids.json` — create `state/` dir if it doesn't exist
- For scheduled runs, prefer `cron` / `schedule` over external task runners (fewer dependencies)
