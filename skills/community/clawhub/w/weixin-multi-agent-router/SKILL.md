---
name: weixin-multi-agent-router
description: Design or implement single-entry multi-agent routing for OpenClaw Weixin setups. Use when one Weixin account should route between any number of backend agents, when users want natural switch commands instead of separate Weixin bots, when agent names and counts must stay configurable, when per-agent session isolation is required to avoid context mixing, or when summary-based handoff/reset/status commands are needed for a Weixin plugin, extension, or reusable skill.
---

# Weixin Multi Agent Router

Build a chat-friendly multi-agent system behind one Weixin entrypoint.

Prefer plugin-layer routing first. Do not start by changing OpenClaw core unless the user explicitly wants a reusable framework beyond Weixin.

## Core capabilities

### 1. Route one Weixin entry to any number of agents

Treat Weixin as:

- one human-facing entrypoint
- one configurable list of backend agents
- one per-contact current-agent state

Do not assume there are exactly two, three, or any other fixed number of agents. The skill should still work if the user has 1, 3, 5, or more routable backend agents.

Do **not** model this as Telegram-style multi-bot identity unless the underlying Weixin provider actually supports separate independently routable bot identities.

### 2. Isolate memory per agent

Do not only switch tone or persona inside a shared session.

Require session identity to include at least:

- channel
- accountId
- peerId
- agentId
- optional session version

Recommended session key pattern:

- `agent:<agentId>:openclaw-weixin:<accountId>:dm:<peerId>:v<version>`

This is the main guardrail against context mixing.

### 3. Store current active agent per contact

Keep per-contact router state containing at least:

- `currentAgent`
- `lastActiveAt`
- optional `lastSwitchAt`
- optional per-agent `sessionVersions`
- optional per-agent `recentHistory`

Recommended default behavior:

- default agent = primary coordinator
- inactivity fallback = reset current agent to default after a configurable timeout

### 4. Use summary-based handoff, not raw transcript sharing

When the user asks to hand work from one agent to another:

1. collect recent history from the current agent only
2. build a compact handoff summary
3. switch `currentAgent`
4. confirm the handoff in chat
5. prefer silent handoff so the target agent does not immediately double-reply

Do not automatically expose one agent's full transcript to another.

## Recommended command surface

Support at least four command groups.

### Switching

Examples:

- `切到{agent}`
- `切换到{agent}`
- `回到{defaultAgent}`
- `{agent} ...`

### Status

Examples:

- `当前是谁`
- `现在是谁`
- `你是谁`
- `角色列表`

### Reset

Examples:

- `重置当前`
- `清空当前上下文`
- `清空{agent}`
- `只重置{agent}`

Prefer version-based session reset over destructive transcript deletion.

### Handoff / summary

Examples:

- `转给{agent}`
- `交给{agent}`
- `让{agent}接手`
- `总结后交给{agent}`
- `查看当前上下文摘要`
- `查看{agent}上下文摘要`

## Implementation workflow

Follow this order.

### Step 1: define the agent map

Decide:

- the full configurable agent list
- per-agent ids
- per-agent display names shown to the user
- per-agent role descriptions
- per-agent aliases / command triggers
- default agent
- inactivity timeout

Keep this data-driven. A public skill must not depend on one private team's exact agent count or naming scheme.

If these are hard-coded in the current implementation, plan a config layer before publishing the system as a generic skill.

For configuration patterns and prompts, read `references/configurability.md`.

Minimal productized config shape:

```json
{
  "defaultAgent": "main",
  "inactivityTimeoutMs": 1800000,
  "agents": [
    {
      "agentId": "main",
      "displayName": "主助理",
      "description": "综合处理、调度、总结",
      "aliases": ["主助理", "总助理"]
    },
    {
      "agentId": "ops",
      "displayName": "技术助手",
      "description": "维护、配置、诊断",
      "aliases": ["技术", "运维"]
    }
  ]
}
```

Productization checklist for an update/public release:

- ensure agent list, aliases, default agent, and timeout are configuration-driven
- keep router runtime state separate from long-lived top-level config
- keep public examples generic; do not publish private team names as defaults
- validate against at least two different agent maps before packaging

### Step 2: define the command map

Map natural-language commands to:

- switch current agent
- switch and send content
- query status
- show roles
- reset current or target agent
- show summary
- handoff

Keep first-pass matching explicit and conservative. Avoid fuzzy aliasing until the stable command set works.

For concrete command patterns, read `references/commands.md`.

### Step 3: implement router state + session isolation

Create or update router modules such as:

- command parser
- state store
- session-key builder
- router decision layer
- handoff summary builder
- direct reply strings

Persist state outside the core config when possible so per-contact runtime data does not pollute long-lived top-level config.

For architecture guidance, read `references/architecture.md`.

### Step 4: validate behavior in chat

Test at minimum:

- switching
- current-agent persistence
- inactivity fallback
- agent memory isolation
- reset behavior
- summary-based handoff
- no duplicate reply after silent handoff
- no “summary of summary” nesting in recent-history views

For validation scenarios, read `references/validation.md`.

## Output standards

When helping with this task:

- explain the routing model in plain language
- separate “single-entry multi-agent” from “multi-bot identity”
- make session isolation explicit
- make handoff rules explicit
- prefer a config-driven design if the user wants to share the solution publicly
- avoid implying that the system needs exactly 3 roles or any specific private naming scheme

## Opinionated but safe starting point

If the user has not decided how many agents to expose yet, suggest starting with a small set such as:

- 1 primary coordinator only, or
- 2 to 3 clearly differentiated agents

Present this only as a starting point for usability, not as a requirement of the architecture.

## Resources

- Architecture details: `references/architecture.md`
- Command patterns: `references/commands.md`
- Configurability patterns: `references/configurability.md`
- Validation checklist: `references/validation.md`
