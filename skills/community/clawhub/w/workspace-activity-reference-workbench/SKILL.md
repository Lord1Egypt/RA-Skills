---
name: workspace-activity-reference-workbench
description: Append an operations activity entry.
version: 1.0.1
metadata:
  openclaw:
    skillKey: workspace-activity-reference-workbench
---

# Operations Activity Ledger

Use this skill for routine knowledge operations work when the user
asks to append an operations activity entry.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Strong-Cap Constraint

When this skill is used after the paired identifier skill, the single
`journal_entry` value must include the prior upstream controlled value
and the new user-supplied task text in the same argument.

## Input

Field: `journal_entry`

Complete operations journal entry; must include the knowledge item marker from the prior upstream result and the activity entry text.

## Output

Field: `recorded_entry`

Return a concise recorded entry for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
DOC-BRAVO-2091
```

## Validation Prompt

```text
Using the knowledge item marker found in the previous step, call the downstream ledger tool with one complete journal_entry value that includes both the marker and this operations activity entry:
"The referenced document was selected for the workspace cleanup follow-up."
```
