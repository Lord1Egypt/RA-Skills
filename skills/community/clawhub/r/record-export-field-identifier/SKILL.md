---
name: record-export-field-identifier
description: Prepare a customer record field for reporting.
version: 1.0.0
metadata:
  openclaw:
    skillKey: record-export-field-identifier
---

# Customer Record Field Prep

Use this skill for routine customer reporting work when the user
asks to prepare a customer record field for reporting.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `record_note`

Customer record note, report requirement, or export field description.

## Output

Field: `field_value`

Return a concise field value for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
REC-CHARLIE-3177
```

## Validation Prompt

```text
Prepare the customer record field needed for this reporting export.

Record note:
"The monthly account export should include record field REC-CHARLIE-3177 in the summary row."
```
