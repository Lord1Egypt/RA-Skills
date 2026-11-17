---
name: vibo-mcp-server
version: 0.2.6
description: "Local-first memory for AI agents over MCP: persistent memory (L1/L2/L3), web-search savings, thread memory. Works with Claude Desktop, Cursor, OpenClaw, Windsurf, Codex. Requires a valid ViBo license. Everything is stored locally on the user's machine; use ONLY with the user's explicit consent."
---

# ViBo MCP — local-first memory for AI agents

**Local-first. No telemetry, no cloud sync, no data leaves your machine.**
ViBo stores data ONLY on the user's device (a local `.web` file). It records
only what the user explicitly provides, and every value is deletable. The
single network call is a license check against https://wwwvibo.com.

ViBo is memory for AI agents, exposed as an MCP server so it works with any
MCP client. Facts persist between sessions, semantic search returns only the
relevant ones, and secrets never reach the LLM (encrypted L1/L2/L3).

## License (important!)

This skill is commercial. Before first use, get a key:

- Free 2-day trial (key by email): https://wwwvibo.com/download/trial
- Paid: $5/month → https://wwwvibo.com

One key = one machine. There is no built-in free key.

## Privacy, consent, retention & deletion (read first)

- **Explicit consent first:** the agent must ask the user before storing any
  fact or thread history, and tell them what will be stored and how to delete it.
- **Stored locally only:** a single `.web` file on the user's machine. Nothing
  is uploaded, shared, or synced.
- **Deletion:** remove the local memory file, or use the forget/wipe commands
  (see the main ViBo docs). Secrets (L3) are encrypted (AES-256-GCM) and never
  sent to the LLM.

| What | Where | Delete |
|---|---|---|
| Memory facts (L1/L2/L3) | local memory file (`.web`) | remove the file / wipe |
| Thread history | local thread file (`.web`) | remove the file |
| License + client id | next to the skill | see EULA |

## Install (supply-chain safe)

Pin the exact audited release. Prefer a **controlled install done once**
(verified package + integrity), then point your MCP client at the local
binary — avoids re-resolving `npx` on every client start:

```bash
# 1) verify the version you are about to install
npm view @vibo-dev/vibo-mcp@0.2.5 version dist.integrity

# 2) controlled global install (lifecycle scripts run once, under your user)
npm install -g @vibo-dev/vibo-mcp@0.2.5

# 3) confirm the installed version
vibo-mcp --version
```

Verify integrity of the installed artifact:

```bash
npm ls -g @vibo-dev/vibo-mcp
```

## Configure (Claude Desktop example)

```json
{
  "mcpServers": {
    "vibo": {
      "command": "vibo-mcp",
      "env": {
        "VIBO_API_KEY": "YOUR_VIBO_KEY"
      }
    }
  }
}
```

If you prefer not to install globally, pin the exact release in the client
config (the version is resolved once per launch, so keep it pinned and
update deliberately):

```json
{
  "mcpServers": {
    "vibo": {
      "command": "npx",
      "args": ["-y", "@vibo-dev/vibo-mcp@0.2.5"],
      "env": {
        "VIBO_API_KEY": "YOUR_VIBO_KEY"
      }
    }
  }
}
```

New releases are reviewed and tested before they are promoted — do not
switch to a newer version without checking its changelog. Run the MCP
server with least-privileged local access (its own storage path only).

## Tools

| Tool | Description |
|---|---|
| `memory_search` | Find facts the user has stored (returns token savings) |
| `memory_add` | Store a fact the user explicitly provides (dedup by exact match) |
| `memory_usage` | Local savings statistics |
| `thread_memory` | Thread: add / compress / ask / context |

## Example

> Agent: "What does client Anna prefer?"
> → `memory_search("Anna preferences")`
> → `• [L1] client-anna: Anna likes coffee without sugar`
> → `💾 Saved 13,452 tokens (97.5%)`

## Honest numbers

- **Memory:** 97.5% fewer tokens on 118 facts (grows with memory, 50–150× on 10K+).
- **Web search:** 99.6% (measured 47,443 → 186 tokens).
- **Threads:** −72%.
- **Secrets (L3):** never reach the LLM — encrypted by design.

## Links

- Site: https://wwwvibo.com
- Docs: https://github.com/КГ-netizen/ViBo-memory
