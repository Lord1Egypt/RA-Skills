---
name: veo-3.1
description: Generate and edit video with Veo 3 through RunAPI. Use when the user asks an agent to create, edit, or transform video with Veo 3. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/veo-3.1.md
provider_page: https://runapi.ai/providers/google.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/veo-3.1
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

# Veo 3 on RunAPI

Generate and edit video with Veo 3 through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Routing decision

- One-off generation, editing, or transformation for the user → use the **CLI path** with the `runapi` binary.
- Building an app, backend, worker, library, or production codebase → use the **SDK integration path**.

## CLI path

The `runapi` binary is the runtime dependency. Authenticate with `runapi login` (browser) or set `RUNAPI_API_KEY`; a saved CLI config also works — no required environment variable.

Inspect the available actions and request fields with CLI help:

```shell
runapi veo-3-1 --help
runapi veo-3-1 text-to-video --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi veo-3-1 text-to-video --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi veo-3-1 text-to-video --async --input-file request.json
runapi wait <task-id> --service veo-3-1 --action text-to-video
```

Available actions: `text-to-video`, `extend-video`, `upscale-video`.

## SDK integration path

When integrating Veo 3 into an app, backend, worker, or library — not for one-off tasks — use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/veo-3.1`
- Ruby: `runapi-veo_3_1`
- Go: `github.com/runapi-ai/veo-3.1-sdk/go`

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/veo-3.1.md
- Provider comparison: https://runapi.ai/providers/google.md
- Full model catalog: https://runapi.ai/models.md

## Variants

- [Veo 3](https://runapi.ai/models/veo-3.1/veo-3.md)
- [Veo 3 fast](https://runapi.ai/models/veo-3.1/fast.md)

