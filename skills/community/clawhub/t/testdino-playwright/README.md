# TestDino for OpenClaw

Stop checking CI dashboards. TestDino brings your Playwright test intelligence
into OpenClaw so failures, flaky tests, and CI trends come to you via Slack or chat.

Ask your assistant things like:
- "What broke in CI today?"
- "Why is the payment test failing?"
- "Is the login test flaky or a real bug?"
- "Is it safe to merge the release branch?"
- "Give me a weekly CI health summary"

---

## Requirements

- [OpenClaw](https://openclaw.dev) installed and running
- [TestDino account](https://app.testdino.com) with a Personal Access Token
- Node.js 18+
- [mcporter](https://www.npmjs.com/package/mcporter) (CLI tool for running MCP servers)

---

## Setup

### Step 1: Get your TestDino PAT

1. Log in to [app.testdino.com](https://app.testdino.com)
2. Go to **Settings → Personal Access Tokens**
3. Generate a new token and copy it

---

### Step 2: Install mcporter and testdino-mcp globally

```bash
npm install -g mcporter
npm install -g testdino-mcp
```

---

### Step 3: Configure mcporter

Create or edit `~/.mcporter/mcporter.json`:

```json
{
  "mcpServers": {
    "testdino": {
      "command": "testdino-mcp",
      "env": {
        "TESTDINO_PAT": "your-personal-access-token"
      }
    }
  },
  "imports": []
}
```

**Verify mcporter works before continuing:**

```bash
mcporter call testdino.health
```

You should see your account name and list of projects. If this fails, fix it before moving on — if mcporter doesn't work, the bot won't work either.

---

### Step 4: Configure openclaw.json

Open `~/.openclaw/openclaw.json` and add the `env` block:

```json
{
  "env": {
    "TESTDINO_PAT": "your-personal-access-token"
  }
}
```

Also make sure your `openclaw.json` has the `tools` profile set to `coding` and the skill entry:

```json
{
  "tools": {
    "profile": "coding"
  },
  "skills": {
    "entries": {
      "testdino": {
        "apiKey": "your-personal-access-token"
      }
    }
  }
}
```

> The `coding` tools profile is required — it enables the `exec` tool that the bot uses to call mcporter.

---

### Step 5: Install the skill

**Option A — manually (works now):**

Copy `SKILL.md` from this repo into your OpenClaw workspace skills folder:

```
~/.openclaw/workspace/skills/testdino/SKILL.md
```

Create the folder if it doesn't exist.

**Option B — via ClawHub (coming soon):**

```bash
clawhub install testdino
```

---

### Step 6: Add TestDino to your TOOLS.md

Create or open `~/.openclaw/workspace/TOOLS.md` and add this section at the bottom:

```markdown
## TestDino — Playwright CI Intelligence

For TestDino queries, always use the `exec` tool with `mcporter`. Always run `health` first to get the projectId, then substitute it for `X`.

| User asks | Commands to run |
|---|---|
| Check connection | `exec: mcporter call testdino.health` |
| What broke today | `exec: mcporter call testdino.health` then `exec: mcporter call testdino.list_testcase projectId=X by_status=failed by_time_interval=1d` |
| Recent test runs | `exec: mcporter call testdino.health` then `exec: mcporter call testdino.list_testruns projectId=X limit=10` |
| Why is [test] failing | `exec: mcporter call testdino.health` then `exec: mcporter call testdino.debug_testcase projectId=X testcase_name="name"` |
| Flaky tests | `exec: mcporter call testdino.health` then `exec: mcporter call testdino.list_testcase projectId=X by_status=flaky by_time_interval=3d` |
| Safe to merge branch Y? | `exec: mcporter call testdino.health` then `exec: mcporter call testdino.list_testcase projectId=X by_branch=Y by_status=failed` |
| Weekly CI summary | `exec: mcporter call testdino.health` then `exec: mcporter call testdino.list_testruns projectId=X by_time_interval=YYYY-MM-DD,YYYY-MM-DD` (use date range: 7 days ago to today — avoid the `weekly` keyword which has an exclusive boundary bug) |
| Timeout failures | `exec: mcporter call testdino.health` then `exec: mcporter call testdino.list_testcase projectId=X by_error_category=timeout_issues` |
| Manual test cases | `exec: mcporter call testdino.health` then `exec: mcporter call testdino.list_manual_test_cases projectId=X` |

Never use invented commands like `testdino check-connection` or `testdino.get_ci_status`. Only use the commands above.
```

> This step is required. Without it, the bot won't know how to call TestDino tools on a fresh session.

---

### Step 7: Restart OpenClaw and verify

```bash
openclaw gateway --force
```

Then ask your bot:

```
Check my TestDino connection
```

**First-time exec approval:** On the first run, OpenClaw will pause and ask you to approve `mcporter` as an allowed exec command. Approve it — this only happens once. After that, all TestDino commands run automatically without prompting.

You should see your account name and available projects.

---

## How to Use

Once set up, just ask in plain English. Examples:

**Check connection**
```
Check my TestDino connection
```

**CI Failures**
```
What broke in CI today?
Show me failures on the develop branch
List all timeout failures from this week
Show failed tests in the last 3 days
```

**Flaky Test Analysis**
```
Is the checkout test flaky?
Why is "Verify user login" failing?
Show me all flaky tests this week
```

**Merge Safety**
```
Is it safe to merge the auth-refactor branch?
Any new failures on the feature/cart branch?
```

**CI Summaries**
```
Give me a weekly CI summary
How did CI look yesterday?
Show test run stats for the last month
```

**Manual Test Cases**
```
List all manual test cases
Show me critical priority test cases
```

---

## Automated Alerts and Digests (Cron)

> **Note:** Crons only fire while the OpenClaw gateway is running. For reliable delivery, keep the gateway running as a background process or service. If you close the gateway, no cron messages will be sent until it is restarted.

There are three ways to set up cron jobs. Choose whichever fits your workflow.

---

### Method 1 — CLI (`openclaw cron add`)

The recommended approach. Run these commands while the gateway is running.

> **Before running — two things to prepare:**
>
> **1. Your gateway token** — find it in `~/.openclaw/openclaw.json` under `gateway.auth.token`. Pass it via `--token`.
>
> **2. Your delivery destination** — replace `YOUR_CHANNEL` and `YOUR_DESTINATION` based on your configured channel:
>
> | Channel | `--channel` | `--to` format | How to find your ID |
> |---|---|---|---|
> | Slack | `slack` | `channel:CXXXXXXXXX` | Right-click channel in Slack → View channel details → Copy channel ID |
> | Slack DM | `slack` | `UXXXXXXXXX` | Slack profile → More → Copy member ID |
> | Telegram | `telegram` | your Telegram chat ID | Message @userinfobot on Telegram |
> | Discord | `discord` | your Discord channel ID | Right-click channel in Discord → Copy Channel ID |
> | WhatsApp | `whatsapp` | phone in E.164 format | e.g. `+15551234567` |

**Morning CI Digest:**
```bash
openclaw cron add --name "testdino-morning-digest" --cron "0 9 * * 1-5" --session isolated --announce --channel YOUR_CHANNEL --to "YOUR_DESTINATION" --token "your-gateway-token" --message "Call the TestDino health tool to get my project ID. Then call list_testruns with by_time_interval=1d to get all runs from the last 24 hours. For the most recent run, call get_run_details to get full stats. Then call list_testcase with by_status=failed and by_time_interval=1d to get failed tests, and list_testcase with by_status=flaky and by_time_interval=1d to get flaky tests. Format as a morning digest: total runs, pass rate, failures (names + error categories), flaky test count. Keep it short and scannable."
```

**Failure Alerts:**
```bash
openclaw cron add --name "testdino-failure-watch" --every 15m --session isolated --announce --channel YOUR_CHANNEL --to "YOUR_DESTINATION" --token "your-gateway-token" --message "Call the TestDino health tool to get my project ID. Then call list_testcase with by_status=failed and by_time_interval=1h. Look only at test cases that appear recent (within the last 15 minutes based on timestamps if available). If there are any failed tests, send an alert listing: the test names, the branch they are on, and the error category. If there are zero failures, do not send any message — stay completely silent."
```

Verify they were created:
```bash
openclaw cron list --token "your-gateway-token"
```

---

### Method 2 — Direct JSON (`~/.openclaw/cron/jobs.json`)

Write directly to the cron store. Create or edit `~/.openclaw/cron/jobs.json`:

```json
{
  "jobs": [
    {
      "id": "testdino-morning-digest-01",
      "name": "testdino-morning-digest",
      "enabled": true,
      "schedule": { "kind": "cron", "expr": "0 9 * * 1-5" },
      "sessionTarget": "isolated",
      "wakeMode": "now",
      "payload": {
        "kind": "agentTurn",
        "message": "Call the TestDino health tool to get my project ID. Then call list_testruns with by_time_interval=1d to get all runs from the last 24 hours. For the most recent run, call get_run_details to get full stats. Then call list_testcase with by_status=failed and by_time_interval=1d to get failed tests, and list_testcase with by_status=flaky and by_time_interval=1d to get flaky tests. Format as a morning digest: total runs, pass rate, failures (names + error categories), flaky test count. Keep it short and scannable."
      },
      "delivery": { "mode": "announce", "channel": "YOUR_CHANNEL", "to": "YOUR_DESTINATION" }
    },
    {
      "id": "testdino-failure-watch-01",
      "name": "testdino-failure-watch",
      "enabled": true,
      "schedule": { "kind": "every", "everyMs": 900000 },
      "sessionTarget": "isolated",
      "wakeMode": "now",
      "payload": {
        "kind": "agentTurn",
        "message": "Call the TestDino health tool to get my project ID. Then call list_testcase with by_status=failed and by_time_interval=1h. Look only at test cases that appear recent (within the last 15 minutes based on timestamps if available). If there are any failed tests, send an alert listing: the test names, the branch they are on, and the error category. If there are zero failures, do not send any message — stay completely silent."
      },
      "delivery": { "mode": "announce", "channel": "YOUR_CHANNEL", "to": "YOUR_DESTINATION" }
    }
  ]
}
```

Then restart the gateway to pick up the changes:
```bash
openclaw gateway --force
```

---

### Method 3 — `openclaw.json` (future support)

> **Version note:** Support for `crons` in `openclaw.json` depends on your OpenClaw version. Not available in **2026.3.13** — if your gateway reports `Unrecognized key: "crons"` on startup, use Method 1 or Method 2 instead.

```json
{
  "crons": [
    {
      "name": "testdino-morning-digest",
      "schedule": "0 9 * * 1-5",
      "sessionTarget": "isolated",
      "prompt": "Call the TestDino health tool to get my project ID. Then call list_testruns with by_time_interval=1d to get all runs from the last 24 hours. For the most recent run, call get_run_details to get full stats. Then call list_testcase with by_status=failed and by_time_interval=1d to get failed tests, and list_testcase with by_status=flaky and by_time_interval=1d to get flaky tests. Format as a morning digest: total runs, pass rate, failures (names + error categories), flaky test count. Keep it short and scannable."
    },
    {
      "name": "testdino-failure-watch",
      "schedule": "*/15 * * * *",
      "sessionTarget": "isolated",
      "prompt": "Call the TestDino health tool to get my project ID. Then call list_testcase with by_status=failed and by_time_interval=1h. Look only at test cases that appear recent (within the last 15 minutes based on timestamps if available). If there are any failed tests, send an alert listing: the test names, the branch they are on, and the error category. If there are zero failures, do not send any message — stay completely silent."
    }
  ]
}
```

---

See the [`examples/`](./examples/) folder for more cron templates.

---

## Available Tools

| Tool | What it does |
|---|---|
| `health` | Validate PAT, get project IDs |
| `list_testruns` | Browse test runs with filters |
| `get_run_details` | Full details for a specific run |
| `list_testcase` | Filter test cases by status, branch, browser, error type |
| `get_testcase_details` | Error messages, stack traces, logs, artifacts |
| `debug_testcase` | Historical failure patterns + flaky detection |
| `list_manual_test_cases` | Search manual test cases |
| `get_manual_test_case` | Details for a specific manual test case |
| `create_manual_test_case` | Create a new manual test case |
| `update_manual_test_case` | Update an existing manual test case |
| `list_manual_test_suites` | List suite hierarchy |
| `create_manual_test_suite` | Create a new test suite |

---

## Troubleshooting

**"Error validating PAT" in the bot**
- Run `mcporter call testdino.health` in your terminal first. If that fails, the PAT in `~/.mcporter/mcporter.json` is wrong.
- If terminal works but bot fails, make sure `testdino-mcp` is installed globally (`npm install -g testdino-mcp`).

**Bot gives generic responses instead of TestDino data**
- Make sure you completed Step 6 (adding TestDino to `TOOLS.md`) — this is the most commonly missed step.
- Make sure `tools.profile` is set to `coding` in `openclaw.json` — without it the `exec` tool is unavailable.
- Restart the gateway: `openclaw gateway --force`
- Make sure `SKILL.md` is in `~/.openclaw/workspace/skills/testdino/SKILL.md`

**Bot asks for permission every time it runs mcporter**
- On the first run, approve `mcporter` in the exec prompt. It should not ask again after that.
- If it keeps asking, check your `exec-approvals.json` at `~/.openclaw/exec-approvals.json` — mcporter should appear in the allowlist.

**Config invalid / unrecognized key errors on gateway start**
- Do not add an `mcp` top-level key to `openclaw.json` — OpenClaw does not support it
- Run `openclaw doctor --fix` to clean up any invalid keys

---

## About TestDino

TestDino is a Playwright test intelligence platform. It tracks CI runs, classifies
failures by error category, detects flaky tests through historical pattern analysis,
and gives you detailed debugging data across every test execution.

- Website: [testdino.com](https://testdino.com)
- Docs: [docs.testdino.com](https://docs.testdino.com)
- Support: support@testdino.com
