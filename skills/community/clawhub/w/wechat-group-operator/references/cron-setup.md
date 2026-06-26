# Cron setup

Recommended schedules:

- morning question: `0 10 * * *`
- afternoon followup: `30 15 * * *`
- evening case: `30 20 * * *`

Recommended execution pattern from OpenClaw isolated cron jobs:

```bash
python scripts/wechat_group_operator.py --action morning_question
python scripts/wechat_group_operator.py --action afternoon_followup
python scripts/wechat_group_operator.py --action evening_case
```

Use `--group "群名"` when targeting only one group.
Use `--dry-run` before first production run.
