---
name: qwen-2.1
description: "Generate and edit images with Qwen 2.1 through RunAPI. Use when the user asks an agent to create images, transparent-background assets, or mask-based local edits with Qwen 2.1. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend."
documentation: https://runapi.ai/models/qwen-2.1.md
provider_page: https://runapi.ai/providers/alibaba.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/qwen-2.1
    requires:
      bins:
      - runapi
    install:
    - kind: brew
      formula: runapi-ai/tap/runapi
      bins:
      - runapi
    envVars:
    - name: RUNAPI_API_KEY
      required: false
      description: Optional RunAPI API key; agents should prefer environment auth or saved CLI config. Browser login is interactive fallback only.
---

# Qwen 2.1 on RunAPI

## Not yet available

This model family is upcoming and has no callable endpoints yet. Read the linked model page for its current release status. Wait for a published callable contract before creating tasks or integrating generation.

Requests return HTTP 404 with `model_not_released` before task creation or balance deduction. There is no generation recipe to execute at this stage.

Read the current endpoint status before integrating: https://runapi.ai/docs/api/qwen-2-1/<operation>.md

Use only read-only discovery commands while waiting for launch: `runapi qwen-2-1 --help` and `runapi qwen-2-1 <operation> --help`. Do not submit requests.

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/qwen-2.1.md
- Provider overview: https://runapi.ai/providers/alibaba.md
- Full model catalog: https://runapi.ai/models.md
- SDK integration: https://github.com/runapi-ai/qwen-2.1-sdk

## Variants
- `qwen-2.1-edit-image`: https://runapi.ai/models/qwen-2.1/edit-image.md
- `qwen-2.1-text-to-image`: https://runapi.ai/models/qwen-2.1/text-to-image.md
