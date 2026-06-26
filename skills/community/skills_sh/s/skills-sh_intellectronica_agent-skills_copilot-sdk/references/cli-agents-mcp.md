# CLI, Custom Agents, Skills, and MCP

This file covers the overlap between the Copilot SDK and Copilot CLI configuration.

## First distinction: SDK config vs CLI config

There are two related but different ways to shape Copilot behavior:

1. **SDK session configuration** - pass options like `customAgents`, `mcpServers`, `skillDirectories`, `disabledSkills`, and hooks directly when creating a session.
2. **Copilot CLI configuration** - use local config files, custom agent profiles, and the CLI UI/commands.

If you are building an application on the SDK, prefer SDK session configuration first and use CLI-level config when you want reusable local behavior outside your app.

## Copilot CLI config locations

By default the CLI stores config under `~/.copilot/`. This location can be overridden with `COPILOT_HOME`.

Common files and directories:

- `config.json` - general CLI config
- `mcp-config.json` - MCP server definitions
- `agents/` - user-level custom agent profiles
- `session-state/` - resumable sessions, plans, and session artifacts

## Headless CLI server

The SDK can manage the CLI for you, or you can connect to a separately running server.

### Start a headless CLI

```bash
copilot --headless --port 4321
```

### Connect from the SDK

```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

const client = new CopilotClient({
  cliUrl: "localhost:4321",
});

const session = await client.createSession({
  onPermissionRequest: approveAll,
});
```

Use this when you want persistent logs, resource sharing, or a separately managed runtime.

## SDK custom agents

Use `customAgents` in session config to define sub-agents inside your app.

### TypeScript example

```typescript
const session = await client.createSession({
  model: "gpt-4.1",
  onPermissionRequest: approveAll,
  customAgents: [
    {
      name: "researcher",
      displayName: "Research Agent",
      description: "Explores codebases and answers questions with read-only tools",
      tools: ["grep", "glob", "view"],
      prompt: "Analyze code and answer questions. Do not modify files.",
    },
    {
      name: "editor",
      displayName: "Editor Agent",
      description: "Makes targeted code changes",
      tools: ["view", "edit", "bash"],
      prompt: "Make minimal, surgical changes only.",
    },
  ],
});
```

Useful fields include:

| Field | Purpose |
| --- | --- |
| `name` | Stable identifier |
| `displayName` | UI-friendly label |
| `description` | Helps the runtime infer when to use the agent |
| `tools` | Restricts tools for that agent |
| `prompt` | Agent-specific instructions |
| `mcpServers` | Agent-local MCP config |
| `infer` | Controls auto-selection behavior |

## CLI custom agent profiles

Copilot CLI also supports standalone agent profile files with YAML frontmatter and Markdown instructions.

Useful docs:

- [Custom agents configuration reference](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Using GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)

Common profile fields:

| Field | Purpose |
| --- | --- |
| `name` | Optional display name |
| `description` | Required description |
| `tools` | Tool filter |
| `target` | Environment target |
| `infer` | Whether it can be auto-selected |
| `mcp-servers` | Embedded MCP server definitions |

Useful tool aliases in CLI docs include:

- `execute`
- `read`
- `edit`
- `search`
- `agent`
- `web`
- `todo`

## Skills in the SDK

Skills are loaded from directories containing child folders with `SKILL.md`.

### TypeScript example

```typescript
const session = await client.createSession({
  model: "gpt-4.1",
  onPermissionRequest: approveAll,
  skillDirectories: ["./skills"],
  disabledSkills: ["deprecated-tooling"],
});
```

Key points:

- `skillDirectories` points to the parent directory.
- The runtime discovers immediate subdirectories containing `SKILL.md`.
- `disabledSkills` disables by skill name or directory name.

## MCP servers

Attach MCP servers with `mcpServers` in session config or define them in CLI config.

Supported server shapes:

| Type | Meaning |
| --- | --- |
| `local` / `stdio` | Spawn a local subprocess |
| `http` / `sse` | Connect to a remote MCP server |

### Local MCP example

```typescript
const session = await client.createSession({
  model: "gpt-5",
  onPermissionRequest: approveAll,
  mcpServers: {
    filesystem: {
      type: "local",
      command: "npx",
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      tools: ["*"],
    },
  },
});
```

### Remote MCP example

```typescript
mcpServers: {
  github: {
    type: "http",
    url: "https://api.githubcopilot.com/mcp/",
    headers: {
      Authorization: "Bearer ${TOKEN}",
    },
    tools: ["*"],
  },
}
```

### Tool filtering rules

- `tools: ["*"]` enables all tools from that server.
- `tools: []` disables all tools from that server.
- `tools: ["tool-a", "tool-b"]` exposes only those tools.

## CLI-managed MCP

The CLI includes built-in support for configuring MCP servers interactively:

```text
/mcp add
```

That writes to `mcp-config.json` under `~/.copilot/` unless `COPILOT_HOME` overrides it.

The CLI also ships with the GitHub MCP server already configured, which is why GitHub repository and workflow operations are often available out of the box in Copilot CLI sessions.

## When to use what

| Need | Prefer |
| --- | --- |
| App-specific agents and tools | SDK session config |
| App-specific skill loading | SDK `skillDirectories` |
| Reusable local MCP setup for the CLI | `~/.copilot/mcp-config.json` |
| Reusable custom agent profile outside app code | CLI agent profile files |
| Shared server or advanced debugging | headless CLI + `cliUrl` |

## Gotchas

- SDK and CLI examples often look similar but are not the same API surface.
- MCP tools still go through permission and tool filtering.
- When a server starts but no tools appear, check `tools` first.
- If sub-agent behavior is inconsistent, improve agent `description` text and tool scoping.
