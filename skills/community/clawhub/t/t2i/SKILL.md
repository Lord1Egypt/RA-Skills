---
name: "t2i"
description: Placeholder skill for text-to-image workflows on skills.video. Use when the user is asking about t2i generation and the concrete API contract has not been implemented yet.
---

# t2i

## Overview
Use this as a placeholder skill for text-to-image generation on `skills.video`.
This file is intentionally incomplete and should not be treated as a production workflow.

## Current status
- No verified t2i OpenAPI contract has been wired into this skill yet.
- No default endpoint, payload template, or helper command is defined yet.
- The skill should surface this limitation clearly instead of guessing request fields.

## Temporary behavior
When this skill is invoked before implementation is completed:

1. Tell the user that `t2i` is currently a placeholder.
2. Check whether a model-specific `openapi.json` or docs page exists for the requested provider/model.
3. Avoid inventing undocumented request fields or unsupported image parameters.
4. Ask for the exact model or endpoint only if it is necessary to continue.
5. Once the API contract is confirmed, promote this placeholder into a real workflow or redirect to `image-generation` if that generic skill is sufficient.

## Implementation checklist
- Confirm which providers/models support t2i on `skills.video`
- Identify the create endpoint and terminal status flow
- Document prompt, size, aspect ratio, and other supported parameters
- Add request-template extraction steps from OpenAPI
- Add execution examples and fallback polling behavior if applicable
- Add runtime error handling guidance

## Related skills
- `image-generation`: generic image generation flow
- `i2i`: image-to-image placeholder flow
- `t2v`: text-to-video placeholder flow
