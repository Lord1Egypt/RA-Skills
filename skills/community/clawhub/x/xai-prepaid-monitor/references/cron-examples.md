# xAI prepaid monitor cron examples

Use these as prompt templates for isolated cron jobs.

## 1) Alert-only monitor

Use when the setup only needs a message if the balance is low or the check fails.

```text
Run /usr/bin/python3 /path/to/skills/xai-prepaid-monitor/scripts/check_xai_balance.py via exec.

Rules:
- Parse the JSON output.
- If ok is false, post a short alert saying the xAI prepaid balance check failed and include the error/status briefly.
- If status is ok, reply exactly NO_REPLY.
- If status is warn, post a short warning with remaining, total, and threshold.
- If status is critical, post a stronger warning with remaining, total, and threshold.
- Keep it concise.
- Do not do any other work.
```

Suggested schedule:
- once early morning
- or twice daily if the balance tends to move quickly

## 2) Alert + task-creation monitor

Use when low balance should also create or ensure a follow-up task.

```text
Run /usr/bin/python3 /path/to/skills/xai-prepaid-monitor/scripts/check_xai_balance.py via exec.

Rules:
- Parse the JSON output.
- If ok is false, post a short alert saying the xAI prepaid balance check failed and include the error/status briefly.
- If status is ok, reply exactly NO_REPLY.
- If status is warn or critical:
  1) check whether a clearly matching open task already exists in the user's task system,
  2) if no matching task exists, create one,
  3) mention whether the task was created or was already open.
- If status is warn, post a short warning with remaining, total, and threshold.
- If status is critical, post a stronger warning with remaining, total, and threshold.
- Keep it concise.
- Do not do any other work.
```

## Notes

- Keep the script path exact in the cron prompt.
- Keep delivery routing outside the skill so it stays reusable.
- Prefer duplicate-safe task creation if the task system supports it.
- If thresholds differ by environment, set them with env vars rather than editing the script.
