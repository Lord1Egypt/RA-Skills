# VS Code Custom Agent Complete Format Reference

## Complete Frontmatter Fields

```yaml
---
name: string                       # Agent name (optional, defaults to filename)
description: string                # Brief description
argument-hint: string              # Input box placeholder
model: string | string[]           # Model, format "Model (vendor)", array attempts in order
tools: string[]                    # Tool list, MCP services use <server>/*
agents: string[] | "*"             # Sub-agents, * for all, [] to prohibit
user-invocable: boolean            # Whether to show in dropdown (default true)
disable-model-invocation: boolean  # Prevent being called by other agents (default false)
target: "vscode" | "github-copilot"
mcp-servers: array                 # GitHub Copilot MCP config
handoffs: array                    # Handoff chain
  - label: string                  #   Button text
    agent: string                  #   Target agent
    prompt: string                 #   Pre-filled prompt
    send: boolean                  #   Auto-send (default false)
    model: string                  #   Specify model
hooks: object                      # (Preview) Agent-level hooks
  PostToolUse: array
    - type: "command"
      command: string
```

## Tool List

### Built-in Tools
- `search/codebase` — Search codebase
- `search/usages` — Search symbol usages
- `web/fetch` — Fetch web content
- `web/search` — Web search
- `edit` — Edit files
- `read/terminalLastCommand` — Read most recent terminal output
- `agent` — Call sub-agent

### MCP Tools
- `<server-name>/<tool-name>` — Specify a tool
- `<server-name>/*` — All tools from that service

### Tool References
Use the `#tool:<tool-name>` syntax in the body, e.g., `#tool:web/fetch`

## Creation Methods

1. **Chat command:** `/agents` → Configure Custom Agents → New Agent
2. **Command palette:** `Chat: New Custom Agent`
3. **AI generation:** `/create-agent` describe the role
4. **Extract from conversation:** "make an agent for this kind of task"

## Management

- **Show/Hide:** Agent Customizations editor → Eye icon
- **Delete:** Delete the `.agent.md` file or trash icon in editor
- **View source:** Hover over agent in editor → tooltip shows path

## Priority

Prompt file tools take precedence over agent tools.

## Organization Sharing

```json
{
  "github.copilot.chat.organizationCustomAgents.enabled": true
}
```

Organization-level agents are defined by GitHub administrators at the organization level and are automatically discovered.

## Monorepo

Enable `chat.useCustomizationsInParentRepositories` to discover agents from the parent repository root.

## FAQ

- **Legacy `.chatmode.md`:** Rename to `.agent.md` + place in correct directory
- **Sub-agent nesting:** Enable `chat.subagents.allowInvocationsFromSubagents`
- **Parent repo discovery:** Enable `chat.useCustomizationsInParentRepositories`