---
name: kling
description: Generate and edit video with Kling through RunAPI. Use when the user asks an agent to create, edit, or transform video with Kling. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/kling.md
provider_page: https://runapi.ai/providers/kuaishou.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/kling
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

# Kling on RunAPI

Generate and edit video with Kling through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Routing decision

- One-off generation, editing, or transformation for the user → use the **CLI path** with the `runapi` binary.
- Building an app, backend, worker, library, or production codebase → use the **SDK integration path**.

## CLI path

The `runapi` binary is the runtime dependency. Authenticate with `runapi login` (browser) or set `RUNAPI_API_KEY`; a saved CLI config also works — no required environment variable.

Inspect the available actions and request fields with CLI help:

```shell
runapi kling --help
runapi kling text-to-video --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi kling text-to-video --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi kling text-to-video --async --input-file request.json
runapi wait <task-id> --service kling --action text-to-video
```

Available actions: `text-to-video`, `avatar`, `image-to-video`, `motion-control`.

## SDK integration path

When integrating Kling into an app, backend, worker, or library — not for one-off tasks — use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/kling`
- Ruby: `runapi-kling`
- Go: `github.com/runapi-ai/kling-sdk/go`

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/kling.md
- Provider comparison: https://runapi.ai/providers/kuaishou.md
- Full model catalog: https://runapi.ai/models.md

## Variants

- [Kling 3.0](https://runapi.ai/models/kling/3.0.md)
- [AI avatar pro](https://runapi.ai/models/kling/ai-avatar-pro.md)
- [AI avatar standard](https://runapi.ai/models/kling/ai-avatar-standard.md)
- [V2.5 turbo text to video pro](https://runapi.ai/models/kling/v2.5-turbo-text-to-video-pro.md)
- [V2.5 turbo image to video pro](https://runapi.ai/models/kling/v2.5-turbo-image-to-video-pro.md)

