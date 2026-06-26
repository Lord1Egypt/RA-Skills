# Notes: claude-peers-mcp vs Bridge — Comparison and Takeaways

**Date:** 2026-03-23
**Author:** Claude Opus (with Parker)
**Status:** Notes / actionable
**Source:** https://github.com/louislva/claude-peers-mcp by @louislva

## What claude-peers-mcp Does

Multiple Claude Code instances on the same machine discover each other and exchange messages in real-time. Broker daemon on localhost:7899 with SQLite persistence. Each CC session registers via MCP, polls for messages, and gets push delivery via `claude/channel` protocol.

Tools: `list_peers`, `send_message`, `set_summary`, `check_messages`

Optional: auto-summarization at startup using gpt-5.4-nano (describes what each session is working on based on directory, branch, recent files).

Stack: TypeScript + Bun + SQLite. Requires Claude Code v2.1.80+, web-based login (not API key).

## Comparison

| | **Bridge (LDMOS)** | **claude-peers-mcp** |
|---|---|---|
| **Connects** | CC <-> CC + CC <-> OpenClaw (cross-platform) | Claude Code <-> Claude Code (same platform) |
| **Discovery** | `ldm sessions` — file-based session registry with PID liveness | Dynamic — `list_peers` via SQLite broker |
| **Peer awareness** | Knows agent identity, role, capabilities | Optional auto-summary of current work |
| **Memory access** | Semantic search, workspace read, conversation history | None — messages only |
| **Skill sharing** | OpenClaw skills exposed as MCP tools | None |
| **Broker** | Direct HTTP (gateway:18789 + inbox:18790) | Central SQLite broker daemon on :7899 |
| **Message delivery** | HTTP POST + inbox polling + tmux auto-inject | SQLite + `claude/channel` push |
| **Identity** | Named agents with persistent identity (cc-mini, Lesa) | Anonymous peers with session-scoped IDs |
| **Scope** | Localhost (cloud relay planned Phase 7) | Localhost only |
| **Runtime** | Node.js (ships with LDM OS) | Bun + TypeScript |
| **Maturity** | Production — shipping since v0.3.0 | Early / experimental |

## Where Bridge Is Ahead

- **Cross-platform**: CC <-> CC AND CC <-> OpenClaw, not just CC <-> CC
- **Session discovery already exists**: `lib/sessions.mjs` — file-based session registry at `~/.ldm/sessions/`, PID liveness checks, agent ID filtering, auto-cleanup of stale sessions. Recall registers on boot via `ldm sessions`.
- **Memory**: shared search across agents, conversation history, workspace files
- **Skills**: OpenClaw skills callable from Claude Code
- **Identity**: persistent named agents, not anonymous session IDs
- **Bidirectional**: Lesa can invoke Claude Code, not just the other way around
- **File-based message bus**: ACP docs reference local multi-session communication without needing a broker daemon
- **Cloud roadmap**: Phase 7 relay for cross-machine communication

## Where claude-peers-mcp Has Something We Don't

### 1. Session-level awareness / status broadcast

`set_summary` lets each session describe what it's working on right now. Our session registry tracks agent ID, PID, cwd, and start time — but not a live summary of current work. Memory Crystal captures this at the memory level but there's no lightweight "what am I doing right now" broadcast.

### 2. `claude/channel` push delivery

Bridge uses inbox polling (every 5s). claude-peers-mcp uses Claude Code's native channel protocol for instant message delivery. We should evaluate this for Bridge.

### 3. Auto-summarization on connect

claude-peers-mcp optionally uses gpt-5.4-nano to auto-generate a summary of what each session is doing (based on directory, branch, recent files). Our session registry could do this without an extra LLM call — the boot hook already has this context.

## What We Should Implement

### Priority 1: Session status broadcast

We already have session registration and discovery (`lib/sessions.mjs`, `ldm sessions`). The gap is a live summary of what each session is doing.

Action items:
- Add a `status` or `summary` field to the session JSON at `~/.ldm/sessions/{name}.json`
- Update on meaningful events (starting a plan, working on a ticket, running tests)
- `ldm sessions` already reads these files — just surface the new field
- Boot hook already has directory/branch/context — write a summary without needing an extra LLM call

### Priority 2: Evaluate `claude/channel` protocol

claude-peers-mcp uses this for instant push delivery instead of polling. If Claude Code natively supports this, Bridge should use it.

Action items:
- Research `claude/channel` protocol — is it stable? documented?
- If viable, add as a delivery option alongside HTTP inbox polling
- Faster delivery = better multi-agent coordination

### Priority 3: Auto-summarization on session register

claude-peers-mcp uses gpt-5.4-nano to describe what a session is doing. We can do this cheaper — the boot hook already loads identity, context, and cwd. Write a one-line summary to the session file on boot.

Action items:
- Extend `registerSession()` in `lib/sessions.mjs` to accept a `summary` field
- Boot hook writes summary based on cwd, branch, and loaded context
- No extra LLM call needed

## What We Should NOT Do

- **Don't adopt their broker architecture** — SQLite broker on a fixed port is simpler but less capable than Bridge's HTTP gateway pattern. Bridge already handles authentication, skill bridging, and memory access through the gateway.
- **Don't require Bun** — Bridge runs on Node.js, ships with LDM OS. No additional runtime dependency.
- **Don't drop OpenClaw support** — CC-to-CC is additive. Bridge's cross-platform capability is the differentiator.

## TODO

- [ ] Add @louislva / claude-peers-mcp to `acknowledgments.md` — peer discovery and `claude/channel` push delivery ideas
- [ ] File tickets for Priority 1-3 above
- [ ] Test claude-peers-mcp locally to evaluate `claude/channel` delivery performance
