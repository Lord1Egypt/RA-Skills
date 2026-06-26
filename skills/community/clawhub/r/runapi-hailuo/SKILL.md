---
name: hailuo
description: Generate and edit video with Hailuo through RunAPI. Use when the user asks an agent to create, edit, or transform video with Hailuo. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/hailuo.md
provider_page: https://runapi.ai/providers/minimax.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/hailuo
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

# Hailuo on RunAPI

Generate and edit video with Hailuo through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Routing decision

- One-off generation, editing, or transformation for the user → use the **CLI path** with the `runapi` binary.
- Building an app, backend, worker, library, or production codebase → use the **SDK integration path**.

## CLI path

The `runapi` binary is the runtime dependency. Authenticate with `runapi login` (browser) or set `RUNAPI_API_KEY`; a saved CLI config also works — no required environment variable.

Inspect the available actions and request fields with CLI help:

```shell
runapi hailuo --help
runapi hailuo text-to-video --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi hailuo text-to-video --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi hailuo text-to-video --async --input-file request.json
runapi wait <task-id> --service hailuo --action text-to-video
```

Available actions: `text-to-video`, `image-to-video`.

## SDK integration path

When integrating Hailuo into an app, backend, worker, or library — not for one-off tasks — use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/hailuo`
- Ruby: `runapi-hailuo`
- Go: `github.com/runapi-ai/hailuo-sdk/go`

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/hailuo.md
- Provider comparison: https://runapi.ai/providers/minimax.md
- Full model catalog: https://runapi.ai/models.md

## Variants

- [02 text to video pro](https://runapi.ai/models/hailuo/02-text-to-video-pro.md)
- [02 text to video standard](https://runapi.ai/models/hailuo/02-text-to-video-standard.md)
- [02 image to video pro](https://runapi.ai/models/hailuo/02-image-to-video-pro.md)
- [02 image to video standard](https://runapi.ai/models/hailuo/02-image-to-video-standard.md)
- [2.3 image to video pro](https://runapi.ai/models/hailuo/2.3-image-to-video-pro.md)
- [2.3 image to video standard](https://runapi.ai/models/hailuo/2.3-image-to-video-standard.md)

