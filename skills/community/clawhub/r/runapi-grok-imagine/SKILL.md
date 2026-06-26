---
name: grok-imagine
description: Generate and edit images with Grok Imagine through RunAPI. Use when the user asks an agent to create, edit, or transform images with Grok Imagine. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/grok-imagine.md
provider_page: https://runapi.ai/providers/xai.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/grok-imagine
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

# Grok Imagine on RunAPI

Generate and edit images with Grok Imagine through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Routing decision

- One-off generation, editing, or transformation for the user → use the **CLI path** with the `runapi` binary.
- Building an app, backend, worker, library, or production codebase → use the **SDK integration path**.

## CLI path

The `runapi` binary is the runtime dependency. Authenticate with `runapi login` (browser) or set `RUNAPI_API_KEY`; a saved CLI config also works — no required environment variable.

Inspect the available actions and request fields with CLI help:

```shell
runapi grok-imagine --help
runapi grok-imagine text-to-video --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi grok-imagine text-to-video --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi grok-imagine text-to-video --async --input-file request.json
runapi wait <task-id> --service grok-imagine --action text-to-video
```

Available actions: `text-to-video`, `image-to-video`, `text-to-image`, `image-to-image`, `extend`, `upscale-image`.

## SDK integration path

When integrating Grok Imagine into an app, backend, worker, or library — not for one-off tasks — use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/grok-imagine`
- Ruby: `runapi-grok_imagine`
- Go: `github.com/runapi-ai/grok-imagine-sdk/go`

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/grok-imagine.md
- Provider comparison: https://runapi.ai/providers/xai.md
- Full model catalog: https://runapi.ai/models.md

## Variants

- [Text to video](https://runapi.ai/models/grok-imagine/text-to-video.md)
- [Image to video](https://runapi.ai/models/grok-imagine/image-to-video.md)
- [Text to image](https://runapi.ai/models/grok-imagine/text-to-image.md)
- [Image to image](https://runapi.ai/models/grok-imagine/image-to-image.md)

