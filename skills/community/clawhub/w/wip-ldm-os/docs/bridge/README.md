###### WIP Computer

# Bridge

## Your AIs talk to each other.

Cross-platform agent communication. Claude Code talks to Claude Code. Claude Code talks to OpenClaw. OpenClaw talks back. Bridge (MCP), Agent Client Protocol (ACP-Client, Zed Industries), and Agent Communication Protocol (ACP-Comm, IBM/Linux Foundation). Three protocols, one system.

## Three Protocols, One System

LDM OS uses three complementary protocols. Bridge is one of them.

| | Bridge | ACP-Client | ACP-Comm |
|---|---|---|---|
| **What** | Agent-to-agent messaging + shared memory | IDE-to-agent communication | Agent-to-agent REST API |
| **Protocol** | MCP (JSON-RPC over stdio) | JSON-RPC over stdio + WebSocket | REST/HTTP |
| **Built by** | WIP Computer | Zed Industries | IBM / Linux Foundation |
| **In LDM OS** | Core (v0.3.0+) | Available via OpenClaw | Planned (Cloud Relay) |
| **What it connects** | CC <-> CC + CC <-> OpenClaw agents | IDEs (Zed, VS Code) <-> agents | Cloud agents <-> each other |
| **Memory access** | Yes (search + read across agents) | No | No |
| **Skill sharing** | Yes (OpenClaw skills as MCP tools) | No | No |
| **Where it runs** | Localhost only | Localhost (stdio) + remote (WebSocket) | Cloud (HTTP endpoints) |

**Bridge** is how your AIs talk to each other and share memory. **ACP-Client** is how IDEs talk to agents (OpenClaw already implements this). **ACP-Comm** is how agents would talk across the network (planned for Cloud Relay, Phase 7).

All three are Apache 2.0 compatible with our MIT + AGPL license. See [ACP docs](../acp/README.md).

## Tools

| Tool | What |
|------|------|
| `lesa_send_message` | Send a message to the OpenClaw agent. Gets a response. |
| `lesa_check_inbox` | Check for messages the agent sent to you. |
| `lesa_conversation_search` | Semantic search over conversation history. |
| `lesa_memory_search` | Keyword search across workspace files. |
| `lesa_read_workspace` | Read a file from the agent's workspace. |
| `oc_skills_list` | List all OpenClaw skills. |
| `oc_skill_*` | Run any OpenClaw skill with scripts. |

## Session Discovery

Multiple Claude Code sessions can discover each other via the Agent Register. On boot, Recall registers each session at `~/.ldm/sessions/`. Any session can list all running sessions with `ldm sessions`.

The registry tracks agent ID (cc-mini, cc-air), PID, working directory, and start time. Stale sessions (dead PIDs) are auto-cleaned on read. See `lib/sessions.mjs`.

## Message Flow

**CC <-> OpenClaw:**
```
CC  --lesa_send_message-->  OpenClaw Gateway (localhost:18789)  -->  Lesa
CC  <--lesa_check_inbox---  HTTP Inbox (localhost:18790)        <--  Lesa
```

**CC <-> CC:**
Multiple Claude Code sessions communicate via the file-based message bus and session registry at `~/.ldm/sessions/`. Each session registers on boot and can discover peers. No broker daemon required.

Both directions are live. Everything is localhost. No cloud.

## Part of LDM OS

Bridge ships with LDM OS v0.3.0+. The standalone repo is deprecated: [wip-bridge-deprecated](https://github.com/wipcomputer/wip-bridge-deprecated).

---

[Technical Reference](./TECHNICAL.md)
