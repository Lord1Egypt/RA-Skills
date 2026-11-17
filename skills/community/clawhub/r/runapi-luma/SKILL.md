---
name: luma
description: "Query historical Luma tasks with the RunAPI CLI for one-off status lookup. This model is retired; do not create new tasks."
documentation: https://runapi.ai/models/luma.md
provider_page: https://runapi.ai/providers/luma.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/luma
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

# Luma on RunAPI

## Query a historical task

This model family is retired. Authenticate with environment auth or saved CLI config, then query an existing task ID using the current task-status contract. Do not create a new task or submit a replacement task.

```shell
runapi auth status
runapi luma --help
runapi luma <operation> --help
curl --fail --location https://runapi.ai/docs/api/luma/<operation>.md --output contract.md
runapi wait <existing-task-id> --service luma --action modify-video > result.json
```

For application integrations, use the SDK task-status method with the existing task ID. Do not call `create` or `run` for this retired model. Preserve the task ID and error if querying fails.

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/luma.md
- Provider overview: https://runapi.ai/providers/luma.md
- Full model catalog: https://runapi.ai/models.md
- SDK integration: https://github.com/runapi-ai/luma-sdk

## Retired references
- `luma-modify-video` (retired 2026-10-14): https://runapi.ai/models/luma.md
  This model ID is not mapped to another model.

New requests for these versions return HTTP 410 before task creation or balance deduction. Existing task IDs remain queryable through the task-status API. Do not retry task creation with a retired model ID.
