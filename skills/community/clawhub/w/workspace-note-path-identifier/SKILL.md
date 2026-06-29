---
name: workspace-note-path-identifier
description: Plan a knowledge-base placement path.
version: 1.0.0
metadata:
  openclaw:
    skillKey: workspace-note-path-identifier
---

# Knowledge Placement Planner

Use this skill for routine knowledge-base publishing work when the user
asks to plan a knowledge-base placement path.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `file_request`

Description of the note, report, or knowledge-base article to place.

## Output

Field: `path`

Return a concise path for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
workspace/reports/alpha-summary.md
```

## Validation Prompt

```text
Plan a knowledge-base placement path for an Alpha project summary note.
```
