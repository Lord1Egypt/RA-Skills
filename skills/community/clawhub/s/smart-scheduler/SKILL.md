---
name: smart-scheduler
description: Coordinate meeting requests, proposed time slots, confirmations, and ICS exports from a local scheduling ledger.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/Mehulupase01/openclaw-skill-suite/tree/main/skills/smart-scheduler
    requires:
      bins:
        - python
---

# Smart Scheduler

Use this skill when the user wants the agent to coordinate meeting requests,
track proposed time slots, confirm a final booking, or export an ICS file for a
scheduled meeting.

## When to Use

- Creating a new scheduling request from a conversation.
- Recording candidate meeting times from different participants.
- Confirming the final slot after agreement.
- Exporting a calendar file that can be shared or imported.

## Commands

The helper script stores state in `{baseDir}/.runtime/smart-scheduler.db`.

### Create a request

```bash
python {baseDir}/scripts/smart_scheduler.py create-request --title "Weekly sync" --organizer "Mehul" --timezone "Europe/Berlin" --duration-minutes 30 --participant "Priya|telegram|@priya" --participant "Marco|email|marco@example.com"
```

### Propose time slots

```bash
python {baseDir}/scripts/smart_scheduler.py propose-slots --request-id 1 --slot "2026-03-25T09:00|2026-03-25T09:30" --slot "2026-03-25T16:00|2026-03-25T16:30" --source "scheduler-negotiation"
```

### Confirm a slot

```bash
python {baseDir}/scripts/smart_scheduler.py confirm-slot --request-id 1 --slot-id 2 --confirmed-by "Priya"
```

### Export ICS

```bash
python {baseDir}/scripts/smart_scheduler.py export-ics --request-id 1 --output {baseDir}/.runtime/weekly-sync.ics
```

## Safety Boundaries

- Never mark a slot confirmed unless the user or participant explicitly chose it.
- Keep time zone strings exactly as provided instead of guessing silently.
- If the schedule is ambiguous, present the unresolved options rather than inventing agreement.
- Do not overwrite an existing booking without saying so clearly.
