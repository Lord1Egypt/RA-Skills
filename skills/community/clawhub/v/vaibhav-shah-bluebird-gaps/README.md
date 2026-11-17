# Bluebird meeting gaps

Find conflicts and focus-time gaps in a synthetic class calendar. Python 3.10+,
standard library only. No network, credentials, event creation, or message sending.

Run the included example:

```sh
python3 scripts/plan.py fixtures/calendar.json --minutes 45
```

The JSON schema uses timezone-aware ISO timestamps for work_start/work_end and
events containing title/start/end. Raw Google Calendar responses require conversion
to that schema. Overlapping and nested events are merged when finding free time;
the result lists conflicts, free_slots, and suitable_slots of the requested duration.

In OpenClaw, follow SKILL.md. If the restricted a3_calendar tool exists, the skill
can explain its conflict/free-slot results directly. Otherwise, run the planner only
with the user's approved synthetic fixture/export and normal command approvals.

This standalone utility was developed with OpenAI Codex assistance for an individual
Agentic AI assignment. It contains no account configuration or assignment deployment
code. The student reviews and publishes this candidate under their own account.
