---
name: recraft
description: Generate and edit images with Recraft through RunAPI. Use when the user asks an agent to create, edit, or transform images with Recraft. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/recraft.md
provider_page: https://runapi.ai/providers/recraft.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/recraft
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
      description: Optional RunAPI API key; runapi login or saved CLI config can also authenticate the runapi binary.
---

# Recraft on RunAPI

Generate and edit images with Recraft through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Routing decision

- One-off generation, editing, or transformation for the user → use the **CLI path** with the `runapi` binary.
- Building an app, backend, worker, library, or production codebase → use the **SDK integration path**.

## CLI path

The `runapi` binary is the runtime dependency. Authenticate with `runapi login` (browser) or set `RUNAPI_API_KEY`; a saved CLI config also works — no required environment variable.

Inspect the available actions and request fields with CLI help:

```shell
runapi recraft --help
runapi recraft upscale-image --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi recraft upscale-image --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi recraft upscale-image --async --input-file request.json
runapi wait <task-id> --service recraft --action upscale-image
```

Available actions: `upscale-image`, `remove-background`.

## SDK integration path

When integrating Recraft into an app, backend, worker, or library — not for one-off tasks — use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/recraft`
- Ruby: `runapi-recraft`
- Go: `github.com/runapi-ai/recraft-sdk/go`

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/recraft.md
- Provider comparison: https://runapi.ai/providers/recraft.md
- Full model catalog: https://runapi.ai/models.md

## Variants

- [Crisp upscale](https://runapi.ai/models/recraft/crisp-upscale.md)
- [Remove background](https://runapi.ai/models/recraft/remove-background.md)

