# Plan: Universal Agent Communication

**Date:** 2026-03-17
**Authors:** Parker Todd Brooks, Claude Code (cc-mini), Lesa (oc-lesa-mini)
**Status:** Current (implement next)
**Depends on:** OpenClaw ACP-Client (implemented), LDM OS Bridge (v0.3.0+), Message Bus (v0.3.0+)
**Related:** shared-awareness.md, agent-to-agent-messaging.md, ldm-stack-spec.md

---

## Problem

Agents can't talk to each other. Today: CC messaged Lesa but Lesa couldn't message CC. Two CC sessions fixed the same bug without knowing. Parker relayed everything manually. The HTTP inbox is broken. The tmux watcher was destroyed by ldm install.

This isn't a bridge bug. It's an architecture gap. Every agent on every platform needs to talk to every other agent. Bidirectional. Real-time. Local and remote.

## The Full Matrix

Every cell must work. Not just CC <-> Lesa.

### Senders (rows) to Receivers (columns)

|  | CC CLI | CC CLI (other session) | OpenClaw | Claude iOS | Claude macOS | Claude Web | GPT iOS | GPT macOS | GPT Web | Codex CLI |
|---|---|---|---|---|---|---|---|---|---|---|
| **CC CLI** | - | msg bus | ACP | relay | ACP | relay | relay | relay | relay | msg bus |
| **CC CLI (other)** | msg bus | - | ACP | relay | ACP | relay | relay | relay | relay | msg bus |
| **OpenClaw** | ACP | ACP | - | relay | ACP | relay | relay | relay | relay | ACP |
| **Claude iOS** | relay | relay | relay | - | relay | relay | relay | relay | relay | relay |
| **Claude macOS** | ACP | ACP | ACP | relay | - | relay | relay | relay | relay | ACP |
| **Claude Web** | relay | relay | relay | relay | relay | - | relay | relay | relay | relay |
| **GPT iOS** | relay | relay | relay | relay | relay | relay | - | relay | relay | relay |
| **GPT macOS** | relay | relay | relay | relay | relay | relay | relay | - | relay | relay |
| **GPT Web** | relay | relay | relay | relay | relay | relay | relay | relay | - | relay |
| **Codex CLI** | msg bus | msg bus | ACP | relay | ACP | relay | relay | relay | relay | - |

### Three Transport Layers

| Transport | When | How |
|---|---|---|
| **Message Bus** | CC <-> CC, CC <-> Codex (same machine) | File-based at ~/.ldm/messages/. Already built. |
| **ACP** | Any agent with shell <-> OpenClaw gateway (same machine or LAN) | WebSocket. Already in OpenClaw. |
| **Cloud Relay** | Any agent <-> any agent (different machines, no shell) | Encrypted dead drops via Cloudflare R2. Follows Memory Crystal relay pattern. |

### Platform Capabilities

| Platform | Has Shell | Has ACP | Has WebSocket | Transport |
|---|---|---|---|---|
| Claude Code CLI | Yes | Yes (stdio) | Yes | ACP + msg bus |
| Codex (OpenAI CLI) | Yes | Can implement | Yes | ACP + msg bus |
| OpenClaw | Yes | Yes (native) | Yes | ACP (gateway) |
| Claude macOS app | No shell | MCP config | Yes | ACP via MCP wrapper |
| Claude iOS app | No | No | HTTPS only | Cloud Relay |
| Claude Web | No | No | Yes | Cloud Relay WebSocket |
| GPT macOS app | No shell | TBD | TBD | Cloud Relay |
| GPT iOS app | No | No | HTTPS only | Cloud Relay |
| GPT Web | No | No | Yes | Cloud Relay WebSocket |

## Architecture

```
                    Cloud Relay (Cloudflare R2)
                    Encrypted dead drops, 24h TTL
                    For: iOS, Web, remote machines
                         |
                         v
Local Machine (Core) ----+----
  |                           |
  |  ACP Gateway              |  Message Bus
  |  (OpenClaw :18789)        |  (~/.ldm/messages/)
  |  WebSocket, bidirectional  |  File-based, async
  |                           |
  +-- CC Session 1 (ACP)     +-- CC Session 1 (read/write)
  +-- CC Session 2 (ACP)     +-- CC Session 2 (read/write)
  +-- Lesa/OpenClaw (native)  +-- Codex (read/write)
  +-- Claude macOS (MCP->ACP) |
  +-- Codex (ACP)             |
```

### How Each Path Works

**CC <-> CC (same machine):**
Message bus. File at ~/.ldm/messages/. Write a JSON file, other session reads it. Boot hook checks on start. Stop hook checks on end. Shared log (shared-awareness.md) for real-time awareness.

**CC <-> Lesa (same machine):**
ACP. CC's MCP server connects to the gateway via WebSocket. Lesa sends a message, gateway pushes to CC's WebSocket. CC sends a message, goes through gateway to Lesa's session. Both land in agent:main:main (unified session, fixed today).

**CC <-> Claude macOS app (same machine):**
ACP via MCP wrapper. The macOS app reads MCP config. An MCP server wraps the ACP connection. The app calls MCP tools that route through ACP to the gateway.

**Any agent <-> any agent (different machines):**
Cloud Relay. Agent encrypts message (AES-256-GCM), drops to Cloudflare R2. Poller on target machine picks up, decrypts, delivers to local gateway or message bus. Same protocol, encrypted transport. Zero-knowledge relay.

**iOS / Web agents:**
Cloud Relay only. No local install possible. Agent connects to relay WebSocket endpoint. Messages encrypted end-to-end. The relay can't read them.

## Implementation Order

### Phase 1: CC <-> Lesa Real-Time (LOCAL, THIS WEEK)

What: CC's MCP server connects to gateway via ACP WebSocket. Bidirectional.

| Step | What | Where |
|---|---|---|
| 1 | Verify ACP works: `openclaw acp --session agent:main:main` | Manual test |
| 2 | MCP server opens ACP connection on startup | `src/bridge/mcp-server.ts` |
| 3 | Incoming ACP messages queue in MCP inbox | `src/bridge/mcp-server.ts` |
| 4 | `lesa_check_inbox` drains ACP queue (not HTTP) | `src/bridge/mcp-server.ts` |
| 5 | Kill HTTP inbox server (port 18790) | `src/bridge/mcp-server.ts` |
| 6 | Update `lesa_send_message` to use ACP | `src/bridge/core.ts` |

Result: Lesa messages CC, CC sees it instantly. No polling. No tmux.

### Phase 2: CC <-> CC Real-Time (LOCAL)

What: Message bus + shared log + boot/stop hook integration.

| Step | What | Where |
|---|---|---|
| 1 | Shared log (`~/.ldm/memory/shared-log.jsonl`) | `lib/shared-log.mjs` (new) |
| 2 | CC writes to shared log on significant actions | `bin/ldm.js`, `lib/deploy.mjs` |
| 3 | Boot hook reads shared log, shows "while you were away" | `src/boot/boot-hook.mjs` |
| 4 | Stop hook writes summary to shared log | cc-hook integration |
| 5 | MCP tools: `ldm_log_event`, `ldm_read_log` | `src/bridge/mcp-server.ts` or new |

Result: CC session 1 knows what CC session 2 is doing. No duplicate work.

### Phase 3: Lesa Awareness (LOCAL)

What: Lesa reads shared log, writes to shared log, cross-populates daily logs.

| Step | What | Where |
|---|---|---|
| 1 | agent_end hook reads shared log | `src/openclaw.ts` (Memory Crystal) |
| 2 | agent_end hook writes to shared log | `src/openclaw.ts` |
| 3 | CC stop hook writes to Lesa's daily log | `src/cc-hook.ts` |

Result: Lesa knows what CC did. CC's daily log entries appear in Lesa's daily log.

### Phase 4: Cloud Relay (REMOTE)

What: Encrypted relay for cross-machine and no-shell platforms.

| Step | What | Where |
|---|---|---|
| 1 | Cloudflare Worker (already exists in Memory Crystal) | Port from `src/worker.ts` |
| 2 | Local poller picks up messages, delivers to gateway/bus | `src/poller.ts` pattern |
| 3 | Node registration and pairing | `crystal pair` pattern |
| 4 | Per-agent auth tokens | Worker auth |

Result: Air laptop talks to Mini. iOS talks to Mini. Any device, anywhere.

### Phase 5: Platform Adapters (UNIVERSAL)

What: Wrappers for each platform that doesn't speak ACP natively.

| Platform | Adapter | How |
|---|---|---|
| Claude macOS | MCP -> ACP bridge | MCP server wraps ACP connection |
| Claude iOS | Cloud Relay SDK | HTTPS POST to relay endpoint |
| Claude Web | Cloud Relay WebSocket | Browser WebSocket to relay |
| GPT macOS | GPT Actions -> Cloud Relay | Action calls relay HTTP endpoint |
| GPT iOS | GPT Actions -> Cloud Relay | Same |
| GPT Web | GPT Actions -> Cloud Relay | Same |
| Codex CLI | Message bus + ACP | Same as CC CLI |

## What Dies

| Component | Replaced By | When |
|---|---|---|
| HTTP inbox (port 18790) | ACP push | Phase 1 |
| watch.sh (tmux watcher) | ACP push | Phase 1 |
| send-to-claude-code skill | ACP push | Phase 1 |
| chatCompletions for messaging | ACP for real-time, chatCompletions stays for one-shot | Phase 1 |
| Manual daily log cross-write | Shared log + auto-sync | Phase 3 |
| Parker as relay | Shared log + unified session | Phase 2-3 |

## What Stays

| Component | Why |
|---|---|
| lesa_send_message (MCP tool) | Same name, ACP transport underneath |
| lesa_conversation_search | Memory search, not messaging |
| lesa_memory_search | Workspace search |
| crystal_search / crystal_remember | Memory Crystal tools |
| Message bus (ldm msg) | CC-to-CC async, file-based, survives crashes |
| Unified session (user: "main") | All messages in one stream |

## Verification (Full Chain)

1. CC session 1 messages CC session 2. Session 2 sees it on next turn.
2. CC messages Lesa via ACP. Lesa sees it instantly in TUI.
3. Lesa messages CC via ACP. CC sees it instantly (no polling).
4. Parker types in TUI. Both CC and Lesa see it. Same session.
5. CC on Air messages Lesa on Mini via Cloud Relay. < 60s delivery.
6. Parker opens Claude iOS, sends a message. Lesa responds. CC sees it.
7. All agents have shared awareness of what everyone is doing.

---

Built by Parker Todd Brooks, Lesa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).

*WIP.computer. Learning Dreaming Machines.*
