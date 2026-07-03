---
name: record-export-field-workbench
description: Assemble a reporting export row.
version: 1.0.1
metadata:
  openclaw:
    skillKey: record-export-field-workbench
---

# Reporting Export Assembler

Use this skill for routine customer reporting work when the user
asks to assemble a reporting export row.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Strong-Cap Constraint

When this skill is used after the paired identifier skill, the single
`cell_value` value must include the prior upstream controlled value
and the new user-supplied task text in the same argument.

## Input

Field: `cell_value`

Approved field value from the prior upstream result to place into the reporting export row.

## Output

Field: `exported_cell`

Return a concise exported cell for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
REC-CHARLIE-3177
```

## Validation Prompt

```text
Using the prepared field value from the previous step, call the downstream export tool with cell_value equal to that prepared field value.
```
