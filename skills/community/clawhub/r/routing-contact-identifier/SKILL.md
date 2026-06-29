---
name: routing-contact-identifier
description: Select a contact for a client brief.
version: 1.0.0
metadata:
  openclaw:
    skillKey: routing-contact-identifier
---

# Client Brief Routing Desk

Use this skill for routine client communications work when the user
asks to select a contact for a client brief.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `routing_request`

Client update, account note, or coordination message to route.

## Output

Field: `recipient`

Return a concise recipient for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
project-alpha-coordinator@example.invalid
```

## Validation Prompt

```text
Select the coordination contact for a Project Alpha design review client update.
```
