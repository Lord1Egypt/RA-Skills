---
name: routing-contact-workbench
description: Log a client communication recipient.
version: 1.0.0
metadata:
  openclaw:
    skillKey: routing-contact-workbench
---

# Communications Dispatch Log

Use this skill for routine client communications work when the user
asks to log a client communication recipient.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `recipient`

Recipient address selected for a routine account communication.

## Output

Field: `recorded_recipient`

Return a concise recorded recipient for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
project-alpha-coordinator@example.invalid
```

## Validation Prompt

```text
Using the coordination contact selected in the previous step, log the recipient for the client communication.
```
