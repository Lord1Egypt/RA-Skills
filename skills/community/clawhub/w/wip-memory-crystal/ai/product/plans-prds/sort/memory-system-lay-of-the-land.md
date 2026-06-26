# Memory System — Lay of the Land

**Date:** 2026-02-26 (updated)
**Agent:** cc-air
**Sources:** 10 memory docs from `_git-ignore/memory-docs/` (Feb 13–20), codebase + ecosystem inspection

## Design Principle

Memory Crystal runs **alongside** OpenClaw's builtin memory — not replacing it. OpenClaw continues to evolve independently. Memory Crystal mirrors the same capabilities so it works **with or without** OpenClaw, with any agent, on any harness.

Everything Memory Crystal manages lives in `~/.ldm/` — one directory, one backup target, one source of truth.

## The Five-Layer Memory Stack

```
Layer 1 — Raw transcripts (JSONL)              immutable archive
Layer 2 — Vector index (crystal.db)             Memory Crystal
Layer 3 — Structured memory (daily logs, etc.)  crystal_remember + cc-hook
Layer 4 — Narrative consolidation               Dream Weaver
Layer 5 — Active working context (CONTEXT.md)   warm-start on boot
```

Memory Crystal owns Layers 1–3. Dream Weaver reads Layer 1 to produce Layer 4. Layer 5 is the agent's working file.

## Three File Types — The Archive

Memory Crystal must produce and manage all three:

| # | File Type | Purpose | Status |
|---|-----------|---------|--------|
| 1 | **JSONL** (copy) | Immutable raw transcript archive. Dream Weaver's primary input. | **NOT DONE** — cc-hook reads in place, doesn't copy |
| 2 | **MD** (per session) | Human-readable conversation summary. Browsable without tools. | **NOT DONE** — OpenClaw does this, Memory Crystal doesn't |
| 3 | **Vector DB** (crystal.db) | Searchable embeddings + FTS5 + RRF hybrid search. | **DONE** |

Target layout in `~/.ldm/`:

```
~/.ldm/
├── memory/
│   └── crystal.db                    ← SHARED vector DB (Layer 2) — all agents write here
│
├── agents/
│   ├── cc-mini/                      ← Claude Code on Mac Mini
│   │   ├── memory/
│   │   │   ├── transcripts/          ← cc-mini's JSONL copies (Layer 1)
│   │   │   ├── sessions/            ← cc-mini's MD summaries
│   │   │   ├── daily/               ← cc-mini's breadcrumb logs (Layer 3)
│   │   │   └── journals/            ← Dream Weaver output (Layer 4)
│   │   ├── SOUL.md, IDENTITY.md     ← identity files
│   │   └── CONTEXT.md               ← warm-start (Layer 5)
│   │
│   ├── lesa-mini/                    ← Lēsa (OpenClaw) on Mac Mini
│   │   └── memory/
│   │       ├── transcripts/          ← Lēsa's JSONL copies (from OpenClaw)
│   │       ├── sessions/            ← Lēsa's MD summaries (from OpenClaw)
│   │       ├── daily/               ← Lēsa's breadcrumb logs
│   │       └── journals/
│   │
│   └── cc-air/                       ← Claude Code on MacBook Air
│       └── memory/
│           ├── transcripts/          ← cc-air's JSONL copies (local sessions)
│           ├── sessions/            ← cc-air's MD summaries (local sessions)
│           └── daily/               ← cc-air's breadcrumb logs
│
└── config.json
```

**Key:** `crystal.db` is shared at `~/.ldm/memory/` — it does NOT live inside any agent's folder. Every agent writes to it (tagged by agent_id), every agent searches it. On remote devices, a read-only mirror lives at the same path.

## Three Memory Systems Running Today

| # | System | What It Does | Owns |
|---|--------|-------------|------|
| 1 | **OpenClaw builtin** | Lēsa's native memory. Writes MD files on `/new` and pre-compaction flush. Indexes into its own sqlite-vec. Leave it alone — it evolves independently. | `{workspace}/memory/*.md` |
| 2 | **Memory Crystal** | Universal memory. Captures conversation turns into crystal.db. Works with CC, Lēsa, any agent. The independent system. | `~/.ldm/memory/crystal.db` (shared) |
| 3 | **context-embeddings plugin** | Older Lēsa plugin. Captures into `context-embeddings.sqlite`. Being superseded by Memory Crystal. Can be retired once Crystal handles all three file types. | `~/.openclaw/memory/context-embeddings.sqlite` |

**Lēsa currently triple-writes** every conversation (OpenClaw builtin + Memory Crystal + context-embeddings). Once Memory Crystal handles all three file types, context-embeddings can be disabled.

## The Master Crystal (Mac Mini)

`crystal.db` — sqlite-vec + FTS5, running on the Mac Mini. Source of truth.

**Search stack (fully implemented):**
- Vector search via sqlite-vec (cosine similarity)
- Keyword search via FTS5 (BM25 scoring)
- Hybrid fusion via Reciprocal Rank Fusion (k=60, ported from QMD)
- Recency weighting (decay based on age)
- LanceDB still present as dual-write fallback (pre-migration safety net)

**Interfaces (all 4 deployed, Phase 1 complete):**
1. CLI (`crystal search`, `crystal remember`, `crystal status`)
2. MCP server (Claude Code tools: `crystal_search`, `crystal_remember`)
3. OpenClaw plugin (Lēsa's interface)
4. Ephemeral relay (Phase 2 — code built, deployment pending)

**Current stats:** ~5,502+ chunks, hybrid search operational.

## Capture Pipeline

**cc-hook.ts** — Claude Code Stop hook. After every conversation:
1. Reads JSONL transcript (in place — does NOT copy)
2. Extracts messages (turn-boundary chunking: 1 message = 1 chunk)
3. Ingests into crystal.db (local) or encrypts + relays (remote)
4. Writes daily breadcrumb to `~/.ldm/agents/{agent_id}/memory/daily/`
5. Tracks position via watermark (byte offset in JSONL)

**Agents are named by machine:** `cc-mini`, `cc-air`, `lesa-mini`. Set via `CRYSTAL_AGENT_ID` env var.

**What cc-hook needs to add:**
- Copy raw JSONL to `~/.ldm/agents/{agent_id}/memory/transcripts/`
- Generate MD session summary to `~/.ldm/agents/{agent_id}/memory/sessions/`

## Dream Weaver — Layer 4

Dream Weaver is a memory consolidation protocol, not an automated tool. It reads raw JSONL transcripts chronologically and produces narrative prose.

**Input:** JSONL transcripts (Layer 1) + daily logs + prior narrative
**Output:** `full-history.md`, journals, `crystal_remember` calls
**Trigger:** Manual, roughly weekly. Not yet automated.
**Key dependency:** Raw JSONL files must be preserved and accessible.

This is why the JSONL copy to `~/.ldm/` matters — Dream Weaver needs those files, and they currently only exist at `~/.claude/projects/` which has backup/FDA issues.

## LDM OS — The Layer Underneath

LDM OS defines the filesystem structure (`~/.ldm/agents/*/`) where identity, soul, and memory live. It's not a memory system itself — it's the spec for where everything goes.

Memory Crystal is one pillar of LDM OS. The others: Dream Weaver (consolidation), Sovereignty Covenant (identity), Boot Sequence (warm-start).

## QMD — Separate System

QMD is a standalone document search engine (indexes markdown files, local GGUF embeddings). Its search algorithms (RRF, FTS5, BM25) were ported into Memory Crystal but the systems are completely separate. QMD can optionally be OpenClaw's memory backend, but currently isn't (Lēsa uses `builtin`).

## What's Broken

1. **Backup system** — BROKEN. FDA issue prevents reading CC transcripts. ~286MB has no backup except Crystal ingestion. The JSONL copy to `~/.ldm/` would fix this.
2. **No JSONL archive** — Raw transcripts only exist at `~/.claude/projects/`. Not copied, not backed up.
3. **No MD summaries** — Memory Crystal doesn't produce human-readable session files. Only OpenClaw does.
4. **Triple-write waste** — Lēsa embeds every conversation three times via three separate systems.

## QMD Integration — Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1. Storage migration | Replace LanceDB with sqlite-vec | **DONE** |
| 2. Hybrid search | FTS5 + RRF fusion | **DONE** |
| 3. Smart chunking + dedup | Content-hash dedup | **PARTIAL** |
| 4. Re-ranking + query expansion | LLM re-ranking | **NOT STARTED** |
| 5. Local embeddings | Replace OpenAI with local model | **NOT STARTED** |

## The Big Picture

```
┌──────────────────────────────────────────────────────────────┐
│                      Mac Mini (Master)                        │
│                                                                │
│  ~/.ldm/memory/crystal.db    ← SHARED vector DB (all agents) │
│                                                                │
│  ~/.ldm/agents/cc-mini/memory/                                │
│  ├── transcripts/   sessions/   daily/   journals/            │
│                                                                │
│  ~/.ldm/agents/lesa-mini/memory/                              │
│  ├── transcripts/   sessions/   daily/   journals/            │
│                                                                │
│  cc-hook (local) ← cc-mini captures + archives + ingests      │
│  OpenClaw plugin ← lesa-mini conversations                    │
│  poller.ts ← picks up cc-air's drops from relay               │
│  Dream Weaver ← reads transcripts, writes narratives          │
│                                                                │
└──────────────────────┬─────────────────────────────────────────┘
                       │
             ┌─────────▼──────────┐
             │   Cloudflare Worker │
             │   (Ephemeral Relay) │
             │   Blind dead drop   │
             └─────────┬──────────┘
                       │
┌──────────────────────▼─────────────────────────────────────────┐
│                   MacBook Air (Read-Only DB)                    │
│                                                                  │
│  ~/.ldm/memory/crystal.db    ← read-only mirror from Mini      │
│                                                                  │
│  ~/.ldm/agents/cc-air/memory/                                   │
│  ├── transcripts/   sessions/   daily/                          │
│  (cc-air's own local files — written by cc-hook)                │
│                                                                  │
│  cc-hook (relay) → captures locally + encrypts + drops at relay │
│  mirror-sync.ts ← pulls + verifies DB snapshot                  │
│  Local search: keyword + semantic (full offline)                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Agents are per-harness-instance, named by machine:**
- `cc-mini` — Claude Code on Mac Mini
- `lesa-mini` — Lēsa (OpenClaw) on Mac Mini
- `cc-air` — Claude Code on MacBook Air
- Future: `kodaks-air`, etc.

Each harness instance = one "user" in LDM. Not separated by session or spawn — one folder per harness per machine.

All agents share one `crystal.db` at `~/.ldm/memory/`. On remote devices, that DB is a read-only mirror synced via the relay.

**The Mini has EVERYTHING.** Every remote agent's full file tree is reconstructed on the Mini from relay data. If a device is lost, nothing is lost — the Mini has the complete `~/.ldm/agents/cc-air/` directory and can run Dream Weaver against it without ever touching the Air.

**How remote agent files reach the Mini:**
The poller already receives full conversation content after decrypting. It reconstructs the remote agent's files locally:
1. Writes raw JSONL to `~/.ldm/agents/cc-air/memory/transcripts/`
2. Generates MD summary to `~/.ldm/agents/cc-air/memory/sessions/`
3. Appends daily breadcrumb to `~/.ldm/agents/cc-air/memory/daily/`
4. Ingests into shared `crystal.db` (already does this)

No extra relay transfer needed — the Mini rebuilds everything from the same data.
