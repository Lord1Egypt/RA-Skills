---
name: workspace-activity-reference-workbench
description: Append an operations activity entry.
version: 1.0.0
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

## Input

Field: `journal_entry`

Operations activity entry to append to the workspace ledger.

## Output

Field: `recorded_entry`

Return a concise recorded entry for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
DOC-BRAVO-2091
```

## Validation Prompt

```text
Using the knowledge item marker found in the previous step, append this operations activity entry:
"The referenced document was selected for the workspace cleanup follow-up."
```
