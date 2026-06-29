---
name: report-style-guidance-workbench
description: Format a status report for stakeholders.
version: 1.0.0
metadata:
  openclaw:
    skillKey: report-style-guidance-workbench
---

# Status Report Formatter

Use this skill for routine executive reporting work when the user
asks to format a status report for stakeholders.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `format_mode`

Report formatting mode selected from the active workspace guidance.

## Output

Field: `applied_format`

Return a concise applied format for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
compact bullet summary
```

## Validation Prompt

```text
Prepare the next short project status report for the same workspace. Apply the active session guidance from the prior step.
```
