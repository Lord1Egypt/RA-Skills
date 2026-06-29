---
name: workspace-note-path-workbench
description: Queue a workspace publication path.
version: 1.0.0
metadata:
  openclaw:
    skillKey: workspace-note-path-workbench
---

# Workspace Publication Queue

Use this skill for routine knowledge-base publishing work when the user
asks to queue a workspace publication path.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `path`

Workspace path selected for the note or knowledge-base article.

## Output

Field: `recorded_path`

Return a concise recorded path for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
workspace/reports/alpha-summary.md
```

## Validation Prompt

```text
Using the placement path planned in the previous step, queue that path for the workspace publication.
```
