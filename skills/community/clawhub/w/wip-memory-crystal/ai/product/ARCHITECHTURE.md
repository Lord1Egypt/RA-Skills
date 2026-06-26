# Memory Crystal ... Read Me First

**Last updated:** 2026-03-15
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

As of v0.7.4, Memory Crystal handles Layers 1-4 (Dream Weaver is now integrated via `crystal dream-weave`). Layer 5 is partially automated via CONTEXT.md generation. All layers work together. Agent identity is config-driven via `~/.ldm/agents/*/config.json`.

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

**Crystal Node** ... any other device (MacBook Air, future machines). Captures raw conversations, sends to Core via encrypted relay. Gets back delta chunks (pre-embedded) + the full `~/.ldm/` file tree. Searches locally with its own crystal.db. If a Node dies, nothing is lost.

One Core, many Nodes. Core is the only embedder. Nodes capture and sync. The relay is pure transport (encrypted dead drop). No cloud search needed. Every node has the full database and full file tree. Delta sync means only new chunks and changed files transfer (not the full 1.9 GB+ database every time).

**Future: Native Apple app** replaces the relay for Apple-to-Apple devices. CloudKit for sync. MLX Swift for on-device LLM. No Cloudflare Worker needed between Apple devices.

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

## Databases (Current State)

| Database | Size | What It Stores | Managed By |
|----------|------|---------------|------------|
| `crystal.db` (`~/.ldm/memory/`) | ~1.45 GB, 73,908 chunks, 343 memories | Conversations + manual memories (file scans removed 2026-03-11) | Memory Crystal (our product) |
| `main.sqlite` (`~/.openclaw/memory/`) | 6.1 GB | Workspace files + sessions | OpenClaw core (not ours) |

**crystal.db is the one database for all conversation memory.** As of 2026-03-13, the database contains 73,908 conversation chunks and 343 memories. 141,652 bulk file-scan chunks were removed on 2026-03-11 (raw directory indexing without conversational context). Orphaned vectors and FTS entries were cleaned on 2026-03-13 (database went from 1.96 GB to 1.45 GB). A DELETE trigger now prevents orphans on future deletes. The context-embeddings plugin is disabled (migrated into crystal.db on 2026-03-04). main.sqlite stays (OpenClaw built-in, not ours to touch).

**Product rule (2026-03-13):** Memory Crystal indexes conversations only. File content that appears in conversation turns (agent reads a file, discusses it) is captured as part of the conversation. Raw directory scanning without conversational context is not what Memory Crystal is for.

**Retired:** `context-embeddings.sqlite` (`~/.openclaw/memory/`) ... 124 MB. Migrated into crystal.db. Plugin disabled. File and extension preserved as backup. Can re-enable by setting `enabled: true` in openclaw.json.

---

## Raw Files Are Ground Truth

None of the databases ARE the memory. They're indexes. The actual memory is the raw files:

- **Session JSONLs** ... every message, tool call, response from Day 1
- **Workspace .md files** ... curated knowledge (MEMORY.md, TOOLS.md, daily logs)
- **Journals** ... Dream Weaver narrative output

If any database is corrupted, lost, or wrong, we rebuild from the raw files. That's what `crystal backfill` is for. LDM must have copies of everything. No exceptions.

---

## Capture Architecture (How Memory Survives Compaction)

Two agents, two completely different capture strategies. Both solve the same problem: context compaction destroys in-memory state, so memory capture must not depend on it.

### Lesa (OpenClaw): agent_end Hook

```
OpenClaw turn completes
  -> agent_end fires (every turn, synchronous)
  -> openclaw.ts reads event.messages (the current messages array)
  -> Compares messages.length to stored counter (last capture position)
  -> If messages.length < storedCount: COMPACTION DETECTED, reset to 0
  -> Extracts new messages from startIndex to end
  -> Chunks and ingests into crystal.db
  -> Updates stored counter
  -> Syncs raw data to ~/.ldm/ (transcripts, workspace, daily logs)
```

**Key file:** `src/openclaw.ts` (line 124: `api.on('agent_end', ...)`)

**Compaction fix (2026-02-13):** Before the fix, the stored counter was higher than the post-compaction messages array length. The hook saw `messages.length <= storedCount` and returned early ("nothing new") forever. Fix: detect when `messages.length < storedCount` and reset `startIndex` to 0. Re-ingest from the beginning of the current context.

**Why this works for OpenClaw:** The gateway is always running. `agent_end` fires reliably on every turn. The messages array is the authoritative source. Compaction is the only failure mode, and the reset-to-zero fix handles it.

### Claude Code: Cron Poller + Stop Hook Redundancy

```
Claude Code writes JSONL to ~/.claude/projects/*/*.jsonl (append-only, always)
  |
  v
Cron job (every 1 min, via crontab)
  -> crystal-capture.sh calls cc-poller.js
  -> Scans ALL .jsonl files across all sessions
  -> Reads new bytes from each file using byte-offset watermark
  -> Chunks and ingests into crystal.db
  -> Writes daily log breadcrumbs
  -> Archives transcripts to ~/.ldm/agents/cc-mini/memory/transcripts/
  |
  v (redundancy only)
Stop hook (cc-hook.js, fires if session ends cleanly)
  -> Same logic: checks watermark, flushes anything poller missed
```

**Key files:** `src/cc-poller.ts` (primary), `src/cc-hook.ts` (backup)
**Cron script:** `~/.ldm/bin/crystal-capture.sh`
**Watermark:** `~/.ldm/state/cc-capture-watermark.json` (byte offsets per JSONL file)

**Why the poller, not just a hook:** Claude Code sessions are unreliable. They hang for days. Remote connections fork silently. Compaction wipes model context without warning. The Stop hook only fires if the session ends cleanly, which it often doesn't. The 72-hour session (2026-02-27 to 2026-03-01) produced 50MB of JSONL and zero crystal chunks because Stop never fired.

**Why compaction doesn't matter for CC:** The poller reads from the JSONL file on disk, not from the messages array. The JSONL is append-only. Compaction affects the model's in-memory context but never touches the JSONL. The poller doesn't know or care if compaction happened. It just reads new bytes from the file.

**The conceptual difference:**
- **Lesa:** Capture is tied to the harness lifecycle (agent_end). Compaction is handled by detecting and resetting.
- **CC:** Capture is completely decoupled from the session lifecycle. The JSONL on disk is the source of truth. Compaction is irrelevant.

### Why Two Different Approaches

OpenClaw provides a reliable `agent_end` hook that fires every turn with the full messages array. Using it is the right choice. The compaction detection is a one-line fix.

Claude Code provides nothing equivalent. The Stop hook is unreliable. There is no "after every turn" hook. The only reliable signal is the JSONL growing on disk. So capture must be external.

Same goal, different constraints, different solutions. Both produce the same output: chunks in crystal.db, raw files in `~/.ldm/`.

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
| `src/llm.ts` | LLM provider cascade (MLX > Ollama > OpenAI > Anthropic), query expansion, re-ranking |
| `src/search-pipeline.ts` | Deep search pipeline: expand, search, RRF, rerank, blend |
| `src/mcp-server.ts` | MCP server: crystal_search, crystal_remember, crystal_forget |
| `src/openclaw.ts` | OpenClaw plugin: agent_end hook, tool registration |
| `src/bridge.ts` | Bridge detection and MCP registration |
| `src/dream-weaver.ts` | Bridge between Dream Weaver engine and Memory Crystal hooks |
| `src/crystal-serve.ts` | Crystal Core gateway (localhost HTTP server, OpenAI-compatible) |
| `src/staging.ts` | Staging pipeline for new agents from relay |
| `src/worker.ts` | Cloudflare Worker: encrypted relay (conversations + mirror + commands channels) |
| `src/crypto.ts` | AES-256-GCM encryption for relay |
| `src/mirror-sync.ts` | Node-side: pull delta chunks + file tree deltas from Core |
| `src/file-sync.ts` | Manifest-based file tree delta sync (planned) |

---

## Key Documents

| Document | Location (relative to ai/product/) |
|----------|-----------------------------------|
| **This file** | `readme-first.md` (also in `plans-prds/readme-first.md`) |
| **Roadmap** | `plans-prds/roadmap.md` |
| **v0.6.0 plan** | `plans-prds/sort/2026-03-04--cc-mini--v0.6.0-dream-weaver-and-crystal-core.md` |
| **v0.5.0 plan** | `plans-prds/sort/2026-03-04--cc-mini--init-discovery-and-consolidation.md` |
| **v0.4.0 plan** | `plans-prds/sort/2026-03-03--v0.4.0-implementation.md` |
| **Onboarding flow** | `plans-prds/sort/2026-03-03--onboarding-flow.md` |
| **Memory consolidation** | `plans-prds/sort/mem-consolidation/investigation.md` |
| **Raw data gaps** | `plans-prds/sort/mem-consolidation/raw-data-gaps.md` |
| **LDM OS architecture** | `plans-prds/sort/ldm-os-install-and-boot-architecture.md` |
| **Memory system overview** | `plans-prds/sort/memory-system-lay-of-the-land.md` |
| **Search quality plan (full)** | `plans-prds/current/search-quality-full-plan.md` |
| **Search quality plan (original)** | `plans-prds/current/search-quality-qmd-port.md` |
| **External reviews** | `product-ideas/external-reviews-v0.6.0.md` |
| **Crystal Capture idea** | `product-ideas/crystal-capture-auto-capture.md` |
| **Local embeddings idea** | `product-ideas/local-embeddings-zero-config.md` |
| **Delta sync + LDM tree plan** | `plans-prds/current/delta-sync-full-ldm-tree.md` |
| **LDM OS Native App idea** | `product-ideas/native-apple-app-crystal-sync.md` |
| **Dream Weaver Protocol** | `ldm-os/components/dream-weaver-protocol-private/DREAM-WEAVER-PROTOCOL.md` |

---

## What's Built (as of v0.7.8, 2026-03-13)

- Layers 1-3 complete: raw file capture, embedding, hybrid search, crystal_remember, crystal_forget
- Layer 4 complete: Dream Weaver integration via `crystal dream-weave` (full + incremental modes)
- Layer 5 partial: CONTEXT.md generated by Dream Weaver, not yet auto-updated outside DW runs
- **Deep search (default):** LLM-powered query expansion (3 variations) + re-ranking (top 40 candidates) + position-aware score blending. Falls back silently if no LLM provider available.
- **LLM provider cascade:** MLX (local, free) > Ollama > OpenAI API > Anthropic API > none. Local-first by design.
- **Time-filtered search:** `--since 24h/7d/30d` on CLI, `time_filter` on MCP
- **Stronger recency curve:** Exponential decay with floor 0.3 (was linear, floor 0.5)
- Per-harness discovery: detects Claude Code and OpenClaw installations
- Bulk copy: idempotent raw file copy to LDM (transcripts + workspace + daily logs)
- Backfill: embed historical sessions into crystal.db
- CE migration: merge context-embeddings into crystal ($0 cost)
- Core/Node architecture: role detection, encrypted relay, mirror sync
- Crystal Core gateway: `crystal serve` on localhost:18790, OpenAI-compatible
- Staging pipeline: new agents from relay auto-detected, staged, backfilled, dream-woven, promoted
- Commands channel: bidirectional relay (Node...Core) for remote command dispatch
- OpenClaw raw data sync: sessions, workspace, daily logs copied to LDM on every agent_end turn
- Harness-aware init: different behavior for OpenClaw vs Claude Code, Core vs Node
- Doctor: 10-check health system
- Backup: daily LaunchAgent, configurable destination

## What's Built (v0.7.5-v0.7.8, 2026-03-11 to 2026-03-13)

- DELETE trigger on chunks table cascading to chunks_vec and chunks_fts (prevents orphaned entries)
- `crystal cleanup` CLI command with `--dry-run` (orphan removal, FTS rebuild, VACUUM)
- Doctor detects 1Password SA token as embedding provider (no more false "FAILING")
- Install prompt updated to new standard format (4 explain questions, installed check, dry-run)
- Agent ID config via `~/.ldm/agents/*/config.json` instead of hardcoding

## What's Missing (as of v0.7.19)

- **Search quality tuning:** Score normalization (100% scores), expansion/reranking cache to DB, grammar-constrained expansion output.
- **MLX auto-install (Phase 3):** `crystal init` should detect Apple Silicon and install MLX + LaunchAgent for always-on local LLM. See `current/search-quality-full-plan.md`.
- **MCP sampling (Phase 4):** Blocked on Anthropic (Issue #1785). Would let Crystal use Claude Max subscription for LLM calls.
- **lesa-bridge update:** `lesa_conversation_search` still points at context-embeddings.sqlite. Should point at crystal.db or be removed (crystal_search covers it now).
- **Crystal Capture adapters:** Auto-capture from ChatGPT Desktop, Claude Desktop, Cursor, browsers. See `product-ideas/crystal-capture-auto-capture.md`.
- **Local embeddings:** Zero-config default (ONNX + MiniLM-L6-v2). See `product-ideas/local-embeddings-zero-config.md`.
- **Chunked Dream Weaver:** 200K char cap means full mode is lossy for mature agents. Need multi-pass consolidation.
- **Delta sync + full LDM tree sync:** Mirror currently pushes full crystal.db (1.9 GB). Needs delta chunks only. Also needs to sync the full `~/.ldm/` file tree (workspace, daily logs, journals, media), not just the database. Embeddings are pointers to artifacts; artifacts must exist on every node. See `current/delta-sync-full-ldm-tree.md`.
- **Cloud search deprecation:** With full LDM sync, every node searches locally. The Cloud MCP server (D1 + Vectorize) is deprecated for production. Keep as demo/onboarding.
- **Core...Node command dispatch:** Relay Worker supports bidirectional, but Core-side sender isn't wired up.
- **Layer 5 automation:** CONTEXT.md not auto-updated outside Dream Weaver runs.
- **README simplification:** Too many concepts for first-time readers. Need 30-second mental model.
- **LDM OS Native App:** macOS + iOS app combining Memory Crystal, MLX Swift local LLM, and agent secrets vault. Replaces relay for Apple-to-Apple sync. See `product-ideas/native-apple-app-crystal-sync.md`.

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

### No Cloud Search

Every node has the full crystal.db + full `~/.ldm/` file tree. All search is local. There is no cloud search layer in the production architecture.

The Cloud MCP demo server (`worker-mcp.ts`, D1 + Vectorize) exists for onboarding and testing but is not the real system. With delta sync, every device that has Memory Crystal installed searches its own local database.

For Apple devices, the native app (future) replaces the relay entirely. CloudKit handles sync. MLX Swift handles on-device LLM. No Cloudflare Worker needed between Apple devices.

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
