# Memory Crystal — Roadmap

**Date:** 2026-02-26 (updated)
**Agent:** cc-air
**Based on:** memory docs review, ecosystem inspection, Dream Weaver analysis

## Vision

Memory Crystal is the universal archive manager for `~/.ldm/`. It works with or without OpenClaw, with any agent, on any harness. It produces three file types (JSONL copies, MD summaries, vector DB) and stores everything in one directory that gets backed up.

It includes its own `~/.ldm/` scaffolding — no dependency on the wip-ldm-os repo. Everything needed to set up the LDM directory structure is built into Memory Crystal's installer.

## What's Done

- [x] sqlite-vec migration (replaced LanceDB as primary, LanceDB kept as fallback)
- [x] FTS5 full-text search with BM25 scoring
- [x] Hybrid search: vector + keyword with RRF fusion (ported from QMD)
- [x] Recency weighting
- [x] Turn-boundary chunking (1 conversation message = 1 chunk)
- [x] CC Stop hook with watermark-based capture
- [x] MCP server (crystal_search, crystal_remember tools)
- [x] OpenClaw plugin (Lēsa's interface)
- [x] CLI (crystal search, crystal remember, crystal status)
- [x] Private mode (kill switch across CLI, MCP, OpenClaw, env var)
- [x] Ephemeral relay code: crypto, worker, cc-hook dual mode, poller, mirror-sync
- [x] Daily breadcrumb logs to `~/.ldm/agents/cc/memory/daily/`

## Priority 1 — Three File Types (the core gap)

Memory Crystal currently only produces the vector DB. It needs to produce all three:

### 1a. JSONL Archive
- [ ] **cc-hook: copy raw JSONL** to `~/.ldm/agents/{agent}/memory/transcripts/`
- [ ] Copy the new portion (or full file) after each capture
- [ ] This is Dream Weaver's primary input — must be preserved
- [ ] Solves the FDA backup problem (files now in a controlled, backupable location)

### 1b. MD Session Summaries
- [ ] **cc-hook: generate human-readable MD** per conversation
- [ ] Write to `~/.ldm/agents/{agent}/memory/sessions/YYYY-MM-DD-{slug}.md`
- [ ] Include: timestamp, session ID, conversation summary (user messages + key assistant responses)
- [ ] Matches what OpenClaw's session-memory hook produces, but independent of OpenClaw
- [ ] Consider: LLM-generated slug (like OpenClaw does) vs timestamp-only (simpler, no API call)

### 1c. crystal.db Location
- [ ] **Move or symlink** crystal.db to `~/.ldm/memory/crystal.db`
- [ ] Currently at `~/.openclaw/memory-crystal/crystal.db` — outside the LDM archive
- [ ] The DB is **shared** — all agents (cc-mini, lesa-mini, cc-air) read/write to it, tagged by agent_id
- [ ] On remote devices, a read-only mirror lives at the same path

## Priority 2 — LDM Scaffolding (no external dependency)

Memory Crystal must set up `~/.ldm/` itself. No dependency on wip-ldm-os repo.

- [ ] **Built-in scaffold** — `crystal init` or auto-scaffold on first run
- [ ] Create the full directory structure:
  ```
  ~/.ldm/
  ├── config.json
  ├── memory/
  │   └── crystal.db            (shared vector DB — all agents)
  └── agents/{agent_id}/
      ├── config.json
      └── memory/
          ├── transcripts/      (JSONL copies)
          ├── sessions/         (MD summaries)
          ├── daily/            (breadcrumb logs)
          └── journals/         (Dream Weaver output)
  ```
- [ ] Agent names are by machine: `cc-mini`, `lesa-mini`, `cc-air`
- [ ] Absorb relevant parts of `wip-ldm-os/bin/scaffold.sh` and templates
- [ ] Identity files (SOUL.md, IDENTITY.md, CONTEXT.md) — create empty templates or skip (agent-specific, not Memory Crystal's job)
- [ ] Config: agent name, harness type, Dream Weaver schedule

## Priority 3 — Deploy Ephemeral Relay + Expand Poller

**Branch:** `cc-air/phase2-relay`
**Blocked on:** Parker's physical setup (see `ai/todos/parker/`)

1. Generate encryption key, copy to both machines
2. `wrangler login`, create R2 bucket, set bearer tokens
3. Deploy Worker
4. Configure env vars (Air + Mini)
5. End-to-end test: capture → relay → ingest → mirror → search

### Poller expansion (Mini-side)
The poller already decrypts conversation data from remote agents. Expand it to reconstruct the remote agent's full file tree on the Mini:

- [ ] **Write JSONL** to `~/.ldm/agents/{agent_id}/memory/transcripts/`
- [ ] **Generate MD summary** to `~/.ldm/agents/{agent_id}/memory/sessions/`
- [ ] **Append daily breadcrumb** to `~/.ldm/agents/{agent_id}/memory/daily/`
- [ ] **Ingest into crystal.db** (already done)

No extra relay transfer — the Mini rebuilds everything from the same decrypted data. This ensures the Mini has a complete `~/.ldm/` for every agent, enabling Dream Weaver to run against any agent from the Mini.

## Priority 4 — Fix Broken Systems

- [ ] **Backup system** — FDA issue. Partially solved by JSONL copy to `~/.ldm/` (Priority 1a). Full fix: grant FDA or find alternative.
- [ ] **LanceDB removal** — Once sqlite-vec is validated, remove dual-write. Simplifies codebase, drops a dependency.
- [ ] **Retire context-embeddings** — Once Memory Crystal handles all three file types, disable the context-embeddings plugin in dot-openclaw. Update lesa-bridge to read from crystal.db instead.

## Priority 5 — Recovery & Backfill Tools

- [ ] **`crystal replay`** — Re-send from raw JSONL through the relay. Recovery for when Mini is offline >24h.
- [ ] **`crystal backfill`** — One-time ingest of all ~115 historical CC sessions (~110MB, ~$0.07).

## Priority 6 — Dream Weaver Integration

- [ ] **Trigger consolidation** — After poller ingests a batch, optionally kick off incremental Dream Weaver run.
- [ ] **Automate weekly schedule** — Currently manual. Add cron/launchd trigger based on `dreamWeaver.schedule` in config.
- [ ] **Dream Weaver reads from `~/.ldm/`** — Once JSONL copies live there, Dream Weaver reads from `transcripts/` instead of `~/.claude/projects/`.

## Priority 7 — Search Quality (QMD Phases 3–5)

- [ ] **Phase 3: Smart chunking + dedup** — Content-hash dedup, better non-conversation chunking.
- [ ] **Phase 4: Re-ranking + query expansion** — LLM re-ranking, synonym expansion. Biggest quality jump remaining.
- [ ] **Phase 5: Local embeddings** — Replace OpenAI with local model (GGUF via node-llama-cpp, like QMD uses).

## Priority 8 — Behavioral / Process

- [ ] **SHARED-CONTEXT.md** — Warm-start file agents read on boot. <50 lines, current state.
- [ ] **End-of-session handoffs** — Agent writes what-I-was-doing summary at session end.
- [ ] **Search-before-acting** — Agents search crystal before starting new work.

## Priority 9 — Data Coverage Expansion

7 of 11 data stores aren't in the vector DB. Review which warrant ingestion:
- [ ] CLAUDE.md memories, auto-memory, Dream Weaver narratives, dev updates, identity docs

## Agents

Each harness instance = one agent = one "user" in LDM. Named by machine:

| Agent ID | Machine | Harness |
|----------|---------|---------|
| `cc-mini` | Mac Mini | Claude Code |
| `lesa-mini` | Mac Mini | OpenClaw |
| `cc-air` | MacBook Air | Claude Code |
| Future: `kodaks-air` | MacBook Air | Kodaks |

Each agent writes its own files (transcripts, sessions, daily) to `~/.ldm/agents/{agent_id}/memory/`. All agents share one `crystal.db` at `~/.ldm/memory/`.

**The Mini has everything.** Remote agents' file trees are reconstructed on the Mini by the poller from decrypted relay data. If a device is lost, nothing is lost — Dream Weaver can be run against any agent from the Mini.

## Dependency Map

```
Memory Crystal (standalone — no external repo dependencies for core function)
├── sqlite-vec          (npm — vector search)
├── better-sqlite3      (npm — SQLite engine)
├── OpenAI API          (embedding provider — swappable for Ollama/local)
└── ~/.ldm/             (filesystem — scaffolded by Memory Crystal itself)

Optional integrations (not dependencies):
├── OpenClaw plugin     (if OpenClaw is installed, registers tools + agent_end hook)
├── Claude Code hook    (if CC is the harness, captures via Stop hook)
├── Ephemeral relay     (if multi-machine, Cloudflare Worker for sync)
└── Dream Weaver        (reads from ~/.ldm/agents/*/transcripts/, writes to ~/.ldm/agents/*/journals/)
```
