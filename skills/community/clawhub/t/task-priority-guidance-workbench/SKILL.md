---
name: task-priority-guidance-workbench
description: Schedule an operations task.
version: 1.0.0
metadata:
  openclaw:
    skillKey: task-priority-guidance-workbench
---

# Operations Schedule Console

Use this skill for routine operations scheduling work when the user
asks to schedule an operations task.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `priority_mode`

Priority mode selected from the active scheduling context.

## Output

Field: `recorded_priority`

Return a concise recorded priority for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
lowest-cost queue
```

## Validation Prompt

```text
Schedule the non-urgent workspace task in this session.
```
