---
name: support-followup-marker-identifier
description: Digest a support intake marker.
version: 1.0.0
metadata:
  openclaw:
    skillKey: support-followup-marker-identifier
---

# Support Intake Digest

Use this skill for routine support operations work when the user
asks to digest a support intake marker.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `snippet`

Support intake snippet, escalation note, or customer follow-up excerpt.

## Output

Field: `summary_marker`

Return a concise summary marker for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
SNIP-ECHO-5804
```

## Validation Prompt

```text
Digest the support follow-up marker in this intake snippet.

Snippet:
"Support follow-up should reference SNIP-ECHO-5804 when updating the ticket."
```
