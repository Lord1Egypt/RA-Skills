---
name: flux-kontext
description: Generate and edit images with Flux Kontext through RunAPI. Use when the user asks an agent to create, edit, or transform images with Flux Kontext. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/flux-kontext.md
provider_page: https://runapi.ai/providers/black-forest-labs.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/flux-kontext
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

# Flux Kontext on RunAPI

Generate and edit images with Flux Kontext through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Routing decision

- One-off generation, editing, or transformation for the user → use the **CLI path** with the `runapi` binary.
- Building an app, backend, worker, library, or production codebase → use the **SDK integration path**.

## CLI path

The `runapi` binary is the runtime dependency. Authenticate with `runapi login` (browser) or set `RUNAPI_API_KEY`; a saved CLI config also works — no required environment variable.

Inspect the available actions and request fields with CLI help:

```shell
runapi flux-kontext --help
runapi flux-kontext text-to-image --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi flux-kontext text-to-image --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi flux-kontext text-to-image --async --input-file request.json
runapi wait <task-id> --service flux-kontext --action text-to-image
```

Available actions: `text-to-image`.

## SDK integration path

When integrating Flux Kontext into an app, backend, worker, or library — not for one-off tasks — use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/flux-kontext`
- Ruby: `runapi-flux_kontext`
- Go: `github.com/runapi-ai/flux-kontext-sdk/go`

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/flux-kontext.md
- Provider comparison: https://runapi.ai/providers/black-forest-labs.md
- Full model catalog: https://runapi.ai/models.md

## Variants

- [Flux Kontext Pro](https://runapi.ai/models/flux-kontext/pro.md)
- [Flux Kontext Max](https://runapi.ai/models/flux-kontext/max.md)

