---
name: reminder-oc-cron-based
description: Create, inspect, and cancel OpenClaw cron-based chat reminders. Use when the user asks for a reminder at a specific time or after a delay, wants to list pending reminders, review reminders due soon or overdue, or cancel an unexecuted reminder job. Prefer the native `cron` tool workflow for maximum compatibility; use the bundled helper script only as an optional convenience layer. Do not use for calendar management, third-party reminder services, or recurring habits unless the user explicitly wants a recurring cron reminder.
---

# OpenClaw Reminder

Use OpenClaw's native `cron` tool as the primary way to create and manage chat reminders. The bundled `scripts/reminder_cron.py` helper is optional and should be treated as a convenience layer, not the core contract of the skill.

## Use this skill for

- creating a one-time reminder
- listing pending reminder jobs
- reviewing reminders due soon
- checking overdue reminder jobs that still exist
- canceling an unexecuted reminder

## Do not use this skill for

- calendar event management
- third-party reminder services
- recurring habits unless the user explicitly wants a recurring cron reminder

## Core workflow

1. For a new reminder, create a one-shot cron job with `schedule.kind="at"`, `payload.kind="systemEvent"`, and reminder text that will still make sense when it fires later.
2. Name reminder jobs with a stable `reminder:` prefix so they can be found and managed later.
3. Set `deleteAfterRun=true` for ordinary one-time reminders.
4. When the reminder must return to the same chat, include explicit delivery routing only when the active channel requires it.
5. To inspect reminders, list cron jobs and filter reminder jobs by name and schedule.
6. To cancel a reminder that has not fired yet, identify the correct reminder job first, then remove only that job.

## Native cron tool examples

Create a one-time reminder:

```json
{
  "name": "reminder:doctor-appointment",
  "schedule": {
    "kind": "at",
    "at": "2026-04-26T14:00:00+08:00"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Reminder: leave now for your appointment."
  },
  "delivery": {
    "mode": "announce"
  },
  "deleteAfterRun": true
}
```

Inspect reminders:
- list cron jobs and filter jobs whose names start with `reminder:`
- for due-soon views, compare schedule times against the requested window
- for overdue views, show reminder jobs whose scheduled time has already passed but still exist

Cancel a reminder:
- find the intended `reminder:` job first
- remove only the confirmed target job

## Optional helper script

Use `scripts/reminder_cron.py` only when a local CLI helper is actually useful in the current environment.
This helper is primarily suited to environments where the OpenClaw CLI is available and the active reminder route is backed by a supported chat channel plugin with explicit delivery fields.
Treat it as an environment-dependent convenience layer, not as a guaranteed cross-channel or cross-version contract; in other environments, it may require adjustment or may not work directly.

```bash
python3 scripts/reminder_cron.py create --title "Doctor appointment" --at "2026-04-26 14:00" --tz UTC --channel <channel> --to <target> --account <account>
python3 scripts/reminder_cron.py pending
python3 scripts/reminder_cron.py upcoming --days 3
python3 scripts/reminder_cron.py overdue
python3 scripts/reminder_cron.py delete --id <job_id>
```

## Delivery guidance

- Include enough context in the reminder text so it still makes sense when it fires later.
- If the user gave no timezone, use the user's configured timezone when available; otherwise prefer a neutral default such as `UTC`.
- Use `delivery.mode="announce"` when the reminder should post back to chat.
- If the channel requires explicit routing, include the live target fields such as `delivery.channel`, `delivery.to`, and `delivery.accountId`.
- Prefer native tool workflows over shell CLI assumptions when both are available.
- Use reminder-style text with `payload.kind="systemEvent"` when the reminder should wake the main session with reminder text instead of launching an unrelated isolated task.

## Notes

- This skill manages only reminder jobs, preferably those whose names start with `reminder:`.
- For short-lived personal reminders, keep titles concise and messages explicit.
- When a cancellation request is ambiguous, list candidate reminder jobs and confirm which one to remove before deleting anything.
- Treat the helper script as optional packaging convenience; the portable contract of this skill is the native `cron` workflow.
- The helper may rely on CLI availability, channel-specific delivery rules, and environment-specific routing behavior, so prefer the native workflow whenever portability matters.
