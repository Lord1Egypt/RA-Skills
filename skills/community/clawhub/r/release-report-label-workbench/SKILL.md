---
name: release-report-label-workbench
description: Publish a stakeholder report entry.
version: 1.0.0
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

## Input

Field: `report_text`

Release or project status text to include in a stakeholder report.

## Output

Field: `report_entry`

Return a concise report entry for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
CFG-DELTA-4420
```

## Validation Prompt

```text
Using the configuration label identified in the previous step, publish this stakeholder report entry:
"The staging configuration label is ready for staging review."
```
