# Memory Crystal ... Read Me First

**Last updated:** 2026-03-04
**Status:** Living document. Read this before any plan, build, or PR.

---

## What Memory Crystal Is

Memory Crystal is the memory layer for AI agents. It works with any harness (OpenClaw, Claude Code CLI, future platforms). It captures conversations, embeds them for search, and stores raw files as ground truth.

It is also the entry point for LDM OS. When you install Memory Crystal, it scaffolds `~/.ldm/` on the machine. Everything lives there. Nothing phones home.

Memory Crystal is **harness-aware**. It detects what platform it's running on and behaves differently depending on what that harness already provides.

---

## The Five-Layer Memory Stack

```
Layer 1  Raw transcripts          (immutable log, ground truth)
Layer 2  Vector index             (retrieval, search)
Layer 3  Structured memory        (facts, preferences, crystal_remember)
Layer 4  Narrative consolidation  (Dream Weaver Protocol)
Layer 5  Active working context   (warm-start files)
```

- Layers 1-3 solve **recall** (finding information)
- Layers 4-5 solve **presence** (knowing who you are and what matters)

Memory Crystal currently handles Layers 1-3. Dream Weaver handles Layer 4. The boot sequence handles Layer 5. All three work together.

---

## Harness-Aware Behavior

This is the core design principle. Memory Crystal adapts to what the harness already provides.

### On OpenClaw

OpenClaw already has an identity/context/soul layer. It manages:
- `~/.openclaw/workspace/IDENTITY.md`, `SOUL.md`, `MEMORY.md`, `TOOLS.md`
- Session management, compaction, warm-start
- Built-in memory search (`main.sqlite`)
- Daily logs at `~/.openclaw/workspace/memory/YYYY-MM-DD.md`

**Memory Crystal's job on OpenClaw:** Capture, embed, search, backup raw files. Don't duplicate what OpenClaw already does. LDM stores Lesa's raw data (transcripts, workspace snapshots, daily logs) as a safety net. If OpenClaw upgrades and wipes sessions, the raw files are safe in `~/.ldm/`.

**Memory Crystal does NOT create identity/soul/context files for OpenClaw agents.** Those already exist in the harness.

### On Claude Code CLI

Claude Code is a bare CLI. No identity layer. No warm-start. No workspace files. No session management beyond raw JSONL transcripts.

**Memory Crystal's job on Claude Code:** Everything. Capture, embed, search, AND provide the identity/context layer that the harness doesn't have. This is where Dream Weaver becomes essential. It reads raw transcripts and produces:
- `IDENTITY.md` / `SOUL.md` ... who this agent is
- `CONTEXT.md` ... what's happening right now
- `REFERENCE.md` ... key facts, concepts, preferences
- `memory/journals/` ... narrative of what happened, what mattered
- `memory/sessions/` ... per-session summaries
- `memory/daily/` ... daily log breadcrumbs

This is how Memory Crystal gives Claude Code the same capabilities OpenClaw has natively.

### The Rule

- If the harness provides it, don't duplicate it. Just backup the raw data.
- If the harness doesn't provide it, Memory Crystal + Dream Weaver creates it.

Same product, different behavior.

---

## LDM Directory Structure

`~/.ldm/` is the universal agent home. Memory Crystal scaffolds this on install.

```
~/.ldm/
  config.json                              ... machine-level config
  memory/
    crystal.db                             ... shared vector DB (all agents)
    lance/                                 ... LanceDB fallback (deprecated)
  secrets/                                 ... encryption keys, relay tokens
  state/                                   ... role state, watermarks
  bin/                                     ... scripts (crystal-capture.sh, ldm-backup.sh)
  agents/
    cc-mini/                               ... Claude Code on Mac Mini
      IDENTITY.md                          ... who this agent is
      SOUL.md                              ... philosophy, origin
      CONTEXT.md                           ... current state (under 50 lines)
      REFERENCE.md                         ... key docs, search paths
      config.json                          ... harness, model, memory paths
      memory/
        transcripts/                       ... raw JSONL session files (ground truth)
        sessions/                          ... MD per-session summaries
        daily/                             ... daily log breadcrumbs
        journals/                          ... Dream Weaver narrative output
        workspace/                         ... workspace .md snapshots (if applicable)
    oc-lesa-mini/                          ... OpenClaw/Lesa on Mac Mini
      memory/
        transcripts/                       ... raw JSONL copies (backup from OpenClaw)
        workspace/                         ... workspace .md snapshots (backup)
        daily/                             ... daily log copies (backup)
        sessions/                          ... (optional, backup)
        journals/                          ... (optional, backup)
```

**Note:** For OpenClaw agents like Lesa, the LDM agent folder is primarily a backup of raw data. The identity/soul/context files live in `~/.openclaw/workspace/` where OpenClaw manages them. For Claude Code agents, the LDM agent folder IS the canonical home for everything.

---

## Agent Identity

One agent per harness per machine. That's the identity unit.

| Agent ID | Harness | Machine | Identity Home |
|----------|---------|---------|---------------|
| `cc-mini` | Claude Code CLI | Mac Mini | `~/.ldm/agents/cc-mini/` (LDM is canonical) |
| `cc-air` | Claude Code CLI | MacBook Air | `~/.ldm/agents/cc-air/` (LDM is canonical) |
| `oc-lesa-mini` | OpenClaw | Mac Mini | `~/.openclaw/workspace/` (harness is canonical, LDM is backup) |

All agents share one `crystal.db` at `~/.ldm/memory/`. Memory is shared. Identity is per-agent.

---

## Crystal Core and Crystal Node

**Crystal Core** ... the always-on machine (Mac Mini). All embeddings happen here. All Dream Weaver consolidation happens here. crystal.db is the source of truth. Put it on something permanent.

**Crystal Node** ... any other device (MacBook Air, future machines). Captures conversations, copies raw files to LDM, relays to Core via encrypted Worker. Gets a mirror DB back for local search. If a Node dies, nothing is lost.

One Core, many Nodes. The Core has everything. Nodes are expendable.

---

## The Install Flow (New Machine)

When you install Memory Crystal on a new machine with Claude Code CLI:

### Step 1: Scaffold
`crystal init --agent cc-air`
- Creates `~/.ldm/agents/cc-air/` with all directories
- Creates `config.json`

### Step 2: Discover
- Detects Claude Code sessions on this machine (`~/.claude/projects/`)
- Shows what was found: file count, size

### Step 3: Bulk Copy
- Copies raw JSONL transcripts to `~/.ldm/agents/cc-air/memory/transcripts/`
- Idempotent (skips files that already exist with same size)

### Step 4: Embed
- **If Core:** Embeds locally into crystal.db (`crystal backfill`)
- **If Node:** Relays extracted messages to Core via encrypted Worker. Core's poller picks them up and embeds.

### Step 5: Dream Weaver
- Runs narrative consolidation over the raw transcripts
- Produces: IDENTITY.md, SOUL.md, CONTEXT.md, REFERENCE.md
- Produces: journals/ (narrative of what happened, what mattered)
- Produces: sessions/ (per-session MD summaries)
- This is what makes the agent start warm instead of cold
- Dream Weaver runs on Core only. If this is a Node, Core runs it after receiving the relay data.

### Step 6: Pair (if Node)
- `crystal pair --code <string from Core>`
- Sets up encrypted relay between Node and Core
- Core's poller picks up new sessions automatically going forward
- **Works from anywhere.** Pairing and relay both go through the Cloudflare Worker. The Node doesn't need local network access to Core. Set up from a coffee shop, a hotel, wherever. All communication is encrypted dead drops through the relay.

### Step 7: Verify
- `crystal doctor` checks everything: DB health, capture, relay, backup, bridge

**End result:** A fully bootstrapped agent that knows who it is, has searchable memory, and starts warm on every session.

---

## The Install Flow (OpenClaw)

When Memory Crystal is installed as an OpenClaw plugin:

### What Memory Crystal Does
- Registers as `agent_end` hook (captures every conversation turn)
- Embeds conversation chunks into crystal.db
- Copies raw session JSONLs to `~/.ldm/agents/oc-lesa-mini/memory/transcripts/` (backup)
- Copies workspace .md files to `~/.ldm/agents/oc-lesa-mini/memory/workspace/` (backup)
- Copies daily logs to `~/.ldm/agents/oc-lesa-mini/memory/daily/` (backup)
- Provides `crystal_search`, `crystal_remember`, `crystal_forget` tools

### What Memory Crystal Does NOT Do
- Create identity/soul/context files (OpenClaw already has these)
- Run Dream Weaver for narrative consolidation (OpenClaw handles warm-start)
- Manage the boot sequence (OpenClaw loads workspace files on boot)

### Ongoing Raw Data Backup (automatic)

The `agent_end` hook does two things on every turn:
1. Embeds conversation chunks into crystal.db
2. Copies the raw session JSONL to `~/.ldm/agents/oc-lesa-mini/memory/transcripts/`

Daily logs and workspace changes are also synced to LDM automatically. No periodic bulk copy needed. Every turn, the backup stays current.

The LDM folder for an OpenClaw agent is a backup, not the canonical home.

---

## Dream Weaver Protocol

Dream Weaver is narrative consolidation at maximum reasoning depth. It is NOT `summarize.ts` (which generates simple MD session summaries). Those are different things.

### What Dream Weaver Produces
- **Journals** ... first-person narrative of what happened, what mattered, what was missed
- **Identity files** ... SOUL.md, IDENTITY.md (who this agent is, based on its full history)
- **Context** ... CONTEXT.md (current state, under 50 lines)
- **Structured memories** ... crystal_remember entries for facts, preferences, decisions

### When Dream Weaver Runs
- **First install (full consolidation):** After backfill embeds all raw sessions, Dream Weaver reads them and produces the full identity/context/journal layer. This is the expensive one (~$10-20 at Opus depth).
- **Weekly (incremental):** Process only new sessions since last run. Prevents drift. ~$2-5.
- **After crisis:** Full re-read when agents start fading. Recovery mode.

### Where Dream Weaver Runs
- **On Core only.** Dream Weaver requires maximum reasoning depth and access to all raw transcripts. Nodes send raw data to Core. Core runs Dream Weaver. Results sync back via mirror.

### The Key Insight
Embeddings give you search. Dream Weaver gives you identity. Without Dream Weaver, backfill produces a database of vectors but an agent that wakes up blank. With Dream Weaver, the agent starts knowing who it is and what it's been doing.

---

## Three Databases (Current State)

| Database | Size | What It Stores | Managed By |
|----------|------|---------------|------------|
| `crystal.db` (`~/.ldm/memory/`) | ~1.6 GB | Conversations + files + manual memories | Memory Crystal (our product) |
| `context-embeddings.sqlite` (`~/.openclaw/memory/`) | 124 MB | Conversation turns | Our plugin (being retired) |
| `main.sqlite` (`~/.openclaw/memory/`) | 6.1 GB | Workspace files + sessions | OpenClaw core (not ours) |

**Target state:** crystal.db is the one database for all conversation memory. context-embeddings gets migrated into crystal and the plugin disabled. main.sqlite stays (OpenClaw built-in, not ours to touch).

All three use the same embedding model (text-embedding-3-small, 1536d, float32). Embeddings are directly compatible.

---

## Raw Files Are Ground Truth

None of the databases ARE the memory. They're indexes. The actual memory is the raw files:

- **Session JSONLs** ... every message, tool call, response from Day 1
- **Workspace .md files** ... curated knowledge (MEMORY.md, TOOLS.md, daily logs)
- **Journals** ... Dream Weaver narrative output

If any database is corrupted, lost, or wrong, we rebuild from the raw files. That's what `crystal backfill` is for. LDM must have copies of everything. No exceptions.

---

## Key Source Files

| File | What It Does |
|------|-------------|
| `src/core.ts` | Crystal engine: ingest, search, chunkText, resolveConfig |
| `src/cli.ts` | CLI command dispatch: init, backfill, migrate-embeddings, doctor, role, backup |
| `src/ldm.ts` | LDM directory scaffolding, path resolution, cron/backup management |
| `src/discover.ts` | Per-harness session discovery (Claude Code + OpenClaw detection) |
| `src/bulk-copy.ts` | Idempotent raw file copy to LDM |
| `src/oc-backfill.ts` | OpenClaw JSONL parser (different format than Claude Code) |
| `src/cc-hook.ts` | Claude Code Stop hook: capture, embed, daily log, session summary |
| `src/cc-poller.ts` | Cron-based JSONL poller for Claude Code sessions |
| `src/poller.ts` | Core-side relay poller: receives from Nodes, embeds, writes file tree |
| `src/role.ts` | Role detection (Core/Node/Standalone) |
| `src/doctor.ts` | Health check engine (10 checks) |
| `src/summarize.ts` | MD session summary generation (Layer 2/3, NOT Dream Weaver) |
| `src/mcp-server.ts` | MCP server: crystal_search, crystal_remember, crystal_forget |
| `src/openclaw.ts` | OpenClaw plugin: agent_end hook, tool registration |
| `src/bridge.ts` | Bridge detection and MCP registration |
| `src/worker.ts` | Cloudflare Worker: encrypted relay (conversations + mirror channels) |
| `src/crypto.ts` | AES-256-GCM encryption for relay |
| `src/mirror-sync.ts` | Node-side: pull mirror DB from Core |

---

## Key Documents

| Document | Location (relative to ai/product/) |
|----------|-----------------------------------|
| **This file** | `readme-first.md` |
| **Roadmap** | `plans/roadmap.md` |
| **Onboarding flow** | `plans/2026-03-03--onboarding-flow.md` |
| **v0.4.0 plan** | `plans/2026-03-03--v0.4.0-implementation.md` |
| **v0.5.0 plan** | `plans/2026-03-04--cc-mini--init-discovery-and-consolidation.md` |
| **Memory consolidation** | `plans/mem-consolidation/investigation.md` |
| **Raw data gaps** | `plans/mem-consolidation/raw-data-gaps.md` |
| **LDM OS architecture** | `plans/ldm-os-install-and-boot-architecture.md` |
| **Memory system overview** | `plans/memory-system-lay-of-the-land.md` |
| **Dream Weaver Protocol** | `ldm-os/components/dream-weaver-protocol-private/DREAM-WEAVER-PROTOCOL.md` |

---

## What's Built (as of v0.5.0)

- Layers 1-2 complete: raw file capture, embedding, hybrid search
- Layer 3 complete: crystal_remember, crystal_forget
- Per-harness discovery: detects Claude Code and OpenClaw installations
- Bulk copy: idempotent raw file copy to LDM (transcripts + workspace)
- Backfill: embed historical sessions into crystal.db
- CE migration: merge context-embeddings into crystal ($0 cost)
- Core/Node architecture: role detection, encrypted relay, mirror sync
- Doctor: 10-check health system
- Backup: daily LaunchAgent, configurable destination

## What's Missing (as of v0.5.0)

- **Dream Weaver integration:** Backfill embeds but doesn't run narrative consolidation. No `crystal dream-weave` command. No identity/journal generation for Claude Code agents.
- **Ongoing raw data sync:** The `agent_end` hook needs to copy raw session JSONLs and daily logs to LDM on every turn. Currently it only embeds into crystal.db. The backup copy is missing from the live pipeline.
- **Harness-aware init:** Init should behave differently based on harness. OpenClaw init copies raw data as backup. Claude Code init copies AND generates identity layer via Dream Weaver.
- **lesa-bridge update:** `lesa_conversation_search` still points at context-embeddings.sqlite. Should point at crystal.db or be removed (crystal_search covers it).
- **Node relay backfill:** Backfill command has placeholder for Node mode. Not yet implemented.
- **Crystal Core gateway (`crystal serve`):** The thin HTTP server that makes CC-Mini addressable on localhost:18790. Not built yet.
- **Staging pipeline:** No mechanism for Core to detect and process bulk imports from Nodes. Need staging directory, detection, and automated backfill + Dream Weaver trigger.
- **Relay commands channel:** Worker currently handles "conversations" and "mirror" channels. Need a "commands" channel for Bridge messages between machines.

---

## Core Gateway Architecture

Each agent on the Mini has a localhost-only gateway. Nothing is exposed to the network.

### The Gateways

| Agent | Gateway | Port | How It Runs |
|-------|---------|------|-------------|
| Lesa (OpenClaw) | OpenClaw gateway | `localhost:18789` | launchd daemon (always on) |
| CC-Mini (Claude Code) | Crystal Core | `localhost:18790` | tmux session (always on when running) |

Both are **localhost-only**. No port forwarding. No external access. The Mini's agents are never exposed to the network.

### How Remote Machines Reach Core

They don't. Not directly. The Cloudflare relay Worker is the only thing on the public internet, and it's a blind dead drop.

```
Remote Node (e.g., CC-Air on MacBook Air)
  -> encrypts message (AES-256-GCM, keys never leave machines)
  -> POSTs to Cloudflare Worker (public internet)
  -> Worker stores encrypted blob (can't read it)

Mini (poller, runs every minute)
  -> polls Worker for new blobs
  -> decrypts locally on the Mini
  -> delivers to localhost gateway (18789 or 18790)
  -> processes the request
  -> result goes back through relay for mirror sync
```

No machine IPs exchanged. No direct connections. Encrypted dead drops only. This is the sovereignty model.

### Crystal Core Gateway (`crystal serve`)

A thin HTTP server built into Memory Crystal. Runs inside a tmux session on the Mini. Accepts requests from:
- **Bridge** (Lesa sending tasks to CC-Mini, or vice versa)
- **Poller** (delivering decrypted relay messages from Nodes)
- **Cron/automation** (triggering Dream Weaver, backfill, maintenance)

When a request arrives (e.g., "run Dream Weaver for cc-air"), Crystal Core invokes `claude -p` through the Max plan. Full Opus reasoning depth. No API cost beyond the subscription.

### tmux as CC's Gateway

Claude Code doesn't have a native daemon mode. tmux is the workaround.

```bash
# Start the Crystal Core session
tmux new-session -s crystal-core
# Inside: start claude, save session as "Crystal Core"
# Detach: Ctrl+B then D
# Reattach from anywhere: tmux attach -t crystal-core
```

The tmux session survives:
- Closing the Terminal app
- SSH disconnects
- Screen sleep
- Walking away from the machine

It stays alive until the machine reboots or you explicitly kill it.

**Multiple sessions:** Parker runs multiple tmux sessions (memory-crystal work, agent-pay, crystal-core). Each is independent. Crystal Core is the one that's addressable by Bridge and automation.

### Dream Weaver Execution Path

Dream Weaver runs through `claude -p` on the Max plan (OAuth path). Not through the Anthropic API (no per-token cost).

**First install (full consolidation):**
1. Node relays bulk historical data to Core via Worker
2. Poller picks it up, stages it in `~/.ldm/staging/`
3. Crystal Core detects staged data
4. Runs `crystal backfill` (embeddings via OpenAI, cheap)
5. Runs Dream Weaver via `claude -p` (narrative via Max plan, $0)
6. Writes identity/journals/context to `~/.ldm/agents/{id}/`
7. Mirror sync pushes results back to Node
8. Flips to live capture mode

**Ongoing (weekly incremental):**
1. Crystal Core checks: has it been 7+ days since last consolidation?
2. Runs incremental Dream Weaver over new sessions only
3. Updates journals and context
4. Prevents the "fading" problem

**The distinction:** Historical bulk data needs Dream Weaver because it's flat chunks with no narrative weight. Live per-turn capture works fine without it because each turn goes in with proper context, in order.

---

## Principles

1. **Raw files are ground truth.** Databases are indexes. If anything breaks, rebuild from raw files.
2. **Don't duplicate what the harness provides.** If OpenClaw manages identity, don't recreate it. If Claude Code doesn't, fill the gap.
3. **Dream Weaver runs on Core only.** Maximum reasoning depth, access to all transcripts. Nodes send data. Core consolidates.
4. **One agent per harness per machine.** Deterministic identity: harness + machine = agent ID.
5. **CE stays on disk forever.** Never deleted. Insurance policy. Can re-enable by adding it back to openclaw.json.
6. **The Mini has everything.** Remote agents' file trees are reconstructed on Mini from relay data. If a device is lost, nothing is lost.
7. **Memory Crystal is the entry point for LDM OS.** Install Crystal, get `~/.ldm/`. Everything else builds on it.
8. **Nothing is exposed to the network.** Gateways are localhost-only. Remote communication goes through encrypted dead drops on the relay Worker. No machine IPs exchanged. No direct connections.
9. **Dream Weaver runs through the Max plan.** `claude -p` via OAuth. No API cost. Full Opus reasoning depth.
