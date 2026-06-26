---
name: sdk
description: Choose RunAPI SDK packages for application developers building web apps, backends, workers, or libraries. Use when the user asks to integrate RunAPI into code, pick JavaScript/Ruby/Go packages, or understand core-sdk vs model SDKs. Do not use for one-off generation or agent-executed media tasks; use the RunAPI CLI or the relevant model skill instead.
documentation: https://runapi.ai/models.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    always: true
    homepage: https://runapi.ai/models
---

# RunAPI SDK selection

Use this skill to help an **application developer** pick and wire up RunAPI SDK
packages for JavaScript, Ruby, or Go.

## When NOT to use this skill

Do not use for one-off generation or agent-executed media tasks. If the user
just wants an agent to create, edit, transform, or transcribe media once, use
the RunAPI CLI (the `runapi-cli` skill) or the relevant model skill instead —
not an SDK.

Reach for an SDK only when building a web app, backend, worker, library, or
production codebase that calls RunAPI from its own code.

## Core SDK vs model SDKs

- **Core SDK** — shared client primitives (auth, HTTP, polling, errors). Install
  it transitively via a model SDK; depend on it directly only for custom
  clients.
  - JavaScript / TypeScript: `@runapi.ai/core`
  - Ruby: `runapi-core`
  - Go: `github.com/runapi-ai/core-sdk/go`
- **Model SDKs** — one typed package per model line, built on the core SDK.
  - JavaScript / TypeScript: `@runapi.ai/<model>` (e.g. `@runapi.ai/suno`)
  - Ruby: `runapi-<model>` (e.g. `runapi-suno`)
  - Go: `github.com/runapi-ai/<model>-sdk/go`

Install only the model SDKs an application actually uses; each pulls the core
SDK as a dependency.

## Authentication

Keep the RunAPI API key in `RUNAPI_API_KEY` (or pass it to the client
constructor); never commit secrets.

## References

- Browse every RunAPI model and SDK package: https://runapi.ai/models.md
