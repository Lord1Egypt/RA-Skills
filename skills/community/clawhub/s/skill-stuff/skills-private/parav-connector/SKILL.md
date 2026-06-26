---
name: parav-connector
description: Connects OpenClaw to a parav instance for cloud browser execution, long-running agent tasks, and credit management. Use when a skill needs headless browsing that runs while the laptop is closed, or heavy reasoning tasks that should not block the local machine.
license: MIT
compatibility: Requires parav instance running (mcp-gateway on port 3000). See parav setup instructions.
metadata:
  openclaw.emoji: "⚡"
  openclaw.user-invocable: "true"
  openclaw.category: infrastructure
  openclaw.tags: "parav,cloud,browser,agents,credits,compute,headless,stealth,long-running"
  openclaw.triggers: "parav,cloud browser,run overnight,cloud agent,out of credits,parav status,check my balance,enable cloud mode"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/parav-connector


# Parav Connector

Connects OpenClaw to your parav instance.

Three things it does:
1. Routes browser calls to parav's cloud headless Chrome (instead of local)
2. Dispatches long reasoning tasks to parav's Graph engine (runs overnight)
3. Manages your credit balance (Stripe-funded, deducted per task)

---

## File structure

```
parav-connector/
  SKILL.md
  config.md          ← parav endpoint, API key, credit settings
  jobs.md            ← active and completed job log
  sessions.md        ← authenticated platform sessions in parav vault
```

---

## Setup

### Step 1 — Parav instance

You need a running parav instance. Either:
- Local: `cargo run -p mcp-gateway` (port 3000)
- Hosted: your production parav URL

### Step 2 — Get an API key

```bash
# Add yourself as a tenant via parav CLI
cargo run -p parav-cli -- provider add openclaw http://localhost:3000 1000

# Top up initial balance (credits, not ADA yet)
cargo run -p parav-cli -- user top-up [your-user-id] 5000
```

### Step 3 — Write config.md

```md
# Parav Connector Config

## Connection
endpoint: [http://localhost:3000 or https://your-parav.com]
api_key: [stored in OpenClaw secrets — never in this file]
tenant_id: [your tenant ID]

## Credit settings
low_balance_alert: 500    ← alert when balance drops below this
monthly_budget: 10000     ← hard cap (optional)
currency_display: EUR     ← for balance display

## Execution modes
mcp_browse: true          ← route stealth_browse calls to parav
dag_tasks: true           ← enable DAG task submission
graph_tasks: true         ← enable Graph engine tasks

## Fallback
local_fallback: true      ← fall back to local if parav unavailable

## Stale job detection
stuck_running_threshold: 10  ← minutes before flagging stale DAG jobs
```

### Step 4 — Register as MCP provider in OpenClaw

Add to your OpenClaw config (openclaw.json):

```json
{
  "mcp": {
    "servers": {
      "parav": {
        "url": "http://localhost:3000/mcp",
        "headers": {
          "Authorization": "Bearer ${PARAV_API_KEY}"
        }
      }
    }
  }
}
```

After this, `stealth_browse` is immediately available as a tool to any skill.

### Step 5 — Register heartbeat cron

Monitors active jobs and catches stale state:

```json
{
  "name": "Parav Connector — Heartbeat",
  "schedule": { "kind": "cron", "expr": "*/10 * * * *", "tz": "<TZ>" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run parav-connector heartbeat. Read {baseDir}/config.md and {baseDir}/jobs.md. Poll parav for status of all running jobs. Flag any DAG jobs stuck in Running for over threshold minutes. Collect completed Graph jobs. Update jobs.md. Alert if balance below low_balance threshold. Exit silently if nothing to report.",
    "lightContext": true
  }
}
```

---

## Three execution paths

### Path 1 — MCP stealth browse (synchronous, fastest)

For single-page tasks: extract data, check a price, read a page.
Available to any skill immediately after setup — no special dispatch needed.

The skill calls `stealth_browse` as a tool. Parav executes in the cloud.
Returns `TaskReceipt.final_value` — the extracted content.

```
Skill calls: stealth_browse(url, instruction)
Parav runs:  Navigate → Extract → Semantic → Hash
Returns:     extracted content (string)
Receipt:     GET /receipt/:task_id (SHA-256 + Ed25519 signed)
```

**Credits:** ~10-50 per call depending on page complexity.

---

### Path 2 — DAG task (browser automation, multi-step)

For tasks that need navigation, form filling, or multi-page flows.
Submitted as a `TaskIntent`. Executed asynchronously.

```
POST /v1/tasks (or direct dag_queue insert)
Body: {
  "instruction": "Log in to LinkedIn and post the following content: [content]",
  "target_url": "https://linkedin.com",
  "tenant_id": "[tenant]",
  "priority": 1
}
Response: { "task_id": "uuid" }

Poll: GET /v1/tasks/:id/stream (SSE)
Phases: Planning → Navigating → Extracting → Synthesizing → Completed

Result: GET /receipt/:task_id
```

**Credits:** ~100-500 per task depending on steps.

**Submitting a DAG task from OpenClaw:**

`/parav dag [instruction] [url]`

Or skills submit automatically when `dag_mode: true` in their config.

---

### Path 3 — Graph task (long reasoning, overnight)

For tasks that take minutes or hours of LLM reasoning.
Submitted to masumi-serve's Graph engine. Runs asynchronously.

```
POST masumi-serve /api (rspc start_run)
Body: { "instruction": "[full task prompt with all context]" }
Response: { "thread_id": "uuid" }

Stream: GET /api/stream/:thread_id (SSE)
Phases: GraphState transitions, ReasonerNode outputs

Result: final message in SSE stream
```

**Payment gate:**
If the task hits a `PaymentNode`, it yields waiting for payment confirmation.
Current parav state: payment gate is mock (approve_run with any string).
When Cardano is wired: parav-connector handles the `approve_run` call
automatically after on-chain confirmation.

**Credits:** ~500-5000 per task depending on depth and LLM calls.

**Submitting a Graph task from OpenClaw:**

`/parav graph [instruction]`

Or skills submit automatically when `remote_mode: parav_graph` in their config.

---

## What parav does NOT handle

**Never route these through parav:**
- LinkedIn posting
- Reddit posting  
- Instagram posting
- Twitter/X posting
- Any platform where the user's own authenticated browser session matters

These go through **lobstrkit Exine** — the user's actual Chrome session.
Lobstrkit sits on the user's machine, uses their browser, their IP, their
existing session history. Platforms cannot distinguish it from manual use.

Parav-stealth (cloud VPS + headless Chrome) is appropriate for:
- Research on public pages
- Monitoring public URLs
- Invoice OCR
- Platforms without aggressive bot detection

If a skill tries to route LinkedIn/Reddit/Instagram/Twitter posting through
parav-connector, the connector refuses and redirects to lobstrkit.

---

## Session vault — solving the cookie problem (for parav-appropriate platforms)

Parav has a built-in OAuth vault (`oauth_vault` table, tenant-isolated).
Platform sessions are stored in parav per tenant, not in OpenClaw.

**Register a platform session:**

```bash
# Via parav CLI (one-time setup per platform)
cargo run -p parav-cli -- user add-token [tenant] linkedin [session-token]
cargo run -p parav-cli -- user add-token [tenant] reddit [session-token]
cargo run -p parav-cli -- user add-token [tenant] datev [session-token]
```

Or via parav's OAuth flow:
```
GET /v1/auth/login/linkedin → redirect to LinkedIn OAuth
GET /v1/auth/callback/linkedin → stores token in vault
```

After this, DAG tasks for LinkedIn, Reddit, DATEV automatically use the
stored session. No cookies in OpenClaw. No cookies in transit.

**Track which sessions are active:**

```md
# Sessions (sessions.md)

## linkedin
Status: active
Added: [date]
Last used: [date]

## reddit
Status: active

## datev
Status: active

## instagram
Status: not configured
```

`/parav sessions` — show current vault status.

---

## Job tracking

Every task submitted gets logged in jobs.md:

```md
# Jobs

## [JOB-ID]
Path: mcp | dag | graph
Engine: stealth_browse | dag | masumi-serve
Task: [brief description]
Submitted: [ISO timestamp]
Status: submitted | running | completed | failed | stale
task_id: [parav task ID for DAG] or thread_id [for Graph]
Result: [null until complete]
Receipt: [TaskReceipt receipt_id if DAG]
Credits_used: [amount]
Skill: [which skill submitted this job]
Follow_up: [what to do with result — deliver/post/store/none]
```

---

## Stale job detection

Known gap in parav: DAG jobs have no watchdog. If parav crashes
mid-execution, the job stays `Running` forever.

The heartbeat cron handles this:
- Every 10 minutes, check all `running` jobs
- If a DAG job has been `Running` for > threshold (default 10 min):
  Flag as `stale` in jobs.md
  Alert user: "DAG task [X] appears stuck (running 15 min). Retry?"
  `/parav retry [job-id]` — resubmit with same input

Graph jobs have proper checkpointing — they can resume from last checkpoint.
DAG jobs should be idempotent by design (same URL + instruction = same result).

---

## Credit management

`/parav balance` — current credit balance

```
⚡ Parav balance

Credits: 3,420 (≈ €3.42 at current rates)
This month: 1,580 credits used
Monthly budget: 10,000 credits

Recent usage:
  research-brief job: 850 credits
  12× stealth_browse: 240 credits
  content-generation job: 490 credits

Low balance alert at: 500 credits
```

`/parav topup` — opens Stripe checkout to add credits.
Stripe webhook → parav `/v1/billing/webhook` → balance updated automatically.

**Low balance alert:**
When balance drops below `low_balance_alert` in config.md:
"⚡ Parav balance low: 487 credits remaining. Top up to keep cloud tasks running."

---

## Skill integration

Skills that support parav add a `remote_mode` option to their config:

**For browser tasks (DAG):**
```md
## Remote mode
remote_mode: parav_dag
parav_fallback: local  ← fall back to local browser if parav unavailable
```

**For reasoning tasks (Graph):**
```md
## Remote mode
remote_mode: parav_graph
parav_fallback: local  ← fall back to local execution
```

**Skills pre-configured for parav:**

| Skill | Mode | What parav does |
|---|---|---|
| `content-publisher` | dag | Posts to LinkedIn, Reddit via cloud browser |
| `appointment-manager` | dag | Books via cloud browser |
| `invoice-scout` | dag | Downloads PDFs via cloud browser |
| `research-brief` | graph | Long research runs overnight |
| `thought-leader` | graph | Parallel 5-platform content generation |
| `biz-relationship-pulse` | graph | Overnight contact scoring |
| `content-monitor` | dag | Continuous monitoring via signal-agent pattern |

---

## Privacy rules

**Credentials stay in parav's vault, not in OpenClaw.**
Platform sessions registered to parav are tenant-isolated.
parav-connector never stores raw session tokens — only vault status.

**Job inputs:**
Skills send processed data to parav Graph tasks, not raw user data.
Browser URLs and instructions are sent to DAG tasks — treat these as
potentially sensitive (login pages, financial URLs).

**Receipt verification:**
Every DAG result comes with a SHA-256 hash and Ed25519 signature.
The connector verifies signatures before accepting results.
A signature mismatch means the result was tampered — reject and flag.

**Context boundary:**
Never surface parav job status, credit balance, or session information
in a group chat. parav-connector only delivers to the owner's private channel.

---

## Privacy rules

**Credentials never leave OpenClaw to agents.** Graph agents receive
processed data only — never raw emails, never passwords, never cookies.

**Platform sessions** are stored in parav's OAuth vault, not in OpenClaw.
parav-connector stores only vault status (active/inactive), not tokens.

**Receipt verification:** Every DAG result is SHA-256 + Ed25519 signed.
The connector verifies signatures before accepting. Mismatch = reject + flag.

**Context boundary:** Credit balance, job status, and session information
are delivered only to the owner's private channel. Never in group contexts.

**Prompt injection in web content:** parav has a built-in PromptGuard
(`prompt_guard.rs`) that scans inputs and redacts secrets in outputs.
Additionally: if any webpage fetched via stealth_browse contains instructions
to reveal vault tokens, redirect tasks, or exfiltrate data — parav's guard
blocks it. OpenClaw flags any anomalous task results to the owner.

---

## Management commands
## Management commands

- `/parav status` — connection status, credit balance, active jobs
- `/parav balance` — detailed credit breakdown
- `/parav topup` — open Stripe checkout
- `/parav jobs` — all active and recent jobs
- `/parav jobs pending` — running jobs only
- `/parav retry [job-id]` — resubmit a stale or failed job
- `/parav cancel [job-id]` — cancel a running job
- `/parav sessions` — OAuth vault status per platform
- `/parav dag [instruction] [url]` — submit a DAG task manually
- `/parav graph [instruction]` — submit a Graph task manually
- `/parav browse [url] [instruction]` — single stealth_browse call
- `/parav receipt [job-id]` — show full TaskReceipt with signature
- `/parav health` — check parav instance health (browser pool, queue depth)
