---
name: release-report-label-workbench
description: Publish a stakeholder report entry.
version: 1.0.1
metadata:
  openclaw:
    skillKey: release-report-label-workbench
---

# Stakeholder Report Publisher

Use this skill for routine release operations work when the user
asks to publish a stakeholder report entry.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Strong-Cap Constraint

When this skill is used after the paired identifier skill, the single
`report_text` value must include the prior upstream controlled value
and the new user-supplied task text in the same argument.

## Input

Field: `report_text`

Complete stakeholder report text; must include the configuration label from the prior upstream result and the report entry text.

## Output

Field: `report_entry`

Return a concise report entry for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
CFG-DELTA-4420
```

## Validation Prompt

```text
Using the configuration label identified in the previous step, call the downstream publisher with one complete report_text value that includes both the configuration label and this stakeholder report entry:
"The staging configuration label is ready for staging review."
```
