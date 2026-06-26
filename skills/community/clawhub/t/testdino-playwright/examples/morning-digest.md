# Morning Digest — Daily CI Health Summary

Sends a test health digest every weekday at 9am to your configured OpenClaw
notification channel (Telegram, Slack, Discord, etc.).

## What it covers

- Total CI runs in the last 24 hours
- New failures vs the day before
- Flaky test count and trend
- Top failing tests by name and error category
- Any tests that recovered (passed after previously failing)

---

## Setup

### Method 1 — CLI (recommended)

Run this while the gateway is running. Replace `YOUR_CHANNEL`, `YOUR_DESTINATION`, and `your-gateway-token` with your values — see the [main README](../README.md#method-1--cli-openclaw-cron-add) for how to find them.

```bash
openclaw cron add --name "testdino-morning-digest" --cron "0 9 * * 1-5" --session isolated --announce --channel YOUR_CHANNEL --to "YOUR_DESTINATION" --token "your-gateway-token" --message "Call the TestDino health tool to get my project ID. Then call list_testruns with by_time_interval=1d to get all runs from the last 24 hours. For the most recent run, call get_run_details to get full stats. Then call list_testcase with by_status=failed and by_time_interval=1d to get failed tests, and list_testcase with by_status=flaky and by_time_interval=1d to get flaky tests. Format as a morning digest: (1) Run summary — total runs, pass rate; (2) Failures — test names and error categories; (3) Flaky tests — count and names; (4) One-line health status. Keep it short."
```

### Method 2 — Direct JSON (`~/.openclaw/cron/jobs.json`)

Add this entry to your `~/.openclaw/cron/jobs.json` then restart the gateway:

```json
{
  "id": "testdino-morning-digest-01",
  "name": "testdino-morning-digest",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "0 9 * * 1-5" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Call the TestDino health tool to get my project ID. Then call list_testruns with by_time_interval=1d to get all runs from the last 24 hours. For the most recent run, call get_run_details to get full stats. Then call list_testcase with by_status=failed and by_time_interval=1d to get failed tests, and list_testcase with by_status=flaky and by_time_interval=1d to get flaky tests. Format as a morning digest: (1) Run summary — total runs, pass rate; (2) Failures — test names and error categories; (3) Flaky tests — count and names; (4) One-line health status. Keep it short."
  },
  "delivery": { "mode": "announce", "channel": "YOUR_CHANNEL", "to": "YOUR_DESTINATION" }
}
```

### Method 3 — `openclaw.json`

> **Version note:** Support for `crons` in `openclaw.json` depends on your OpenClaw version. Not available in **2026.3.13** — if your gateway reports `Unrecognized key: "crons"` on startup, use Method 1 or Method 2 instead.

```json
{
  "crons": [
    {
      "name": "testdino-morning-digest",
      "schedule": "0 9 * * 1-5",
      "sessionTarget": "isolated",
      "prompt": "Call the TestDino health tool to get my project ID. Then call list_testruns with by_time_interval=1d to get all runs from the last 24 hours. For the most recent run, call get_run_details to get full stats. Then call list_testcase with by_status=failed and by_time_interval=1d to get failed tests, and list_testcase with by_status=flaky and by_time_interval=1d to get flaky tests. Format as a morning digest: (1) Run summary — total runs, pass rate; (2) Failures — test names and error categories; (3) Flaky tests — count and names; (4) One-line health status. Keep it short."
    }
  ]
}
```

---

## Schedule Options

Change the `--cron` value to match your timezone or preference:

| `--cron` value | Meaning |
|---|---|
| `0 9 * * 1-5` | 9am weekdays |
| `0 8 * * 1-5` | 8am weekdays |
| `0 9 * * *` | 9am every day including weekends |
| `0 6 * * 1-5` | 6am weekdays (early alert) |

---

## Example Output

```
TestDino Morning Digest — Monday

Runs: 4 runs in the last 24 hours. Pass rate: 91%.

Failures (3):
• checkout.spec.ts — assertion_failure — main branch
• payment-flow.spec.ts — timeout_issues — main branch
• user-auth.spec.ts — element_not_found — develop branch

Flaky (2):
• sidebar-nav.spec.ts
• modal-close.spec.ts

Recoveries (1):
• login-redirect.spec.ts — passing again after 2 days

Overall: 3 real failures need attention. 2 known flaky tests still noisy.
```
