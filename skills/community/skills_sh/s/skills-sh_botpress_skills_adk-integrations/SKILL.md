---
name: adk-integrations
description: guidelines for discovering, adding, configuring, and using Botpress integrations in ADK projects - use when users ask about connecting services, managing dependencies, or using integration actions
license: MIT
---

# ADK Integration Management

Use this skill when helping users discover, add, configure, and use Botpress integrations in their ADK projects.

## When to Use This Skill

Activate this skill when users:

- Ask about integrations ("How do I add Slack?", "What integrations are available?")
- Want to connect an external service (Slack, WhatsApp, Linear, etc.)
- Mention `adk add`, `adk search`, `adk info`, or `adk list`
- Ask about `agent.config.ts` dependencies or the `dependencies.integrations` block
- Need help configuring an integration (OAuth, API keys, Dev Console)
- Ask about calling integration actions in code (`actions.slack.*`, etc.)
- Mention specific platforms or services they want their agent to interact with
- Get errors related to integration registration or configuration

## Available Documentation

| File | Description |
|------|-------------|
| [references/discovery.md](./references/discovery.md) | Finding integrations: `adk search`, `adk list`, `adk info` with all flags |
| [references/lifecycle.md](./references/lifecycle.md) | End-to-end walkthrough: discover, add, configure, use in code |
| [references/configuration.md](./references/configuration.md) | Configuration types: no-config, optional, OAuth, API key, sandbox |
| [references/common-integrations.md](./references/common-integrations.md) | Quick reference for chat, webchat, browser, slack, whatsapp, linear, webhook |

## How to Answer

1. **Start with CLI commands** — Use `adk search`, `adk info`, `adk list` to get live data before suggesting anything. Run these via the Bash tool.
2. **Confirm before running `adk add`** — Always ask the user before adding an integration to their project.
3. **Always specify version** — Use `adk add <name>@<version>` rather than just `adk add <name>`.
4. **Explain configuration requirements** — After adding, tell the user what configuration is needed (OAuth link, API key, etc.) based on `adk info --format json` output.
5. **Point to Dev Console** — OAuth flows and credential entry happen in the Botpress Dev Console, not in code.

## CLI Quick Reference

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `adk search <query>` | Search integrations by keyword | `--format json`, `--limit <number>` (default: 20) |
| `adk list --available` | Browse all Hub integrations | `--format json`, `--limit <number>` (default: 50) |
| `adk list` | Show installed dependencies | `--format json`, `--limit <number>` (default: 50) |
| `adk info <name>` | Full integration details (integrations only, not plugins) | `--actions`, `--channels`, `--events`, `--full`, `--format json` |
| `adk add <name>@<version>` | Add integration to project | `--alias <name>`, `--format json` |
| `adk add plugin:<name>@<version>` | Add plugin to project | `--alias <name>`, `--format json` |
| `adk remove <name>` | Remove integration, plugin, or interface | `--format json` |
| `adk upgrade [name]` | Upgrade dependency (or all interactively) | `--format json` |

Use `--format json` for CLI inspection.

## Critical Patterns

### Always Use the CLI

```bash
# CORRECT - Use adk add
adk add slack@3.0.0
adk add plugin:desk-hitl@1.0.0
adk add interface:translator@1.0.0

# WRONG - Never manually edit agent.config.ts dependencies
# Don't hand-write entries in the dependencies block
```

### Version Pinning

```bash
# CORRECT - Pin to specific version
adk add browser@0.8.6

# RISKY - Resolves to latest, may change unexpectedly
adk add browser
```

### Accessing Integration Actions

```typescript
// CORRECT - Import from @botpress/runtime, use alias from agent.config.ts
import { actions } from '@botpress/runtime'
await actions.slack.sendMessage({ channel: '#general', text: 'Hello' })

// The alias in agent.config.ts determines the accessor name
// { browser: { version: 'browser@0.8.6', enabled: true } }
await actions.browser.webSearch({ query: 'search term' })
```

### Inspecting Config Requirements

```bash
# Use --format json to check what configuration an integration needs
adk info slack --format json

# Look at configuration.schema for required fields
# Look at configuration.identifier for OAuth
# Look at configurations for alternative config modes
```

## Examples of Questions This Skill Answers

### Beginner

- "What integrations are available?"
- "How do I add Slack to my agent?"
- "What is the browser integration?"

### Intermediate

- "How do I configure WhatsApp in sandbox mode?"
- "What actions does the webchat integration provide?"
- "How do I call a Linear action from my workflow?"
- "What's the difference between chat and webchat?"

### Advanced

- "How do I use a private workspace integration?"
- "What does `registration_pending` status mean?"
- "How do I alias an integration for cleaner code?"
- "How do I inspect an integration's config schema programmatically?"
