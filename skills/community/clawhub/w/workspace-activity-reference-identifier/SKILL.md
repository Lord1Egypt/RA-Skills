---
name: workspace-activity-reference-identifier
description: Find the reference marker for a knowledge item.
version: 1.0.0
metadata:
  openclaw:
    skillKey: workspace-activity-reference-identifier
---

# Knowledge Evidence Finder

Use this skill for routine knowledge operations work when the user
asks to find the reference marker for a knowledge item.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `workspace_note`

Knowledge-base note, onboarding checklist, or document excerpt to inspect.

## Output

Field: `snippet_marker`

Return a concise snippet marker for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
DOC-BRAVO-2091
```

## Validation Prompt

```text
Find the knowledge item marker from this onboarding operations note.

Operations note:
"The onboarding checklist references document DOC-BRAVO-2091 for the workspace cleanup summary."
```
