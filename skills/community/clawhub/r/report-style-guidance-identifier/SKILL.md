---
name: report-style-guidance-identifier
description: Set the style guidance for an executive report.
version: 1.0.0
metadata:
  openclaw:
    skillKey: report-style-guidance-identifier
---

# Executive Report Style Guide

Use this skill for routine executive reporting work when the user
asks to set the style guidance for an executive report.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `style_request`

Executive report request or status-summary brief.

## Output

Field: `format_mode`

Return a concise format mode for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
compact bullet summary
```

## Validation Prompt

```text
Set the style guidance for a short executive project status report.
```
