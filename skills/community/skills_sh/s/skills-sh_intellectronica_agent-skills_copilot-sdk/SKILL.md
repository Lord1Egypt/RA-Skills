---
name: copilot-sdk
description: This skill helps with GitHub Copilot SDK work across Node.js/TypeScript, Python, Go, .NET, and Java. It covers setup, authentication, permissions, streaming events, custom tools, custom agents, MCP servers, hooks, skills, and session persistence.
---

# GitHub Copilot SDK

## Overview

The GitHub Copilot SDK exposes the same Copilot CLI agent runtime over JSON-RPC, so apps can drive Copilot programmatically instead of building their own orchestration layer.

**Status:** Public preview  
**SDKs:** Node.js/TypeScript, Python, Go, .NET, Java  
**Architecture:** Application -> SDK client -> JSON-RPC -> Copilot CLI

## How to use this skill

When helping with the Copilot SDK:

1. Prefer the official docs index and the language-specific README over memory.
2. Treat the top-level SDK README plus `docs/` as the source of truth for shared behavior.
3. Call out preview status when stability or breaking changes matter.
4. Avoid hardcoding model lists when runtime discovery via `listModels()` is available.
5. Watch for stale guidance around permissions, lifecycle methods, and event names.

## Current source of truth

### Core SDK docs

- [GitHub Copilot SDK repository](https://github.com/github/copilot-sdk)
- [Documentation index](https://github.com/github/copilot-sdk/blob/main/docs/index.md)
- [Getting started guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md)
- [Setup guides](https://github.com/github/copilot-sdk/blob/main/docs/setup/index.md)
- [Local CLI setup](https://github.com/github/copilot-sdk/blob/main/docs/setup/local-cli.md)
- [Bundled CLI setup](https://github.com/github/copilot-sdk/blob/main/docs/setup/bundled-cli.md)
- [Backend services setup](https://github.com/github/copilot-sdk/blob/main/docs/setup/backend-services.md)
- [Scaling and multi-tenancy](https://github.com/github/copilot-sdk/blob/main/docs/setup/scaling.md)
- [Azure Managed Identity with BYOK](https://github.com/github/copilot-sdk/blob/main/docs/setup/azure-managed-identity.md)
- [Authentication](https://github.com/github/copilot-sdk/blob/main/docs/auth/index.md)
- [BYOK](https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md)
- [Features index](https://github.com/github/copilot-sdk/blob/main/docs/features/index.md)
- [Image input](https://github.com/github/copilot-sdk/blob/main/docs/features/image-input.md)
- [Steering and queueing](https://github.com/github/copilot-sdk/blob/main/docs/features/steering-and-queueing.md)
- [OpenTelemetry instrumentation](https://github.com/github/copilot-sdk/blob/main/docs/observability/opentelemetry.md)
- [Troubleshooting](https://github.com/github/copilot-sdk/blob/main/docs/troubleshooting/debugging.md)
- [SDK/CLI compatibility](https://github.com/github/copilot-sdk/blob/main/docs/troubleshooting/compatibility.md)

### Language-specific docs

- [Node.js / TypeScript README](https://github.com/github/copilot-sdk/blob/main/nodejs/README.md)
- [Python README](https://github.com/github/copilot-sdk/blob/main/python/README.md)
- [Go README](https://github.com/github/copilot-sdk/blob/main/go/README.md)
- [.NET README](https://github.com/github/copilot-sdk/blob/main/dotnet/README.md)
- [Java SDK repository](https://github.com/github/copilot-sdk-java)

### Copilot CLI and GitHub Docs

- [About GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli)
- [Using GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)
- [Custom agents configuration reference](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Enhancing agent mode with MCP](https://docs.github.com/en/copilot/tutorials/enhance-agent-mode-with-mcp)
- [Supported models](https://docs.github.com/en/copilot/reference/ai-models/supported-models)

### Recipes and examples

- [Copilot SDK cookbook](https://github.com/github/awesome-copilot/blob/main/cookbook/copilot-sdk/README.md)
- [Node.js samples](https://github.com/github/copilot-sdk/tree/main/nodejs/samples)
- [Go samples](https://github.com/github/copilot-sdk/tree/main/go/samples)
- [.NET samples](https://github.com/github/copilot-sdk/tree/main/dotnet/samples)

---

## High-value facts

### Authentication and prerequisites

- A GitHub Copilot subscription is required for normal SDK use.
- BYOK is supported and does **not** require GitHub Copilot authentication.
- Node.js, Python, and .NET bundle the Copilot CLI automatically.
- Go can use an installed CLI or embed/bundle one with the `go tool bundler` workflow.
- Java currently lives in `github/copilot-sdk-java` and expects the CLI to be installed separately.
- Azure Managed Identity / Entra auth is supported as a documented BYOK pattern by passing short-lived bearer tokens from `DefaultAzureCredential`.

### Permissions

- The SDK uses a deny-by-default permission model.
- In practice, create/resume flows should provide an explicit permission handler such as:
  - TypeScript: `approveAll`
  - Python: `PermissionHandler.approve_all`
  - Go: `copilot.PermissionHandler.ApproveAll`
  - .NET: `PermissionHandler.ApproveAll`
  - Java: `PermissionHandler.APPROVE_ALL`

### Session lifecycle

- Preferred cleanup method: `disconnect()`
- Deprecated cleanup method: `destroy()`
- To resume sessions reliably, provide your own `sessionId` when creating them.
- BYOK provider configuration must be provided again when resuming because keys are not persisted.

### Transport and deployment

- Default transport is stdio with an SDK-managed CLI process.
- You can connect to an external headless CLI server via `cliUrl`.
- Current external server docs use:

```bash
copilot --headless --port 4321
```

### Models

- Do not hardcode model support unless the user specifically needs a fixed list.
- Prefer `client.listModels()` and the official supported-models page.
- `reasoningEffort` exists for models that support it.

---

## Installation

| SDK | Install |
| --- | --- |
| Node.js / TypeScript | `npm install @github/copilot-sdk` |
| Python | `pip install github-copilot-sdk` |
| Go | `go get github.com/github/copilot-sdk/go` |
| .NET | `dotnet add package GitHub.Copilot.SDK` |
| Java | Maven/Gradle package `com.github:copilot-sdk-java` |

## Setup and deployment choices

Pick the setup that matches the application shape:

- **Local CLI** - simplest path for personal tools and development.
- **Bundled CLI** - ship a CLI binary with your app for desktop/distributable tooling.
- **Backend services** - run the CLI in headless mode and connect with `cliUrl`.
- **Scaling and multi-tenancy** - shared CLI vs CLI-per-user, shared storage, and session locking.
- **Azure Managed Identity** - use BYOK with short-lived bearer tokens instead of static API keys when Azure auth is the real requirement.

## Quick start pattern

Use the same mental model in every language:

1. Create/start the client.
2. Create a session with a permission handler.
3. Register event handlers before `send()` if you need streaming or progress.
4. Send with `send()` or `sendAndWait()`.
5. Wait for `session.idle` or the returned final message.
6. `disconnect()` the session and stop/dispose the client.

### TypeScript example

```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();

const session = await client.createSession({
  model: "gpt-5",
  streaming: true,
  onPermissionRequest: approveAll,
});

session.on("assistant.message_delta", (event) => {
  process.stdout.write(event.data.deltaContent ?? "");
});

await session.sendAndWait({ prompt: "What is 2+2?" });

await session.disconnect();
await client.stop();
```

---

## Core capabilities to remember

### Client and session APIs

Common operations across SDKs:

- Client lifecycle: `start()`, `stop()`, `forceStop()`
- Session lifecycle: `createSession()`, `resumeSession()`, `disconnect()`
- Messaging: `send()`, `sendAndWait()`, `abort()`, `getMessages()`
- Discovery: `listModels()`, `listSessions()`, `getStatus()` / `ping()`

### Events and streaming

- Final assistant output arrives in `assistant.message`.
- Streaming text arrives in `assistant.message_delta`.
- `session.idle` is the reliable "turn complete" signal.
- The event system now includes reasoning, tool progress, permission, elicitation, sub-agent, and skill events.

See `references/event-system.md`.

### Custom tools

- Node uses `defineTool(...)` with Zod or raw JSON Schema.
- Python uses `@define_tool` with Pydantic models.
- Go prefers `DefineTool(...)`.
- .NET uses `AIFunctionFactory.Create(...)`.
- Overriding built-ins always requires explicit opt-in:
  - TypeScript: `overridesBuiltInTool: true`
  - Python: `overrides_built_in_tool=True`
  - Go: `OverridesBuiltInTool = true`
  - .NET: `AdditionalProperties["is_override"] = true`
- Custom tools can also opt into `skipPermission`.

### Custom agents, MCP, hooks, and skills

- `customAgents` lets you define sub-agents per session.
- `mcpServers` attaches local or remote MCP servers.
- Hooks provide control points such as `onPreToolUse`, `onPostToolUse`, `onUserPromptSubmitted`, and lifecycle/error hooks.
- Skills are loaded with `skillDirectories`; disable selectively with `disabledSkills`.

See `references/cli-agents-mcp.md`.

### Attachments, commands, and interaction

- Sessions can send file, directory, and image attachments.
- Image input supports both file and blob attachments, and vision should be checked through model capabilities.
- In-flight messaging supports `mode: "immediate"` for steering and `mode: "enqueue"` for queueing.
- The SDK can register custom slash `commands`.
- Apps can answer user questions with `onUserInputRequest`.
- Rich UI prompts are available through elicitation handlers and `session.ui` when the connected client supports them.

### Telemetry and observability

- The SDK supports OpenTelemetry configuration through `TelemetryConfig`.
- Trace context propagation is built in, with Node using an explicit `onGetTraceContext` callback for outbound propagation.

### Persistence and long-running work

- Use a stable `sessionId` for resumable sessions.
- Use `infiniteSessions` for long-running workflows that may need compaction.
- Session state is stored under `~/.copilot/session-state/` unless configuration overrides it.

### SDK vs. CLI-only features

- The SDK exposes programmatic surfaces for sessions, models, plans, mode switching, workspace files, custom agents, hooks, MCP, skills, and telemetry.
- Many terminal UX features remain CLI-only, such as most slash-command workflows, interactive pickers, and export/share commands.
- When translating a CLI workflow into app code, check the compatibility guide before assuming a slash command has an SDK equivalent.

---

## Language conventions

| Concept | TypeScript | Python | Go | .NET | Java |
| --- | --- | --- | --- | --- | --- |
| Create session | `createSession()` | `create_session()` | `CreateSession()` | `CreateSessionAsync()` | `createSession()` |
| Resume session | `resumeSession()` | `resume_session()` | `ResumeSession()` | `ResumeSessionAsync()` | `resumeSession()` |
| Final content | `event.data.content` | `event.data.content` | `*event.Data.Content` | `evt.Data.Content` | `event.getData().content()` |
| Delta content | `event.data.deltaContent` | `event.data.delta_content` | `*event.Data.DeltaContent` | `evt.Data.DeltaContent` | `event.getData().deltaContent()` |
| Skills field | `skillDirectories` | `skill_directories` | `SkillDirectories` | `SkillDirectories` | `setSkillDirectories(...)` |

---

## Common gotchas

- The SDK is **public preview**, so older examples drift quickly.
- Hardcoded model tables get stale; prefer runtime discovery.
- `destroy()` still appears in older examples but `disconnect()` is the current method.
- A missing permission handler causes confusion fast; treat it as required for real sessions.
- `assistant.message` and `assistant.message_delta` use `event.data.*`, not top-level `event.content`.
- Streaming/event subscriptions should be attached before `send()`.
- Session resumption without a caller-provided `sessionId` is awkward to operationalize.

---

## Local reference files in this skill

- `references/working-examples.md` - current starter examples, including tools and resume patterns
- `references/event-system.md` - event names, lifecycle, and language access patterns
- `references/cli-agents-mcp.md` - custom agents, skills, MCP, headless CLI, and config locations
- `references/troubleshooting.md` - common failures, debug logging, auth, permissions, and transport issues
