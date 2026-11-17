---
name: vidu
description: "Generate Vidu Q4 videos from a first-frame image or reference images and optional reference audio through RunAPI. Use the RunAPI CLI for one-off generation and an SDK for application integration."
documentation: https://runapi.ai/models/vidu.md
provider_page: https://runapi.ai/providers/vidu.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/vidu
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

# Vidu on RunAPI

## Not yet available

This model family is upcoming and has no callable endpoints yet. Read the linked model page for its current release status. Wait for a published callable contract before creating tasks or integrating generation.

Requests return HTTP 404 with `model_not_released` before task creation or balance deduction. There is no generation recipe to execute at this stage.

Read the current endpoint status before integrating: https://runapi.ai/docs/api/vidu/<operation>.md

Use only read-only discovery commands while waiting for launch: `runapi vidu --help` and `runapi vidu <operation> --help`. Do not submit requests.

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/vidu.md
- Provider overview: https://runapi.ai/providers/vidu.md
- Full model catalog: https://runapi.ai/models.md
- SDK integration: https://github.com/runapi-ai/vidu-sdk

## Variants
- `vidu-q4-image-to-video`: https://runapi.ai/models/vidu/q4-image-to-video.md
- `vidu-q4-reference-to-video`: https://runapi.ai/models/vidu/q4-reference-to-video.md
