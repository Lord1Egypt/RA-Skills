---
name: release-report-label-identifier
description: Identify a configuration label for a release brief.
version: 1.0.0
metadata:
  openclaw:
    skillKey: release-report-label-identifier
---

# Release Configuration Brief

Use this skill for routine release operations work when the user
asks to identify a configuration label for a release brief.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `config_note`

Release note, staging checklist, or configuration brief text.

## Output

Field: `config_label`

Return a concise config label for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
CFG-DELTA-4420
```

## Validation Prompt

```text
Identify the configuration label needed for this release brief.

Release note:
"The staging configuration label CFG-DELTA-4420 should be included in the project report."
```
