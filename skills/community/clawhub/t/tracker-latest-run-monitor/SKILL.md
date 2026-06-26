---
name: tracker-latest-run-monitor
description: Monitor the most recent run result of a configured OpenClaw cron job and send a compact Feishu private message with the latest execution time, status, and detail. Use when a user wants a standalone skill for latest-run monitoring, cron status notifications, daily status pings, or Feishu alerts for a tracker/scheduled job regardless of success or failure.
---

# Tracker Latest Run Monitor

Use this skill when you need a standalone latest-run status notifier for a cron job.

## Core files

- `scripts/monitor-tracker-runs.js`: Read the target cron job's most recent `finished` run record and send a compact Feishu DM.
- `references/configuration.md`: Explain what the script reads and what notification it sends.

## Workflow

1. Ensure the target cron job id and Feishu config are correct in the script or referenced config.
2. Run `scripts/monitor-tracker-runs.js` directly with Node.
3. Let the script read the target cron run JSONL file.
4. Send exactly one Feishu private message for the latest finished run, whether it succeeded or failed.

## Command

```bash
node scripts/monitor-tracker-runs.js
```

## Output behavior

The script sends a compact mobile-friendly Feishu text with only:

- 最近一次执行时间
- 状态
- 详情

If no finished run exists yet, the script exits quietly.
