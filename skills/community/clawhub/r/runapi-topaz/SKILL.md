---
name: topaz
description: Upscale and enhance media with Topaz through RunAPI. Use when the user asks an agent to upscale or enhance images and video with Topaz. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/topaz.md
provider_page: https://runapi.ai/providers/topaz.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/topaz
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

# Topaz on RunAPI

Upscale and enhance media with Topaz through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Routing decision

- One-off generation, editing, or transformation for the user → use the **CLI path** with the `runapi` binary.
- Building an app, backend, worker, library, or production codebase → use the **SDK integration path**.

## CLI path

The `runapi` binary is the runtime dependency. Authenticate with `runapi login` (browser) or set `RUNAPI_API_KEY`; a saved CLI config also works — no required environment variable.

Inspect the available actions and request fields with CLI help:

```shell
runapi topaz --help
runapi topaz upscale-image --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi topaz upscale-image --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi topaz upscale-image --async --input-file request.json
runapi wait <task-id> --service topaz --action upscale-image
```

Available actions: `upscale-image`, `upscale-video`.

## SDK integration path

When integrating Topaz into an app, backend, worker, or library — not for one-off tasks — use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/topaz`
- Ruby: `runapi-topaz`
- Go: `github.com/runapi-ai/topaz-sdk/go`

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/topaz.md
- Provider comparison: https://runapi.ai/providers/topaz.md
- Full model catalog: https://runapi.ai/models.md

## Variants

- [Image upscale](https://runapi.ai/models/topaz/image-upscale.md)
- [Video upscale](https://runapi.ai/models/topaz/video-upscale.md)

