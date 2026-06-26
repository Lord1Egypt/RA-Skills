---
name: qqbot-remind-absolute
description: Manage QQBot reminders through real OpenClaw cron jobs with explicit per-user timezone settings. Use when a QQ user asks for reminders, alarms, timed notifications, recurring reminders, reminder lookup, reminder cancellation, or timezone setup/change. On a user's first reminder request, require them to explicitly provide a timezone before creating reminders.
---

# QQBot Remind Absolute

Use this skill for QQ reminder workflows.

## Core rules

1. Do not promise reminders verbally. Always create or manage real cron jobs.
2. Before a user's first reminder is created, require an explicit timezone.
3. Store timezone per QQ target and allow later updates.
4. Parse reminder time locally, then convert it into either an absolute datetime or a cron expression.
5. Keep query and cancellation in the same skill.

## Required flow

### First-time reminder setup

If the user has never set a timezone, do not create the reminder yet.
Ask them to explicitly provide one, for example:
- `Asia/Shanghai`
- `Asia/Tokyo`
- `America/Los_Angeles`

Then run:
- `python scripts/schedule_reminder.py set-timezone --to "<qq-target>" --timezone "<IANA timezone>"`

### Change timezone later

Run:
- `python scripts/schedule_reminder.py set-timezone --to "<qq-target>" --timezone "<IANA timezone>"`

### Check timezone

Run:
- `python scripts/schedule_reminder.py get-timezone --to "<qq-target>"`

### Add reminders

Use one of these:
- One-shot absolute: `python scripts/schedule_reminder.py add --content "抢票" --to "<qq-target>" --at "2026-04-22 21:30"`
- One-shot natural language: `python scripts/schedule_reminder.py add --content "喝水" --to "<qq-target>" --at "今晚11点"`
- Relative: `python scripts/schedule_reminder.py add --content "喝水" --to "<qq-target>" --in 5`
- Recurring cron: `python scripts/schedule_reminder.py add --content "打卡" --to "<qq-target>" --cron "0 8 * * *"`
- Recurring Chinese phrase: `python scripts/schedule_reminder.py add --content "喝水" --to "<qq-target>" --at "每天早上8点"`

### List reminders

Run:
- `python scripts/schedule_reminder.py list --to "<qq-target>"`

### Remove reminders

Run:
- `python scripts/schedule_reminder.py remove --id "<job-id>"`

## Time handling

The script supports:
- `21:30`
- `21.30`
- `21点30`
- `今晚11点`
- `明天早上8点`
- `每天早上8点`
- `工作日9点`
- `周六晚上10点`

The script stores timezone per target in `data/user_timezones.json`.

## Reply style

Keep replies short and direct.

Examples:
- `先告诉我你的时区，例如 Asia/Shanghai，我再给你建提醒。`
- `⏰ 好，今晚十一点提醒你。`
- `⏰ 好，我会每天早上八点提醒你。`
- `✅ 时区已经改成 Asia/Tokyo。`
- `📋 这是你当前的提醒列表。`
- `✅ 已帮你取消这个提醒。`

## Notes

- Delivery still relies on real `openclaw cron` jobs.
- Timezone is mandatory on first use because reminder meaning depends on the user's locale.
- Query and cancel are part of the same reminder system and should stay in this skill.
