---
name: adk
description: a set of guidelines to build with Botpress's Agent Development Kit (ADK) - use these whenever you're tasked with building a feature using the ADK
license: MIT
---

# Botpress ADK Guidelines

Use this skill when you've got questions about the Botpress Agent Development Kit (ADK) - like when you're building a feature that involves tables, actions, tools, workflows, conversations, files, knowledge bases, triggers, assets, integrations, plugins, evals, or Zai.

## What is the ADK?

The Botpress ADK is a **convention-based TypeScript framework** where **file structure maps directly to bot behavior**. Place files in the correct directories, and they automatically become available as bot capabilities.

The ADK provides primitives for:

- Actions & Tools (reusable functions and AI-callable tools)
- Workflows (long-running, resumable processes)
- Conversations (message handling)
- Tables (data storage with semantic search)
- Files (file storage with semantic search)
- Knowledge Bases (RAG implementation)
- Triggers (event-driven automation)
- Assets (static files with permanent URLs)
- Integrations (external service connections managed via CLI and dependency snapshots)
- Plugins (reusable agent extensions with interface dependencies)
- **Zai** (production-ready LLM utility library for common AI operations)

### Project Structure (Convention-Based)

Most primitives must be placed in `src/` directory (assets use the `assets/` directory at the project root):

```
/                      # Project root
├── assets/            # Static files → synced to Botpress Cloud with permanent URLs
├── src/
│   ├── actions/       # Strongly-typed functions → auto-registered
│   ├── tools/         # AI-callable tools → available via execute()
│   ├── workflows/     # Long-running processes → resumable/scheduled
│   ├── conversations/ # Message handlers → routes by channel
│   ├── tables/        # Database schemas → auto-created with search
│   ├── triggers/      # Event handlers → subscribe to events
│   ├── knowledge/     # Knowledge bases → RAG with semantic search
│   └── utils/         # Shared helpers (not auto-registered)
├── .adk/
│   └── dependencies/
│       ├── dev.json             # Generated dependency snapshot (dev)
│       ├── prod.json            # Generated dependency snapshot (prod)
│       └── migration.json       # One-way legacy migration marker
├── .agent0/
│   └── capabilities/            # Project-local Agent(0) capability bundle
└── agent.config.ts    # Bot configuration
```

> **Note:** Manage integrations and plugins via the `adk integrations` / `adk plugins` CLI or the Dev Console. Botpress Cloud is the source of truth; `.adk/dependencies/` contains generated local snapshots for fast/offline reads and should not be edited manually. See `integrations.md` and `plugins.md`.

> **Critical:** Files outside `src/` are not discovered. Location = behavior.

## Session Start

The first time you help with an ADK project in a session, silently check the project's health:

1. Run `adk check --format json` and `adk status --format json`. (`adk check` validates primitives but does **not** typecheck — also run `tsc --noEmit` to catch type errors before treating work as done.)
2. If there are errors or warnings (unconfigured integrations, missing models, validation issues), proactively mention them before answering the user's question: _"Before we start — I noticed [issue]. Want me to help fix that?"_
3. Only do this once per session. Don't re-run on every question.

## Available Commands

If the user asks "what can you help with?", "what commands are available?", or invokes `/adk-explain` without arguments, present:

- **Build**: `/adk-init` (scaffold project), `/adk-build` (interview & build a primitive), `/adk-integration` (add services), `/adk-frontend` (build UI)
- **Test & Debug**: `/adk-validate` (check a primitive's schema/types/config), `/adk-test` (invoke a primitive once), `/adk-eval` (write assertion tests), `/adk-debug` (fix issues)
- **Ship**: `/adk-ship` (pre-flight checks + deploy)
- **Document**: `/adk-document` (create, review, update, sync, search)
- **Understand**: `/adk-explain` (explain bot architecture and components), `/adk-dev-console` (navigate the Dev Console)

Then ask: _"What are you working on?"_

## When to Use This Skill

Activate this skill when users ask ADK-related questions like:

- "How do I create an Action/Tool/Workflow/Conversation?"
- "What is the difference between X and Y?"
- "Show me an example of..."
- "How do I configure...?"
- "What's the CLI command for...?"
- "How do I use the Context API?"
- "How do I call integration actions?"
- "How do I use Zai for [extract/check/label/etc]?"
- "What are the best practices for...?"
- "How do I avoid common mistakes?"
- "How do I handle ticket assignment/escalation?"
- "Explain my config"
- "What does my bot do?"
- "What models am I using?"
- "What integrations do I have?"
- "What state does my bot track?"

## Plugin Installation Prompt

If you are running inside Claude Code and the `/adk-*` commands (like `/adk-debug`, `/adk-eval`, `/adk-init`) are not available as slash commands, suggest that the user install the Botpress ADK plugin to get the full set of skills and commands:

```
/plugin marketplace add botpress/skills
/plugin install adk@botpress-skills
```

Only suggest this once per session. If the user declines, do not ask again.

## How to Answer ADK Questions

ADK questions fall into two categories: **CLI queries** and **documentation lookups**.

### Option 1: Direct CLI Commands (FAST - Use First!)

For integration discovery and CLI queries, use the Bash tool to run commands directly:

**Integration Discovery:**

```bash
# Search for integrations
adk integrations search <query>

# Find integrations that implement an interface
adk integrations search --interface <interface-name>

# Get detailed integration info (actions, channels, events)
adk integrations info <integration-name>

# Check installed integrations (must be in ADK project)
adk integrations list
```

**Project Info:**

```bash
# Check CLI version
adk --version

# Show project status
adk

# Get help
adk --help
```

**Prefer non-interactive paths when driving ADK workflows:**

```bash
# Login without browser prompts
adk login --token "$BOTPRESS_TOKEN"

# Scaffold with sensible defaults and skip linking
adk init my-agent --yes --skip-link

# Link directly when IDs are known
adk link --workspace ws_123 --bot bot_456

# More automation-friendly dev mode (NDJSON events, no TUI)
adk dev --non-interactive

# Review/apply project compatibility updates after ADK upgrades
adk project upgrade --dry-run
adk project upgrade

# Auto-approve non-destructive deploy-plan changes
adk deploy --yes
```

Use these defaults when relevant:

- Prefer `adk login --token "$BOTPRESS_TOKEN"` or `adk login --token <token>` over interactive login.
- Treat bare `BOTPRESS_TOKEN` as a no-TTY convenience, not a guaranteed interactive-terminal shortcut.
- Prefer `adk init <name> --yes --skip-link` for AI-driven scaffolding, but only after login is already completed.
- Treat `adk link --workspace ... --bot ...` as scriptable, but not guaranteed safe in every no-TTY environment.
- Treat `adk dev --non-interactive` as CI-friendly, not fully prompt-free.
- Treat `adk deploy --yes` as auto-approving non-destructive deploy-plan changes; config validation and destructive storage changes can still block automation.
- If project commands report a runtime/package mismatch, run `adk project upgrade --dry-run` first, then `adk project upgrade` to apply compatibility patches.

**When to use CLI commands:**

- "What integrations are available?"
- "Search for Slack integration"
- "Show me details about the Linear integration"
- "What actions does the Slack integration have?"
- "What version of ADK am I using?"
- "How do I add an integration?"

**Response pattern:**

1. Use Bash tool to run the appropriate `adk` command
2. Parse and present the output to the user
3. Optionally suggest next steps (e.g., "Run `adk integrations add slack@3.0.0` to install")

### Option 2: Documentation Questions (For Conceptual Questions)

For documentation, patterns, and how-to questions, search and reference the documentation files directly:

**When to use documentation:**

- "How do I create a workflow?"
- "What's the difference between Actions and Tools?"
- "Show me an example of using Zai"
- "What are best practices for state management?"
- "How do I fix this error?"
- "What's the pattern for X?"

**How to answer documentation questions:**

1. **Find relevant files** - Use Glob to discover documentation:

   ```
   pattern: **/references/*.md
   ```

2. **Search for keywords** - Use Grep to find relevant content:

   ```
   pattern: <keyword from user question>
   path: <path to references directory from step 1>
   output_mode: files_with_matches
   ```

3. **Read the files** - Use Read to load relevant documentation

4. **Provide answer** with:
   - Concise explanation
   - Code examples from the references
   - File references with line numbers (e.g., "From references/actions.md:215")
   - Common pitfalls if relevant
   - Related topics for further reading

### Option 3: Config Explanation (CLI + File Reading)

For questions about what a bot does, how it's configured, or what it's capable of, combine CLI and file reading:

**When to use:**

- "What does my bot do?"
- "Explain my config"
- "What models am I using?"
- "What integrations do I have?"
- "What state does my bot track?"

**Response pattern:**

1. Run `adk status --format json` to get the structured project overview
2. Read `agent.config.ts` for full configuration details
3. Follow the explanation patterns in **references/explain-config.md**
4. Produce a structured explanation covering metadata, models, integrations, state, and primitives
5. Flag any issues (unconfigured integrations, missing models, hardcoded secrets)

## Available Documentation

Documentation should be located in `./references/` directory relative to this skill. When answering questions, search for these topics:

### Core Concepts

- **actions.md** - Actions with strong typing and validation
- **tools.md** - AI-callable tools and Autonomous namespace
- **autonomous-execution.md** - Advanced execute() API: Objects, Exits, hooks, configuration
- **workflows.md** - Workflows and step-based execution
- **workflow-steps.md** - Complete Workflow Step API reference (step.request, step.map, step.notify, etc.)
- **conversations.md** - Conversation handlers, message routing, and receiving `chat:custom` events
- **conversation-lifecycle.md** - Nudge/expiration lifecycle management for conversations
- **triggers.md** - Integration & bot-lifecycle event subscriptions (app-pushed custom events → conversations.md)
- **messages.md** - Sending messages and events
- **custom-components.md** - Custom webchat components (`.bp.tsx` files, metadata, usage in conversations)

### Zai (AI Operations)

- **zai-agent-reference.md** - Quick reference: all operations, everyday problems Zai solves, edge cases & gotchas
- **zai-complete-guide.md** - Full developer guide: architecture, active learning, chunking, performance tuning

### Data & Content

- **tables.md** - Data storage with semantic search
- **files.md** - File storage and management
- **knowledge-bases.md** - RAG implementation
- **assets.md** - Static files with permanent URLs and sync lifecycle

### Configuration & Integration

- **agent-config.md** - Bot configuration and state management
- **explain-config.md** - How to interpret and explain an agent's configuration to developers
- **model-configuration.md** - AI model configuration reference
- **context-api.md** - Runtime context access
- **integration-actions.md** - Using integration actions
- **tags.md** - Entity tags for bot, user, conversation, and workflow
- **cli.md** - Complete CLI command reference
- **mcp-server.md** - MCP server for AI assistants
- **desk.md** - Desk integration for ticket/support workflows
- **integrations.md** - Integration management overview (points to adk-integrations skill)
- **interfaces.md** - Built-in interface abstraction layer over integrations (typing indicators, LLM, listable)
- **plugins.md** - Plugin consumption: discovery, installation, configuration, and usage

### Patterns & Best Practices

- **advanced-patterns.md** - Guardrails, admin auth, logging/observability, extension composition
- **patterns-mistakes.md** - Common mistakes, correct patterns, and context access reference

### Frontend Integration

> **Note:** Frontend integration docs are in the separate **adk-frontend** skill. Install it with `npx skills add botpress/skills --skill adk-frontend`. The `adk-frontend` skill covers @botpress/client, calling actions, type generation, and authentication. You need it if you are touching any frontend code.

### Evals

> **Note:** Detailed eval docs are in the separate **adk-evals** skill. Install it with `npx skills add botpress/skills --skill adk-evals`. The `adk-evals` skill covers writing evals, assertion types, testing workflows, and CLI usage. You usually always need it, for testing and evaluations.

## Runtime Access Patterns

Quick reference for accessing ADK runtime services:

### Imports

```typescript
// Always import from @botpress/runtime
import {
  Action,
  Autonomous,
  Workflow,
  Conversation,
  z,
  actions,
  adk,
  user,
  bot,
  conversation,
  configuration,
  context,
} from '@botpress/runtime'
```

### State Management

```typescript
// Bot state (defined in agent.config.ts)
bot.state.maintenanceMode = true
bot.state.lastDeployedAt = new Date().toISOString()

// User state (defined in agent.config.ts)
user.state.preferredLanguage = 'en'
user.state.onboardingComplete = true

// User tags
user.tags.email // Access user metadata
```

### Calling Actions

```typescript
// Call bot actions
await actions.fetchUser({ userId: '123' })
await actions.processOrder({ orderId: '456' })

// Call integration actions
await actions.slack.sendMessage({ channel: '...', text: '...' })
await actions.linear.issueList({ teamId: '...' })

// Convert action to tool
tools: [fetchUser.asTool()]
```

### Context API

```typescript
// Get runtime services
const client = context.get('client') // Botpress client
const cognitive = context.get('cognitive') // AI model client
const citations = context.get('citations') // Citation manager
```

### File Naming

- **Actions/Tools/Workflows**: `myAction.ts`, `searchDocs.ts` (camelCase)
- **Tables**: `Users.ts`, `Orders.ts` (PascalCase)
- **Conversations/Triggers**: `chat.ts`, `slack.ts` (lowercase)

## Critical ADK Patterns (Always Reference in Answers)

When answering questions, always verify these patterns against the documentation:

### Package Management

```bash
# All package managers are supported
bun install       # Recommended (fastest)
npm install       # Works fine
yarn install      # Works fine
pnpm install      # Works fine

# ADK auto-detects based on lock files
# - bun.lockb → uses bun
# - package-lock.json → uses npm
# - yarn.lock → uses yarn
# - pnpm-lock.yaml → uses pnpm
```

### Imports

```typescript
// ✅ CORRECT - Always from @botpress/runtime
import { Action, Autonomous, Workflow, z } from '@botpress/runtime'

// ❌ WRONG - Never from zod or @botpress/sdk
import { z } from 'zod' // ❌ Wrong
import { Action } from '@botpress/sdk' // ❌ Wrong
```

### Export Patterns

```typescript
// ✅ Both patterns work - export const is recommended
export const myAction = new Action({ ... });  // Recommended
export default new Action({ ... });           // Also valid

// Why export const?
// - Enables direct imports: import { myAction } from "./actions/myAction"
// - Can pass to execute(): tools: [myAction.asTool()]
```

### Actions

```typescript
// ✅ CORRECT - Handler receives { input, client }
export const fetchUser = new Action({
  name: "fetchUser",
  async handler({ input, client }) {  // ✅ Destructure from props
    const { userId } = input;         // ✅ Then destructure fields
    return { name: userId };
  }
});

// ❌ WRONG - Cannot destructure input fields directly
handler({ userId }) {  // ❌ Wrong - must be { input }
  return { name: userId };
}
```

### Tools

```typescript
// ✅ CORRECT - Tools CAN destructure directly
export const myTool = new Autonomous.Tool({
  handler: async ({ query, maxResults }) => {
    // ✅ Direct destructuring OK
    return search(query, maxResults)
  },
})
```

### Conversations

```typescript
// ✅ CORRECT - Use conversation.send() method
await conversation.send({
  type: "text",
  payload: { text: "Hello!" }
});

// ❌ WRONG - Never use client.createMessage() directly
await client.createMessage({ ... });  // ❌ Wrong
```

### Conversation Handler Types

```typescript
// Handler receives typed context based on the event type:
// type: "message" | "event" | "workflow_request" | "workflow_callback"
async handler({ type, message, event, request, completion, conversation, execute }) {
  if (type === "workflow_request") {
    // event: WorkflowDataRequestEventType, request: WorkflowRequest
    await request.workflow.provide("email", { email: "..." });
  }
  if (type === "workflow_callback") {
    // event: WorkflowCallbackEventType, completion: WorkflowCallback
    console.log(completion.status); // "completed" | "failed" | "canceled" | "timed_out"
  }
}

// ⚠️ isWorkflowDataRequest() and isWorkflowCallback() are deprecated
// Use type === "workflow_request" / "workflow_callback" instead
```

## Examples of Questions This Skill Answers

### Beginner Questions

- "What is an Action?"
- "How do I create my first workflow?"
- "What's the difference between Actions and Tools?"

### Implementation Questions

- "How do I access the Botpress client?"
- "How do I use citations in RAG?"
- "What's the syntax for searchable table columns?"
- "How do I call a Slack integration action?"
- "How do I use Zai to extract structured data?"
- "How do I validate content with Zai?"

### Advanced Pattern Questions

- "How do I add guardrails to prevent hallucinations?"
- "How do I implement admin authentication?"
- "How do I add logging and observability?"
- "How do I compose multiple extensions?"
- "How do I manage context in async tool handlers?"

### Troubleshooting Questions

- "Why am I getting 'Cannot destructure property' error?"
- "How do I fix import errors?"
- "What's wrong with my workflow state access?"

### Best Practices Questions

- "What are common mistakes to avoid?"
- "How should I structure my project?"
- "What's the recommended pattern for X?"

## Response Format

**Match your response depth to the question depth.** Not every question needs a full walkthrough.

### Conceptual Questions ("what is X?", "what's the difference between X and Y?")

One sentence definition + one short code example. That's it.

```
Knowledge bases add RAG to your bot — place markdown or PDF files in `src/knowledge/` and they become queryable with semantic search.

import { Autonomous } from '@botpress/runtime'
export default new Autonomous.Tool({
  handler: async ({ query }) => adk.knowledgeBase.search({ query }),
})
```

### How-To Questions ("how do I create X?", "how do I use X?")

Brief explanation + working code example + one critical pitfall only if it's a common trap.

### Implementation Questions ("implement X in my project", "add X to my bot")

Read the user's existing files first (`src/actions/`, `src/tools/`, `src/tables/`, `agent.config.ts`). Generate code that uses their actual names, patterns, and conventions. Only mention pitfalls they're likely to hit given their specific code.

### Architecture Questions ("explain my bot", "how does X work in my project?")

Full structured response: read `adk status --format json`, `agent.config.ts`, and relevant source files. Map the data flow and identify the bot's archetype (RAG assistant, support agent, automation, etc.).

### Troubleshooting Questions ("X is broken", "why is X failing?")

Don't answer with documentation. Run `adk check --format json` and `adk logs error --format json`, show evidence, and point to the root cause. Follow the debug loop from the `adk-debugger` skill.

### Default Rule

If the answer fits in one sentence and a code snippet, don't add headers, pitfall sections, or related topics. More structure ≠ more helpful.
