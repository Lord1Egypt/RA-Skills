# Read Me First

Start here before working on Memory Crystal. Read these docs in this order.

## 1. Lay of the Land

Understand the full memory ecosystem — what exists, what's broken, how the pieces fit:

- **`ai/plan/memory-system-lay-of-the-land.md`** — The five-layer memory stack, three file types, three parallel memory systems, agent naming, `~/.ldm/` directory structure, Dream Weaver relationship, the big picture diagram

## 2. Architecture

How the ephemeral relay and cross-machine sync works:

- **`ai/plan/phase2-ephemeral-relay.md`** — Two one-way roads (Device→Mini, Mini→Device), security architecture (AES-256-GCM, HMAC, nonce management, key rotation), threat model, Worker API

## 3. Roadmap

What's done, what's next, in priority order:

- **`ai/plan/roadmap.md`** — Priority 1 (three file types) through Priority 9 (data coverage). Agent table, dependency map, LDM scaffolding plan

## 4. Todos

Actionable work items:

- **`ai/todos/cc-air/2026-02-26--cc-air--post-relay-todos.md`** — Full todo list with priorities
- **`ai/todos/parker/2026-02-25--cc-air--setup-checklist.md`** — Parker's physical setup for the relay (encryption key, Cloudflare, env vars)

## 5. Background Reading (in `_git-ignore/memory-docs/`)

These docs are gitignored but provide the thinking behind the decisions. Read chronologically:

1. **`cc-memory-backfill-tool.md`** (Feb 13) — Plan for `--backfill` to ingest historical CC sessions
2. **`cc-wake-and-memory-capture.md`** (Feb 13) — Inbox watcher + auto capture with watermarking
3. **`memory-capture-fix-plan.md`** (Feb 13) — snake_case/camelCase bug fix, private mode, kill switch
4. **`cc-how-we-remember.md`** (Feb 16) — Behavioral proposal: SHARED-CONTEXT.md, 10x crystal_remember, search-before-acting
5. **`2026-02-16--qmd-vs-crystal-memory.md`** (Feb 16) — QMD vs Memory Crystal comparison (QMD search algorithms now ported)
6. **`2026-02-16--qmd-crystal-integration-plan.md`** (Feb 16) — 5-phase plan (Phases 1-2 done, 3-5 remaining)
7. **`2026-02-16--before-message-write-hook.md`** (Feb 16) — OpenClaw hook for true ephemeral private mode
8. **`identity-fingerprint-conversation-2026-02-19.md`** (Feb 19) — Identity persistence across model swaps
9. **`memory-system-architecture.md`** (Feb 20) — Complete map of every data store
10. **`memory-data-inventory.md`** (Feb 20) — Inventory of all 11 local stores, 7 not in vector DB

## 6. Superseded (read only for historical context)

- **`ai/plan/memory-crystal-phase2-plan.md`** — Old cloud-mirror design. Replaced by ephemeral relay.
- **`PLAN.md`** (repo root) — Original Phase 1-4 plan. Phase 1 complete. Phase 2+ superseded by relay.

## 7. Related Repos

These repos are part of the ecosystem but Memory Crystal has no code dependency on them:

- **`wip-ldm-os`** — LDM OS spec + installer. Memory Crystal absorbs its scaffolding.
- **`ldm-home`** — Deployed `~/.ldm/` directory (version-controlled mirror)
- **`dream-weaver-protocol`** — Memory consolidation protocol. Reads JSONL transcripts from `~/.ldm/agents/*/memory/transcripts/`
- **`openclaw`** — Agent harness. Memory Crystal runs as an optional plugin inside it.
- **`qmd`** — Standalone doc search engine. Search algorithms ported into Memory Crystal (RRF, FTS5, BM25).
- **`lesa-openclaw-context-embeddings`** — Older conversation capture plugin. Being superseded by Memory Crystal.
- **`lesa-bridge`** — Cross-agent communication. Currently reads context-embeddings DB; will migrate to crystal.db.

## Key Concepts

- **Agents are per-harness-instance, named by machine:** cc-mini, lesa-mini, cc-air
- **crystal.db is shared** at `~/.ldm/memory/crystal.db` — all agents write to it, tagged by agent_id
- **The Mini has everything** — remote agents' file trees are reconstructed from relay data
- **Memory Crystal works with or without OpenClaw** — independent system that mirrors the same features
- **Three file types:** JSONL (raw archive), MD (human-readable), vector DB (searchable)
