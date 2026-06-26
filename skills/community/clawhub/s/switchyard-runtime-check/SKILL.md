---
name: switchyard-runtime-check
description: Verify the optional local Switchyard runtime path without changing Campus-owned response semantics.
---

# Switchyard Runtime Check

Use this skill when you want to verify the Campus consumer seam while keeping runtime transport behind the optional local Switchyard boundary.

## Steps

1. Call `GET /api/providers/status`.
2. Confirm whether `switchyard.ready` is `true`.
3. If ready, use the Campus consumer seam or `/api/providers/switchyard/chat`.
4. Preserve Campus response semantics: `answerText`, optional `structuredAnswer`, `nextActions`, `trustGaps`, and `citations`.

## Hard boundary

- Do not bypass Campus semantics by exposing raw upstream provider payloads.
- Do not describe this as hosted autonomy or a write-capable agent runtime.
