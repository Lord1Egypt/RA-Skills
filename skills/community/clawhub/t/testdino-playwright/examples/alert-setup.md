# Failure Alerts — Real-Time CI Failure Notifications

Polls TestDino every 15 minutes and sends an alert when new failures appear.
Stays silent when CI is clean or only flaky tests are failing.

## What triggers an alert

- Any test with `status=failed` in the last 15 minutes
- Only sends a message if failures are found — no noise when everything passes

## What the alert includes

- Test name
- Branch name
- Error category (timeout, element_not_found, assertion_failure, network_issues)
- Number of failures found

---

## Setup

### Method 1 — CLI (recommended)

Run this while the gateway is running. Replace `YOUR_CHANNEL`, `YOUR_DESTINATION`, and `your-gateway-token` with your values — see the [main README](../README.md#method-1--cli-openclaw-cron-add) for how to find them.

```bash
openclaw cron add --name "testdino-failure-watch" --every 15m --session isolated --announce --channel YOUR_CHANNEL --to "YOUR_DESTINATION" --token "your-gateway-token" --message "Call the TestDino health tool to get my project ID. Then call list_testcase with by_status=failed and by_time_interval=1h. Look only at test cases that appear recent (within the last 15 minutes based on timestamps if available). If there are any failed tests, send an alert listing: the test names, the branch they are on, and the error category. If there are zero failures, do not send any message — stay completely silent."
```

### Method 2 — Direct JSON (`~/.openclaw/cron/jobs.json`)

Add this entry to your `~/.openclaw/cron/jobs.json` then restart the gateway:

```json
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
```

### Method 3 — `openclaw.json`

> **Version note:** Support for `crons` in `openclaw.json` depends on your OpenClaw version. Not available in **2026.3.13** — if your gateway reports `Unrecognized key: "crons"` on startup, use Method 1 or Method 2 instead.

```json
{
  "crons": [
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

## Alert Frequency Options

| Schedule | Meaning |
|---|---|
| `--every 15m` | Every 15 minutes (recommended) |
| `--every 10m` | Every 10 minutes |
| `--every 30m` | Every 30 minutes |
| `--cron "0 * * * *"` | Once per hour |
| `--cron "*/5 * * * 1-5"` | Every 5 minutes on weekdays only |

---

## Combining Digest + Alerts

Run both together — the digest gives you the morning overview, the alerts catch new failures during the day. See [morning-digest.md](./morning-digest.md) for the digest setup, then add both crons.

---

## Example Alert Output

```
TestDino Alert — New CI Failure

2 failures detected:

• checkout.spec.ts — assertion_failure — branch: main
• payment-flow.spec.ts — timeout_issues — branch: main
```

---

## Tips

- If you get too many alerts during a known flaky period, temporarily change
  the frequency to `--every 1h` until things stabilize.
- To monitor a specific branch only, add `on branch X` to the prompt.
- To suppress alerts outside working hours, use `--cron "*/15 8-18 * * 1-5"` (every 15 min, 8am–6pm weekdays).
