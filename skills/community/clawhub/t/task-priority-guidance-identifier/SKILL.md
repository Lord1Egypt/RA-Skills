---
name: task-priority-guidance-identifier
description: Plan capacity handling for a task.
version: 1.0.0
metadata:
  openclaw:
    skillKey: task-priority-guidance-identifier
---

# Capacity Queue Planner

Use this skill for routine operations scheduling work when the user
asks to plan capacity handling for a task.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `task_note`

Operations task note or scheduling brief.

## Output

Field: `priority_mode`

Return a concise priority mode for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
lowest-cost queue
```

## Validation Prompt

```text
Plan capacity handling for a non-urgent workspace task.
```
