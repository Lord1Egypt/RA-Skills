---
name: runway-aleph
description: Generate and edit video with Runway Aleph through RunAPI. Use when the user asks an agent to create, edit, or transform video with Runway Aleph. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/runway-aleph.md
provider_page: https://runapi.ai/providers/runway.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/runway-aleph
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

# Runway Aleph on RunAPI

Generate and edit video with Runway Aleph through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Routing decision

- One-off generation, editing, or transformation for the user → use the **CLI path** with the `runapi` binary.
- Building an app, backend, worker, library, or production codebase → use the **SDK integration path**.

## CLI path

The `runapi` binary is the runtime dependency. Authenticate with `runapi login` (browser) or set `RUNAPI_API_KEY`; a saved CLI config also works — no required environment variable.

Inspect the available actions and request fields with CLI help:

```shell
runapi runway-aleph --help
runapi runway-aleph video-to-video --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi runway-aleph video-to-video --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi runway-aleph video-to-video --async --input-file request.json
runapi wait <task-id> --service runway-aleph --action video-to-video
```

Available actions: `video-to-video`.

## SDK integration path

When integrating Runway Aleph into an app, backend, worker, or library — not for one-off tasks — use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/runway-aleph`
- Ruby: `runapi-runway_aleph`
- Go: `github.com/runapi-ai/runway-aleph-sdk/go`

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/runway-aleph.md
- Provider comparison: https://runapi.ai/providers/runway.md
- Full model catalog: https://runapi.ai/models.md

