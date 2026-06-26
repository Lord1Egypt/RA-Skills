# Architecture

## Goal

Turn one Weixin account into a front door for an arbitrary configurable set of backend agents without mixing their session memory.

## Recommended flow

1. Receive Weixin message
2. Parse command intent
3. Load per-contact router state
4. Resolve current agent
5. Build agent-scoped session key
6. Either:
   - reply directly from the router layer, or
   - dispatch to the resolved agent session

## Anti-patterns to avoid

### 1. Shared session + roleplay switching

Do not keep one shared session and only change the speaking style. This causes context leakage between agents.

### 2. Raw transcript sharing across agents

Do not let one agent automatically read another agent's complete transcript. Use summary-based handoff instead.

### 3. Destructive reset by default

Prefer version-based session reset before attempting transcript deletion.

## State model

Recommended per-contact state:

```json
{
  "currentAgent": "main",
  "lastActiveAt": 1774200000000,
  "lastSwitchAt": 1774200100000,
  "sessionVersions": {
    "main": 1,
    "ops": 2,
    "writer": 1
  }
}
```

Optional additions:

- `recentHistory` per agent for summary view / handoff
- `lastTransferAt`
- `lastTransferTarget`

## Session key model

Recommended pattern:

- `agent:<agentId>:openclaw-weixin:<accountId>:dm:<peerId>:v<version>`

This should change when:

- the current agent changes
- the target agent session version increments after reset

## Timeout fallback

Recommended behavior:

- default agent = primary coordinator
- reset to default after a configurable inactivity window

The timeout should be configurable. Do not hard-code a project-specific value into a public skill unless the user explicitly wants an opinionated default.
