---
name: "v2v"
description: Placeholder skill for video-to-video workflows on skills.video. Use when the user is asking about v2v generation and the concrete API contract has not been implemented yet.
---

# v2v

## Overview
Use this as a placeholder skill for video-to-video generation on `skills.video`.
This file is intentionally incomplete and should not be treated as a production workflow.

## Current status
- No verified v2v OpenAPI contract has been wired into this skill yet.
- No default endpoint, payload template, or helper command is defined yet.
- The skill should surface this limitation clearly instead of guessing request fields.

## Temporary behavior
When this skill is invoked before implementation is completed:

1. Tell the user that `v2v` is currently a placeholder.
2. Check whether a model-specific `openapi.json` or docs page exists for the requested provider/model.
3. Avoid inventing undocumented video input fields, upload semantics, or edit parameters.
4. Ask for the exact model or endpoint only if it is necessary to continue.
5. Once the API contract is confirmed, promote this placeholder into a real workflow similar to `video-generation`.

## Implementation checklist
- Confirm which providers/models support v2v on `skills.video`
- Identify the create endpoint and terminal status flow
- Document video input format such as URL, file upload, or asset ID
- Document supported edit controls such as prompt, strength, trim, or style transfer
- Add request-template extraction steps from OpenAPI
- Add execution examples and fallback polling behavior if applicable
- Add runtime error handling guidance

## Related skills
- `video-generation`: generic video generation flow
- `i2v`: image-to-video placeholder flow
- `i2i`: image-to-image placeholder flow
