---
name: ideogram-v3
description: Generate and edit images with Ideogram V3 through RunAPI. Use when the user asks an agent to create, edit, or transform images with Ideogram V3. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/ideogram-v3.md
provider_page: https://runapi.ai/providers/ideogram.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/ideogram-v3
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

# Ideogram V3 on RunAPI

Generate and edit images with Ideogram V3 through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Routing decision

- One-off generation, editing, or transformation for the user → use the **CLI path** with the `runapi` binary.
- Building an app, backend, worker, library, or production codebase → use the **SDK integration path**.

## CLI path

The `runapi` binary is the runtime dependency. Authenticate with `runapi login` (browser) or set `RUNAPI_API_KEY`; a saved CLI config also works — no required environment variable.

Inspect the available actions and request fields with CLI help:

```shell
runapi ideogram-v3 --help
runapi ideogram-v3 text-to-image --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi ideogram-v3 text-to-image --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi ideogram-v3 text-to-image --async --input-file request.json
runapi wait <task-id> --service ideogram-v3 --action text-to-image
```

Available actions: `text-to-image`, `edit-image`, `remix-image`.

## SDK integration path

When integrating Ideogram V3 into an app, backend, worker, or library — not for one-off tasks — use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/ideogram-v3`
- Ruby: `runapi-ideogram_v3`
- Go: `github.com/runapi-ai/ideogram-v3-sdk/go`

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/ideogram-v3.md
- Provider comparison: https://runapi.ai/providers/ideogram.md
- Full model catalog: https://runapi.ai/models.md

## Variants

- [Text to image](https://runapi.ai/models/ideogram-v3/text-to-image.md)
- [Edit](https://runapi.ai/models/ideogram-v3/edit.md)
- [Remix](https://runapi.ai/models/ideogram-v3/remix.md)

