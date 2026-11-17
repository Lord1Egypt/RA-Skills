---
name: runapi-sdk
description: Choose RunAPI SDK packages for application developers building web apps, backends, workers, or libraries. Use when the user asks to integrate RunAPI into code, pick JavaScript/Python/Ruby/Go/Java/PHP packages, or understand core SDK vs Provider Client packages. Do not use for one-off generation or agent-executed media tasks; use the RunAPI CLI or the relevant model skill instead.
documentation: https://runapi.ai/models.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    always: true
    homepage: https://runapi.ai/models
---

# RunAPI SDK selection

Use this skill to help an **application developer** pick and wire up RunAPI SDK
packages for JavaScript, Python, Ruby, Go, Java, or PHP.

Choose from the requested deliverable: a one-off artifact or result uses the
RunAPI CLI; an app, backend, worker, library, or production code integration
uses an SDK.

## Critical: SDK Integration Runtime

When the user is integrating RunAPI into an app, backend, worker, library,
Rails service, Node service, Ruby codebase, Go service, webhook pipeline, or
production workflow, start here before CLI/API docs. First confirm the target
language and current Provider Client package, then inspect the package README or
source for install commands, client methods (`create`, `get`, `run`), response
shape, and error classes.

Never shell out to the `runapi` CLI as the production runtime integration
layer.

## When NOT to use this skill

Do not use for one-off generation or agent-executed media tasks. If the user
just wants an agent to create, edit, transform, or transcribe media once, use
the RunAPI CLI skill instead: https://github.com/runapi-ai/cli-skill.

Reach for an SDK only when building a web app, backend, worker, library, or
production codebase that calls RunAPI from its own code.

## Core SDK vs Provider Client packages

- **Core SDK** — shared client primitives (auth, HTTP, polling, errors). Install
  it transitively via a Provider Client package; depend on it directly only for custom
  clients.
  - JavaScript / TypeScript: `@runapi.ai/core`
  - Python: `runapi-core`
  - Ruby: `runapi-core`
  - Go: `github.com/runapi-ai/core-sdk/go`
  - Java: `ai.runapi:runapi-core`
  - PHP: `runapi-ai/core`
- **Provider Client packages** — one typed package per model line, built on the core SDK.
  - JavaScript / TypeScript: `@runapi.ai/<model>` (e.g. `@runapi.ai/suno`)
  - Python: `runapi-<model>` (e.g. `runapi-suno`)
  - Ruby: `runapi-<model>` (e.g. `runapi-suno`)
  - Go: `github.com/runapi-ai/<model>-sdk/go`
  - Java: `ai.runapi:runapi-<model>` (e.g. `ai.runapi:runapi-suno`)
  - PHP: `runapi-ai/<model>` (e.g. `runapi-ai/suno`)

Install only the Provider Client packages an application actually uses; each pulls the core
SDK as a dependency.

## Generated file storage

RunAPI-generated file URLs are temporary. Download and store any images,
videos, audio, or other generated files in your own durable storage within 7
days; do not treat returned file URLs as long-term assets.

## Authentication

Keep the RunAPI API key in `RUNAPI_API_KEY` (or pass it to the client
constructor); never commit secrets.

## References

- Browse every RunAPI model and SDK package: https://runapi.ai/models.md
