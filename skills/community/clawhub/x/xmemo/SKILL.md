---
name: xmemo-memory
description: Persistent, user-owned memory for AI agents over hosted MCP. Remember decisions, recall project context, manage TODOs, preserve handoff state, and govern memory lifecycle across sessions and tools.
---

# XMemo Memory

Give your agent durable memory that survives across sessions, projects, and tools. XMemo is a hosted MCP memory service; no local database or self-hosting is required.

This Skill teaches the agent when to use memory. Real memory read/write requires an XMemo runtime path: the native OpenClaw plugin, the Hermes provider plugin, or the hosted MCP server.

## Setup

Use the shortest path for the active client:

```text
npm install -g @xmemo/client
xmemo login
xmemo setup openclaw
xmemo setup hermes
```

- OpenClaw: run `xmemo setup openclaw`. This installs or updates the XMemo OpenClaw memory plugin and syncs the shared XMemo credential.
- Hermes: run `xmemo setup hermes`. This installs or updates the Hermes XMemo provider and syncs the shared XMemo credential.
- Generic MCP clients: connect `https://xmemo.dev/mcp` with OAuth when the client supports it, or use the shared XMemo credential from `xmemo login`.
- Add `--with-mcp` to the OpenClaw or Hermes setup command only when the native integration should also get a hosted MCP fallback.
- Use `--mcp-only` only when you want the hosted MCP fallback without installing the native plugin/provider.

Do not ask normal OpenClaw or Hermes users to choose agent identity fields, attribution headers, or token storage locations. The setup flow and native integrations handle those details.

When the user supplies only `https://xmemo.dev`, read these public, secret-free endpoints first:

```text
https://xmemo.dev/.well-known/agent-discovery.json
https://xmemo.dev/v1/mcp/config/openclaw
https://xmemo.dev/v1/mcp/config/hermes
```

## OpenClaw And Hermes

OpenClaw should use this Skill together with the native XMemo memory plugin:

```text
https://clawhub.ai/plugins/@xmemo/openclaw-memory
```

Hermes should prefer the `hermes-xmemo` provider over raw MCP because the provider participates in Hermes' memory lifecycle.

If this Skill is installed but XMemo memory tools are unavailable, do not simulate a successful memory operation. Tell the user that the Skill is guidance only and recommend the matching setup command for the active client.

## When To Use

Use XMemo when:

- The task depends on prior decisions, preferences, project context, or handoff state.
- The user asks to remember something for later.
- The agent is about to make an architecture, product, release, or security decision that prior memory could affect.
- The user wants TODOs, reminders, milestones, or follow-ups tracked across sessions.
- Multiple agents or clients need a shared but governed project memory trail.

## Workflow

1. Recall before assuming. For non-trivial work, call `recall_context`, `recall`, or `search_memory` with the current repo, project, task, and subsystem before making decisions.
2. Recall across agents. Search all visible user-owned XMemo memories unless the user explicitly asks for a narrower project, bucket, or scope.
3. Read provenance correctly. `agent_id`, `agent_instance_id`, and `agent_boundary` are attribution/provenance signals, not authorization boundaries and not a reason to ignore `other_agent` memories.
4. Use the result carefully. Treat recalled memories as context, not as proof that current files, production state, or external services are unchanged.
5. Save what matters. Store durable facts: decisions, conventions, preferences, architecture notes, release procedures, action items, and handoff state.
6. Preserve handoffs. At milestones or before stopping, use timeline/TODO/snapshot tools such as `record_event`, `create_memory_todo`, or `create_restart_snapshot` when available.
7. Confirm destructive actions. Always confirm the exact target before delete, forget, redact, overwrite, or broad cleanup operations.
8. On auth failure, tell the user to run `xmemo login` and then rerun the matching `xmemo setup <client>` command. Never request raw tokens in chat.

## Available Tools

Core memory operations may include:

| Tool | Purpose |
|------|---------|
| `remember` | Save a new durable memory |
| `recall` / `recall_context` | Retrieve relevant memories before answering or acting |
| `search_memory` | Search memories by query |
| `update_memory` | Revise existing memory content or metadata |
| `forget` / `forget_memory` | Delete or hide a memory |
| `redact_memory` | Remove sensitive content while keeping an audit trail |
| `explain_memory` | Show why a memory exists or matched a query |
| `memory_activity` | Inspect recent writes, reads, deletions, and changes |
| `create_memory_todo` | Create a follow-up task |
| `list_memory_todos` | List pending TODOs |
| `complete_memory_todo` | Mark a TODO done |
| `record_event` | Log a milestone, decision, or handoff event |
| `get_timeline` | Show recent events |
| `create_restart_snapshot` | Save active work state for future sessions |
| `restore_restart_snapshot` | Resume from saved work state |
| `add_expense` | Record a ledger entry when the user states a concrete expense |

Some deployments expose only a subset of tools depending on OAuth scopes, marketplace policy, or client capability. If a tool is missing, use the closest available safe workflow and explain the limitation briefly.

## Good Memory Candidates

- Repository conventions, build/test/deploy commands, and verified troubleshooting steps.
- Architecture decisions, product decisions, release procedures, and their rationale.
- User-approved preferences for code review, testing, documentation, or UX.
- Project TODOs, blockers, risks, and handoff summaries for future sessions.
- Bug fix context that might recur.

## Never Save

- Secrets, tokens, API keys, OAuth codes, cookies, session IDs, or private keys.
- Private customer data or sensitive personal data unless the user explicitly asks and the memory tool supports the required privacy policy.
- Temporary debugging output that will not help future work.
- Large code blocks; link to files, commits, or concise summaries instead.

## Safety

- Keep XMemo credentials private. Do not paste them into public prompts, screenshots, repositories, issue comments, marketplace metadata, or shared logs.
- Use synthetic data for marketplace demos and screenshots.
- Treat `X-Memory-OS-Agent-ID` and `X-Memory-OS-Agent-Instance-ID` as attribution only, not authorization proof.
- Do not claim a marketplace integration is certified unless there is explicit approval evidence for that marketplace.
