# Explaining an Agent's Configuration

Guide for interpreting and explaining an ADK agent's configuration to the developer. Use this when the developer asks questions like "What does my bot do?", "Explain my config", "What integrations do I have?", or "What models am I using?".

## Gathering Configuration Data

Before explaining anything, gather data from multiple sources. Each source provides a different view of the project.

### Source 1: `adk status --format json`

Structured overview of the project — primitives, integrations, and server state.

```bash
adk status --format json
```

**Example output:**

```json
{
  "project": {
    "name": "customer-support-bot",
    "path": "/home/dev/customer-support-bot"
  },
  "primitives": {
    "actions": {
      "count": 3,
      "details": [
        { "name": "lookupCustomer", "path": "src/actions/lookup-customer.ts", "description": "Look up customer records" },
        { "name": "sendInvoice", "path": "src/actions/send-invoice.ts", "description": "Send invoices to customers" },
        { "name": "triageTicket", "path": "src/actions/triage-ticket.ts", "description": "Route support tickets" }
      ],
      "names": ["lookupCustomer", "sendInvoice", "triageTicket"]
    },
    "tools": {
      "count": 2,
      "details": [
        { "name": "search", "path": "src/tools/search.ts", "description": "Search indexed docs" },
        { "name": "lookup", "path": "src/tools/lookup.ts", "description": "Look up CRM records" }
      ]
    },
    "workflows": { "count": 2, "details": [...] },
    "conversations": {
      "count": 1,
      "details": [
        { "name": "supportConversation @ chat.channel, webchat.channel", "path": "src/conversations/support.ts", "description": "Handle support conversations" }
      ]
    },
    "triggers": { "count": 0, "details": [] },
    "tables": { "count": 1, "details": [...] },
    "knowledge": { "count": 1, "details": [...] }
  },
  "integrations": [
    { "alias": "slack", "name": "slack", "version": "2.5.5", "status": "configured" },
    { "alias": "browser", "name": "browser", "version": "1.0.0", "status": "unconfigured", "missing": ["apiKey"] }
  ],
  "devServer": {
    "running": true,
    "port": 3100,
    "botId": "bot_abc123",
    "url": "http://localhost:3100"
  },
  "adkDevConsole": {
    "running": true,
    "port": 3005,
    "url": "http://localhost:3005"
  }
}
```

**What this tells you:**

- Project name and location
- Every registered primitive with name, file path, and description
- Integration status — which are configured and which are missing fields
- Whether the dev server is running

### Source 2: `agent.config.ts`

Full configuration details — models, state schemas, integration config, variables.

Read the file directly:

```bash
cat agent.config.ts
```

**What this tells you:**

- Model configuration (`defaultModels`)
- State schemas (`user.state`, `bot.state`, `conversation.state`)
- Integration versions and inline config
- Configuration schema
- Environment variable usage

### Source 3: `agent.json`

Bot and workspace IDs for deployment.

```bash
cat agent.json
```

**Example:**

```json
{
  "botId": "bot_abc123",
  "workspaceId": "ws_xyz789"
}
```

### Source 4: `agent.local.json`

Development bot ID (may not exist if `adk dev` hasn't run yet).

```bash
cat agent.local.json
```

**Example:**

```json
{
  "devId": "bot_dev_456"
}
```

## Explaining Each Configuration Section

### Metadata

The `name` and `description` fields in `agent.config.ts`.

**How to explain:**

- The `name` identifies the bot in the Botpress Cloud dashboard and CLI output.
- The `description` is optional — it documents the bot's purpose.

**Example explanation:**

> This is **customer-support-bot** — a customer support assistant. The name is used as the bot identifier in Botpress Cloud.

**Potential issues:**

- Missing `description` — not critical, but worth adding for documentation.
- Name with spaces or special characters — should be kebab-case.

### Model Configuration

The `defaultModels` object controls which AI models power the bot.

**Two model slots:**

| Slot         | Purpose                                                                     | Used By                                                        |
| ------------ | --------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `autonomous` | Agentic reasoning — conversation handling, tool selection, multi-step logic | `execute()` in conversations and workflows                     |
| `zai`        | Utility AI operations — extraction, classification, summarization           | `adk.zai.extract()`, `adk.zai.check()`, `adk.zai.text()`, etc. |

**How to explain model choices:**

```typescript
defaultModels: {
  autonomous: "openai:gpt-4o",
  zai: "openai:gpt-4o-mini",
}
```

> Your bot uses **gpt-4o** for autonomous reasoning (conversations, tool calls) and **gpt-4o-mini** for Zai utility operations (extraction, classification). This is a good balance — the more capable model handles complex decision-making while the cheaper/faster model handles structured utility tasks.

**Common configurations and tradeoffs:**

| Configuration                                                           | Tradeoff                                           |
| ----------------------------------------------------------------------- | -------------------------------------------------- |
| `autonomous: "openai:gpt-4o"`                                           | High quality, higher cost and latency              |
| `autonomous: "openai:gpt-4o-mini"`                                      | Fast and cheap, less capable for complex reasoning |
| `autonomous: "fast"`                                                    | Zai shortcut — fastest/cheapest available model    |
| `autonomous: "best"`                                                    | Zai shortcut — highest quality available model     |
| `autonomous: "anthropic:claude-3-5-sonnet"`                             | Strong reasoning, different provider               |
| `zai: "openai:gpt-4o-mini"`                                             | Good default for utility tasks                     |
| Fallback arrays like `["openai:gpt-4o", "anthropic:claude-3-5-sonnet"]` | Automatic fallback if first model is unavailable   |

**If `defaultModels` is not set**, the ADK uses these defaults:

- `zai`: `"openai:gpt-4.1-2025-04-14"`
- `autonomous`: `"openai:gpt-4.1-mini-2025-04-14"`

**Potential issues:**

- No `defaultModels` set — the bot uses ADK defaults, which may not be optimal.
- Both slots set to `"fast"` — fine for development, but may underperform in production for complex conversations.
- Both slots set to `"best"` — high quality but expensive; consider using `"best"` only for `autonomous`.

### Integrations

The `dependencies.integrations` section defines which external services the bot connects to.

**How to explain:**

For each integration, describe:

1. **What it is** — the platform or service it connects to
2. **What it provides** — channels (for messaging), actions (for API calls), events (for triggers)
3. **Whether it's configured** — check the `status` field from `adk status`

**Example explanation:**

```typescript
dependencies: {
  integrations: {
    webchat: "webchat@0.3.0",
    chat: "chat@1.0.0",
    slack: {
      version: "slack@2.5.5",
      enabled: true,
      config: { botToken: "{{secrets.SLACK_BOT_TOKEN}}" },
    },
    browser: "browser@0.8.7",
  },
}
```

> Your bot has 4 integrations:
>
> - **webchat** (v0.3.0) — Provides the Botpress webchat widget channel. Users can chat with your bot through an embeddable web widget.
> - **chat** (v1.0.0) — Provides the Botpress Chat API channel. Allows programmatic messaging via the Botpress API.
> - **slack** (v2.5.5) — Connects to Slack. Provides channels for DMs and group messages, plus actions like `sendMessage`, `addReaction`, etc. Configured with a bot token from environment variables.
> - **browser** (v0.8.7) — Provides web browsing and scraping actions like `webSearch` and `browsePages`. No channel — this is a tool-only integration.

**To get details about a specific integration's capabilities:**

```bash
adk integrations info slack --format json
```

**Potential issues:**

- Integration with `status: "unconfigured"` and `missing` fields — needs configuration before it works.
- Integration using hardcoded secrets instead of the ADK secrets API — security risk.
- Integration with `enabled: false` — installed but not active.

### State Schemas

State schemas define what data the bot persists across interactions.

**Three state scopes:**

| Scope                | Persisted Per | Typical Use                                    |
| -------------------- | ------------- | ---------------------------------------------- |
| `user.state`         | User          | Preferences, profile data, onboarding progress |
| `bot.state`          | Bot (global)  | Feature flags, counters, maintenance mode      |
| `conversation.state` | Conversation  | Context within a single conversation thread    |

**How to explain:**

```typescript
user: {
  state: z.object({
    name: z.string().optional().describe("The user's name"),
    department: z.string().optional().describe("The user's department"),
    role: z.string().optional().describe("The user's job role"),
    age: z.number(),
  }).default({ age: 10 }),
},
bot: {
  state: z.object({
    version: z.number(),
    ticketCounter: z.number(),
  }).default({ version: 0, ticketCounter: 0 }),
},
```

> **User state** tracks per-user data:
>
> - `name` (optional string) — The user's name, collected during conversation
> - `department` (optional string) — The user's department
> - `role` (optional string) — The user's job role
> - `age` (number, defaults to 10) — The user's age
>
> **Bot state** tracks global data:
>
> - `version` (number, defaults to 0) — Bot configuration version
> - `ticketCounter` (number, defaults to 0) — Running count of tickets created
>
> No conversation state is defined — conversation-scoped data is not being tracked.

**Potential issues:**

- No `.default()` on required fields — will fail if state hasn't been initialized.
- Large state objects — can slow down read/write operations.
- Sensitive data in state (emails, tokens) — consider whether it needs to be stored.

### Variables and Secrets

Check the `secrets` block in `agent.config.ts` for declared secrets, and look for hardcoded string literals in integration configs.

**How to explain:**

> Your config declares these secrets:
>
> - `SLACK_BOT_TOKEN` — Used to authenticate the Slack integration
> - `LINEAR_API_KEY` — Used to authenticate the Linear integration
>
> Secrets are managed via `adk secrets` and injected at runtime. Make sure they're set for both dev and production environments.

**Potential issues:**

- Hardcoded secrets in `agent.config.ts` — should use the ADK secrets API instead.
- Declared secrets that aren't set — the integration won't work at runtime.

### Registered Primitives

The primitives from `adk status` show what the bot can actually do.

**How to explain each type:**

| Primitive         | What It Means                                                                       |
| ----------------- | ----------------------------------------------------------------------------------- |
| **Actions**       | Functions callable by the bot or external APIs. Each action has typed input/output. |
| **Tools**         | AI-callable tools — these are what the LLM can invoke during autonomous reasoning.  |
| **Workflows**     | Long-running, resumable processes with step-based execution.                        |
| **Conversations** | Message handlers — routes incoming messages by channel.                             |
| **Triggers**      | Event-driven handlers — react to specific events (e.g., new user, webhook).         |
| **Tables**        | Structured data storage with optional semantic search.                              |
| **Knowledge**     | RAG knowledge bases — documents the bot can search and cite.                        |

**Example explanation from status output:**

> Your bot has **3 actions**, **2 tools**, **2 workflows**, **1 conversation handler**, **no triggers**, **1 table**, and **1 knowledge base**.
>
> **What it can do:**
>
> - Look up customers, send invoices, and triage tickets (actions)
> - Search docs and look up CRM records autonomously (tools — the LLM decides when to call these)
> - Escalate urgent tickets and schedule follow-ups (workflows — long-running processes)
> - Handle support conversations on chat and webchat channels (conversation handler)
> - Store contacts (table)
> - Answer questions from the FAQ knowledge base (knowledge)

## Producing a Structured Explanation

### High-Level Overview ("What does my bot do?")

Combine all sources into a concise summary:

1. Start with the bot's name and description
2. List what channels it operates on (from integrations + conversations)
3. Summarize its capabilities (from primitives)
4. Mention the AI models powering it
5. Note any issues

**Example full explanation:**

> **customer-support-bot** is a customer support assistant that operates on **Slack**, **webchat**, and the **Chat API**.
>
> It uses **gpt-4o** for conversations and **gpt-4o-mini** for utility AI tasks.
>
> **Capabilities:**
>
> - Looks up customers, sends invoices, and triages support tickets
> - Can autonomously search documentation and look up CRM records
> - Runs escalation and follow-up workflows for ticket management
> - Stores contacts in a table and uses an FAQ knowledge base for answers
>
> **State tracking:**
>
> - Tracks user preferences (language, timezone, account tier)
> - Maintains global counters and feature flags
>
> **Issues to address:**
>
> - The `browser` integration is missing its `apiKey` configuration

### Section-Specific Explanation

When the developer asks about a specific section, read the relevant part of `agent.config.ts` and explain just that section using the patterns above.

### Identifying Issues

When reviewing the config, check for:

| Check                     | How to Detect                                                             | Severity                                   |
| ------------------------- | ------------------------------------------------------------------------- | ------------------------------------------ |
| Unconfigured integrations | `status: "unconfigured"` in `adk status` output                           | High — integration won't work              |
| Hardcoded secrets         | String literals in `config` blocks instead of ADK secrets API             | High — security risk                       |
| Missing default models    | No `defaultModels` in `agent.config.ts`                                   | Low — ADK defaults apply                   |
| No conversation handler   | `conversations.count === 0` in status                                     | High — bot can't respond to messages       |
| No tools registered       | `tools.count === 0` in status                                             | Medium — LLM can't take autonomous actions |
| No knowledge base         | `knowledge.count === 0` in status                                         | Low — bot relies only on tools and actions |
| State without defaults    | `z.object({...})` without `.default()`                                    | Medium — may fail on first access          |
| Unused integrations       | Integration installed but no conversation handler or action references it | Low — wasted dependency                    |

### Suggesting Improvements

Based on what's present vs missing, suggest concrete next steps:

- No tools? "Consider adding tools in `src/tools/` so the LLM can take autonomous actions during conversations."
- No knowledge base? "If your bot needs to answer questions from documents, add files to `src/knowledge/`."
- Using `"fast"` for autonomous model in production? "Consider upgrading the autonomous model to `gpt-4o` or `best` for better reasoning quality in production."
- No conversation state defined? "If you need to track context within a conversation (e.g., current topic, step in a flow), add a `conversation.state` schema."

## Handling Common Questions

### "What does my bot do?"

1. Run `adk status --format json`
2. Read `agent.config.ts`
3. Produce a high-level overview (see template above)

### "What integrations do I have?"

1. Run `adk status --format json` — check the `integrations` array
2. For each integration, explain what it provides
3. Flag any with `status: "unconfigured"`
4. Optionally run `adk integrations info <name> --format json` to show available actions/channels

### "Explain my config"

1. Read `agent.config.ts`
2. Walk through each section: metadata, models, integrations, state, variables
3. Use the section-specific explanation patterns above

### "What models am I using?"

1. Read `agent.config.ts` — find `defaultModels`
2. Explain each slot (autonomous vs zai) and the tradeoffs
3. If not set, mention the ADK defaults

### "What state does my bot track?"

1. Read `agent.config.ts` — find `user.state`, `bot.state`, `conversation.state`
2. List each field with its type, whether it's optional, and its default value
3. Explain the `.describe()` annotations if present — these document the field's purpose

## See Also

- **[agent-config.md](./agent-config.md)** — Full configuration format and options reference
- **[model-configuration.md](./model-configuration.md)** — AI model configuration details and precedence
- **[integration-actions.md](./integration-actions.md)** — Using integration actions in code
- **[context-api.md](./context-api.md)** — Accessing runtime services like client and state
- **[cli.md](./cli.md)** — Complete CLI command reference
