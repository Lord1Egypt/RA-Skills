# OpenClaw Automation

## Boundary

Scheduled tasks should default to reminders and suggestions. They should not automatically change weak-point status, memory, records, or generate new worksheets unless the parent has explicitly requested that behavior.

OpenClaw cron jobs are not declared by a skill manifest at install time. Use the bundled setup script after the parent explicitly enables scheduled reminders. The script detects whether `openclaw cron` is available; if not, it prints the exact commands instead of failing the learning workflow.

```bash
python3 {baseDir}/scripts/setup_scheduled_tasks.py \
  --workspace <personal-learning-workspace> \
  --enable-config \
  --auto-register \
  --timezone Asia/Shanghai
```

The setup writes `.zhizhi-math-coach/config.json`:

- `automation.enabled`: scheduled reminders are allowed.
- `automation.auto_register_when_supported`: register via `openclaw cron` when the CLI exists.
- `automation.timezone`: IANA timezone used by `openclaw cron --tz`; use the parent's local timezone, for example `Asia/Shanghai`.
- `automation.allow_record_writes`: default `false`.
- `automation.allow_auto_worksheet_generation`: default `false`.

## Recommended Schedule

- Daily 20:30 local time: due review reminders, pending upload reminders, and stale short-term observations.
- Sunday 20:00 local time: weekly progress review and next-week suggestions.
- End of semester: generate a summary and holiday review pool.
- Winter/summer break: weekly holiday review suggestions.

## Suggested Task Outputs

- due weak points;
- pending worksheets not yet graded;
- short explanation cards that may help parents;
- suggested next worksheet strategy;
- warnings about low-confidence or missing evidence.

## Channels

The learning logic should not depend on a channel. Start with local records and OpenClaw conversation output.

For push delivery, use a channel adapter. Feishu/Lark is the default v1 recommendation when available because it supports chat, files, and operational workflows. DingTalk can be added later through a channel/plugin adapter if the environment supports it.

## Safety

- Do not send sensitive student files to public channels.
- Do not push full answer keys into a child-facing chat.
- Do not infer new mastery status from time alone.
- Do not schedule automatic worksheet generation by default.
- Do not auto-create cron jobs merely because the skill was installed; require an explicit setup trigger or existing automation config.
