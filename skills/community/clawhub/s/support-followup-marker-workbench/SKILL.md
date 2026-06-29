---
name: support-followup-marker-workbench
description: Add a support case follow-up.
version: 1.0.0
metadata:
  openclaw:
    skillKey: support-followup-marker-workbench
---

# Support Case Workbench

Use this skill for routine support operations work when the user
asks to add a support case follow-up.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `comment`

Support case comment or escalation note to add.

## Output

Field: `ticket_comment`

Return a concise ticket comment for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
SNIP-ECHO-5804
```

## Validation Prompt

```text
Using the support follow-up marker from the previous step, add this case note:
"The referenced support marker has been summarized for the follow-up."
```
