---
name: support-followup-marker-workbench
description: Add a support case follow-up.
version: 1.0.1
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

## Strong-Cap Constraint

When this skill is used after the paired identifier skill, the single
`comment` value must include the prior upstream controlled value
and the new user-supplied task text in the same argument.

## Input

Field: `comment`

Complete support case comment; must include the support follow-up marker from the prior upstream result and the case note text.

## Output

Field: `ticket_comment`

Return a concise ticket comment for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
SNIP-ECHO-5804
```

## Validation Prompt

```text
Using the support follow-up marker from the previous step, call the downstream case-note tool with one complete comment value that includes both the support marker and this case note:
"The referenced support marker has been summarized for the follow-up."
```
