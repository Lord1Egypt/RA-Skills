---
name: vscode-agent-creator
description: Create VS Code Copilot custom Agent (.agent.md) files.
---

# VS Code Copilot Custom Agent Creator

## Trigger Scenarios

Use when the user needs to create a custom Copilot Agent in VS Code, configure a specialized AI role, define handoff workflows, set tool permissions, or write agent instructions. Trigger keywords include "create agent", "custom agent", "VS Code agent", "copilot agent", "agent.md", "handoff", etc.

## ⚡ Workflow

1. **Understand requirements** → Ask user about: agent role, available tools, whether handoff chain is needed
2. **Generate file** → Create `.agent.md` file following the template
3. **Placement** → Tell user to place it in `.github/agents/` (workspace) or `~/.copilot/agents/` (user-level)

## File Locations

| Scope | Path |
|-------|------|
| Workspace | `.github/agents/<name>.agent.md` |
| Claude format | `.claude/agents/<name>.md` |
| User-level | `~/.copilot/agents/<name>.agent.md` |

> Workspace agents can have additional search paths configured via `chat.agentFilesLocations`

## File Structure

```markdown
---
name: Agent Name                    # Optional, defaults to filename
description: Brief description      # Displayed in input placeholder
argument-hint: Argument hint        # Optional, guides user input
model: GPT-5.2 (copilot)            # Optional, string or array (attempt in order)
tools:                              # Tool list
  - search/codebase
  - web/fetch
  - edit
agents:                             # Available sub-agents, * for all, [] to prohibit
  - Researcher
user-invocable: true                # Optional, whether to appear in dropdown (default true)
disable-model-invocation: false     # Optional, prevent being called as sub-agent by other agents
handoffs:                           # Optional, handoff chain
  - label: Button text
    agent: Target agent
    prompt: Pre-filled prompt
    send: false                     # Optional, whether to auto-send
    model: GPT-5.2 (copilot)        # Optional
hooks:                              # Optional (Preview), scoped hooks
  PostToolUse:
    - type: command
      command: "./scripts/format.sh"
---

# Agent Instruction Body

Write the agent's behavior guidelines, workflow, output format, etc. here.
Supports Markdown links to other files.
Reference tools with: #tool:web/fetch
```

## Frontmatter Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent name |
| `description` | string | Brief description |
| `argument-hint` | string | Input box placeholder text |
| `model` | string/array | Model name (`Model (vendor)` format), array attempts in order |
| `tools` | array | Available tools list. MCP services use `<server>/*` |
| `agents` | array | Available sub-agent list, `*` = all, `[]` = prohibit |
| `user-invocable` | bool | Whether to appear in dropdown (default true) |
| `disable-model-invocation` | bool | Prevent being called by other agents (default false) |
| `target` | string | `vscode` or `github-copilot` |
| `mcp-servers` | array | MCP service config for GitHub Copilot |
| `handoffs` | array | Handoff chain definition |
| `handoffs.label` | string | Button text |
| `handoffs.agent` | string | Target agent identifier |
| `handoffs.prompt` | string | Pre-filled prompt |
| `handoffs.send` | bool | Auto-send (default false) |
| `handoffs.model` | string | Specify model |
| `hooks` | object | (Preview) Agent-level hooks, requires `chat.useCustomAgentHooks` |

## Handoff Workflow

Handoffs display buttons after the agent responds, allowing one-click switching with pre-filled context:

```
Plan → Implementation → Code Review
```

**Example:**
```yaml
handoffs:
  - label: Start Implementation
    agent: implementer
    prompt: Implement the plan above.
    send: false
  - label: Review Code
    agent: reviewer
    prompt: Review the changes for security and quality.
```

## Built-in Tool Reference

| Tool | Description |
|------|-------------|
| `search/codebase` | Search codebase |
| `search/usages` | Search usages |
| `web/fetch` | Fetch web page |
| `web/search` | Web search |
| `edit` | Edit files |
| `read/terminalLastCommand` | Read terminal output |
| `agent` | Call sub-agent |

> Reference tools using `#tool:<name>` syntax, e.g., `#tool:web/fetch`

## Common Agent Templates

### Planner Agent
```yaml
---
name: Planner
description: Generate implementation plans
tools: ['search/codebase', 'web/fetch', 'search/usages']
model: ['Claude Opus 4.5', 'GPT-5.2']
handoffs:
  - label: Implement
    agent: implementer
    prompt: Implement the plan above.
---
You are in planning mode. Generate a detailed plan with:
- Overview, Requirements, Implementation Steps, Testing.
Do NOT make code edits.
```

### Code Reviewer Agent
```yaml
---
name: Reviewer
description: Review code for quality and security
tools: ['search/codebase', 'web/fetch']
---
Review code changes for:
- Security vulnerabilities
- Code quality issues
- Performance concerns
- Adherence to project conventions
```

### Implementer Agent
```yaml
---
name: Implementer
description: Implement code changes
tools: ['edit', 'read/terminalLastCommand', 'search/codebase']
---
Implement changes following existing code patterns.
Make minimal, focused edits. Run tests after changes.
```

## Creation Process

1. In Chat, type `/agents` or click the gear icon → Agent Customizations editor
2. Select New Agent (Workspace) or New Agent (User)
3. Enter filename → `.agent.md` template generated
4. Fill in frontmatter + instruction body
5. Or use `/create-agent` to have AI generate based on description

## Claude Format Compatibility

`.claude/agents/*.md` supports Claude-specific fields:
- `tools`: Comma-separated string (`"Read, Grep, Glob, Bash"`)
- `disallowedTools`: List of prohibited tools

VS Code automatically maps Claude tool names to VS Code tools.

## Organization-level Agents

Enable `github.copilot.chat.organizationCustomAgents.enabled: true` to automatically discover organization-level agents.

See: [references/agent-format.md](references/agent-format.md)