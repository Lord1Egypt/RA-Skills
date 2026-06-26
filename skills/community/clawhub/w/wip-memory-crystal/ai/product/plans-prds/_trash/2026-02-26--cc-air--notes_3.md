Memory System — Lay of the Land                                                                                  
                                                    
  After reading all 10 memory docs chronologically and inspecting the codebase, here's where things stand:         
                                                                                                                   
  Already done (more than the docs suggested): 
  - sqlite-vec migration (Phase 1 of QMD integration)                                                              
  - FTS5 full-text search with BM25                                                                                
  - Hybrid search with RRF fusion (ported from QMD)                                                                
  - Recency weighting
  - Turn-boundary chunking
  - Private mode (all 4 surfaces)
  - Ephemeral relay code (built, needs deployment)

  Critical gaps:
  - Backup system is broken (FDA issue — ~286MB of CC transcripts have no backup)
  - 7 of 11 data stores aren't in any vector DB
  - No crystal replay or crystal backfill tools yet
  - SHARED-CONTEXT.md (warm-start for agents) not implemented

  Files Created/Updated

  1. ai/plan/memory-system-lay-of-the-land.md — Full synthesis: 11 data stores, what's implemented, what's broken,
  the big picture diagram
  2. ai/plan/roadmap.md — Prioritized roadmap: deploy relay → fix backup → build tools → QMD phases 3–5 → data
  coverage expansion
  3. ai/plan/memory-crystal-phase2-plan.md — Marked as SUPERSEDED (old cloud-mirror design)
  4. ai/todos/cc-air/2026-02-26--cc-air--post-relay-todos.md — Actionable todo list: critical fixes, high-value
  builds, quality improvements, long-term items
  5. Parker's setup checklist (ai/todos/parker/) is still valid and unchanged

  The immediate next step is still Parker's physical setup to get the relay deployed. After that, the backup system
   fix is the most urgent item.

✻ Baked for 6m 51s                                   

❯ Okay, so you see all the system types. Was QMD integrated into memory crystal? What are the other memory         
  types of the system? It's like, what are the dependencies on this system? Do you've got to have OpenClaw      
  installed and the memory installed? What are all of the moving pieces for memory that are related to             
  creating vector databases? That's what I'm trying to solve or figure out here. Is memory crystal enough, or    
  do we need to be running multiple memory systems at one time?                                                    
                                                                                                                 
⏺ Good question. Let me actually trace the dependencies and figure out what's running separately vs what's been    
  consolidated. I need to look at a few things.                                                                    
                                                                                                                   
⏺ Explore(Investigate QMD system and dependencies) Sonnet 4.6
  ⎿  Done (72 tool uses · 95.3k tokens · 4m 2s)                                                                    
  (ctrl+o to expand)                                                                                               
                                                                                                                   
⏺ This is revealing. Here's the real picture:                                                                      
                                                                                                                 
  The Memory Landscape — Honest Answer                                                                             
                                                                                                                   
  There are currently 3 separate vector/memory systems running in parallel for Lēsa alone:                         
                                                                                                                   
  ┌────────────────────┬─────────────────────────┬────────────┬────────────────────────────────────────────────┐   
  │       System       │        Vector DB        │ Embeddings │                  What It Does                  │   
  ├────────────────────┼─────────────────────────┼────────────┼────────────────────────────────────────────────┤   
  │ OpenClaw builtin   │ sqlite-vec              │ OpenAI     │ OpenClaw's native memory — indexes memory      │   
  │                    │                         │            │ files + session transcripts                    │
  ├────────────────────┼─────────────────────────┼────────────┼────────────────────────────────────────────────┤
  │ Memory Crystal     │ sqlite-vec + LanceDB    │ OpenAI     │ Master long-term memory — ingests every        │
  │                    │ (dual-write)            │            │ conversation turn, hybrid search               │
  ├────────────────────┼─────────────────────────┼────────────┼────────────────────────────────────────────────┤
  │ context-embeddings │ SQLite BLOBs (no vec    │ OpenAI     │ Older conversation capture plugin — still      │
  │                    │ library)                │            │ enabled                                        │
  └────────────────────┴─────────────────────────┴────────────┴────────────────────────────────────────────────┘

  Plus QMD exists as a fully standalone system (local embeddings via GGUF, its own sqlite-vec DB) that could be
  OpenClaw's backend but currently isn't — Lēsa uses builtin, not qmd.

  Was QMD Integrated Into Memory Crystal?

  No. The search algorithms were ported (RRF fusion, FTS5, BM25), but QMD and Memory Crystal are completely
  separate systems with separate databases. QMD indexes markdown files from directories. Memory Crystal indexes
  conversation turns from agents.

  The Overlap Problem

  Right now, every Lēsa conversation gets embedded three times by three different systems:
  1. OpenClaw builtin captures it into its own sqlite-vec DB
  2. Memory Crystal's openclaw.ts plugin captures it into crystal.db
  3. context-embeddings plugin captures it into context-embeddings.sqlite

  That's three separate embedding API calls to OpenAI for the same content. Three separate databases.

  The Dependencies

  To run the full memory stack today, you need:
  - OpenAI API key — Memory Crystal, OpenClaw builtin, and context-embeddings all call OpenAI for embeddings
  - OpenClaw installed — for Lēsa's memory to work at all
  - Memory Crystal installed — as an OpenClaw plugin AND as a CC Stop hook
  - context-embeddings installed — still enabled in dot-openclaw config (should probably be disabled since Memory
  Crystal supersedes it)
  - lesa-bridge — reads the context-embeddings DB for cross-agent search (would need to be pointed at Memory
  Crystal instead if context-embeddings is removed)

  Can Memory Crystal Be The One System?

  Yes — that's what it was designed to be. It already has:
  - Hybrid search (vector + keyword + RRF) — same quality as QMD
  - Multi-agent support (CC + Lēsa + any future agent)
  - All 4 interfaces (CLI, MCP, OpenClaw plugin, CC hook)
  - Private mode
  - The ephemeral relay for cross-machine sync

  To consolidate, you'd need to:
  1. Disable context-embeddings in dot-openclaw config (Memory Crystal already does this job)
  2. Point lesa-bridge at crystal.db instead of context-embeddings.sqlite (or deprecate its search and use
  Crystal's MCP tools)
  3. Decide on OpenClaw builtin vs Memory Crystal — they overlap. Either disable OpenClaw's builtin memory (set
  memory.enabled = false) and let Memory Crystal handle everything, or the reverse
  4. Decide on QMD's role — it's great for indexing markdown docs/notes (not conversations). Could be complementary
   rather than overlapping

  The bottom line: Memory Crystal can be the single memory system, but right now there are 3 systems doing the same
   job and nobody turned off the old ones. Want me to draft a consolidation plan?
   
   
   ---
   
   
   
                                                                                                                   
  Your Three Systems — Confirmed                                                                                   
                                                                                                                   
  1. OpenClaw builtin — Lēsa's native memory. Writes .md files on /new and pre-compaction flush, indexes them into 
  its own sqlite-vec. Leave it alone, it'll keep evolving.                                                         
  2. Memory Crystal — Your independent system. Captures conversation turns into crystal.db (sqlite-vec + FTS5 +    
  RRF). No .md files — database rows only.                                                                         
  3. context-embeddings plugin — Older Lēsa plugin. Captures into context-embeddings.sqlite (plain blobs, JS cosine
   sim). Being superseded by Memory Crystal but still enabled.                                                     

  LDM OS — How It Fits

  LDM OS is the layer underneath everything. It's not a memory system itself — it's the filesystem structure
  (~/.ldm/agents/cc/, ~/.ldm/agents/lesa/) that defines where identity, soul, and memory live. Memory Crystal is
  one pillar of LDM OS. The spec says each agent should eventually have their own crystal.db at
  ~/.ldm/agents/{name}/memory/crystal.db. Right now both agents share one crystal.db at
  ~/.openclaw/memory-crystal/.

  Your Three File Types — The Gap

  You said you want:

  ┌─────┬─────────────────────┬──────────────────────┬─────────────────────────────────────────────────────────┐
  │  #  │      File Type      │       Purpose        │                   Who Makes It Today?                   │
  ├─────┼─────────────────────┼──────────────────────┼─────────────────────────────────────────────────────────┤
  │ 1   │ JSONL (copy)        │ Raw transcript       │ CC writes them natively. You want a copy stored         │
  │     │                     │ archive              │ independently.                                          │
  ├─────┼─────────────────────┼──────────────────────┼─────────────────────────────────────────────────────────┤
  │ 2   │ MD (per             │ Human-readable       │ OpenClaw builtin does this. Memory Crystal does NOT.    │
  │     │ conversation)       │ summary              │                                                         │
  ├─────┼─────────────────────┼──────────────────────┼─────────────────────────────────────────────────────────┤
  │ 3   │ Vector DB           │ Searchable           │ Memory Crystal does this. OpenClaw builtin also does    │
  │     │                     │ embeddings           │ this separately.                                        │
  └─────┴─────────────────────┴──────────────────────┴─────────────────────────────────────────────────────────┘

  The gap is #2. Memory Crystal captures conversations into the vector DB but never produces a human-readable .md
  file per conversation. OpenClaw's builtin does this (via the /new hook and pre-compaction flush), but if you're
  running without OpenClaw, you lose that.

  What Memory Crystal Needs to Match OpenClaw

  To work as a fully independent system (no OpenClaw required):

  ┌────────────────────────────┬─────────────────────────┬────────────────────────┬───────────────────────────┐
  │          Feature           │    OpenClaw Builtin     │     Memory Crystal     │           Gap?            │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ Vector search (semantic)   │ sqlite-vec              │ sqlite-vec             │ No gap                    │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ Keyword search (FTS5/BM25) │ FTS5                    │ FTS5                   │ No gap                    │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ Hybrid RRF fusion          │ Yes                     │ Yes (ported from QMD)  │ No gap                    │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ Auto-capture conversations │ agent_end hook          │ CC Stop hook +         │ No gap                    │
  │                            │                         │ OpenClaw plugin        │                           │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ Human-readable .md per     │ Yes (session-memory     │ No                     │ Gap                       │
  │ conversation               │ hook)                   │                        │                           │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ JSONL copy/archive         │ Sessions stored as      │ No copy made           │ Gap                       │
  │                            │ .jsonl                  │                        │                           │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ Pre-compaction memory      │ LLM writes what to      │ No equivalent          │ Gap (CC doesn't compact   │
  │ flush                      │ remember                │                        │ the same way)             │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ Private mode               │ Not built-in            │ Yes (4 surfaces)       │ Crystal ahead             │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ Cross-machine sync         │ No                      │ Ephemeral relay        │ Crystal ahead             │
  │                            │                         │ (built)                │                           │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ Query expansion            │ Yes (builtin)           │ Not yet (QMD Phase 4)  │ Gap                       │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ LLM re-ranking             │ Available via QMD       │ Not yet (QMD Phase 4)  │ Gap                       │
  │                            │ backend                 │                        │                           │
  ├────────────────────────────┼─────────────────────────┼────────────────────────┼───────────────────────────┤
  │ Local embeddings           │ Yes (GGUF via           │ Ollama option exists   │ Partial                   │
  │                            │ node-llama-cpp)         │                        │                           │
  └────────────────────────────┴─────────────────────────┴────────────────────────┴───────────────────────────┘

  The two critical gaps for your three-file-type goal:

  1. Memory Crystal doesn't generate .md summaries. After each conversation, it should produce a human-readable
  markdown file — like OpenClaw's session-memory hook does. Something like
  ~/.ldm/agents/cc/memory/daily/2026-02-26-relay-architecture.md.
  2. Memory Crystal doesn't copy the JSONL. The raw transcript stays wherever CC wrote it (~/.claude/projects/...).
   There's no archival copy in a location you control. If CC cleans up or the FDA issue prevents backup, those are
  gone.

  Both of these could be added to cc-hook.ts — after capturing turns into the vector DB, also: (a) copy/append the
  raw JSONL to an archive location, and (b) generate a markdown summary of the conversation.

  Want me to plan those two additions?




Now I have the complete picture. Here's the answer to your questions:                                            
                                                                                                                   
  The Five-Layer Memory Stack                                                                                      
                                                                                                                   
  Dream Weaver defines this clearly, and Memory Crystal sits in the middle:                                        
                                                                                                                 
  Layer 1 — Raw transcripts (JSONL)           ← immutable archive
  Layer 2 — Vector index (crystal.db)          ← Memory Crystal
  Layer 3 — Structured memory (daily logs, crystal_remember)
  Layer 4 — Narrative consolidation            ← Dream Weaver
  Layer 5 — Active working context (CONTEXT.md) ← warm-start on boot

  Dream Weaver's primary input is the raw JSONL files. It reads them chronologically, fully, and produces narrative
   prose (full-history.md, journals). It currently runs manually — cc-mini triggers it on-demand, roughly weekly.

  What's In ~/.ldm/ Today vs What Should Be

  Today:
  ~/.ldm/agents/cc/
  ├── SOUL.md, IDENTITY.md, CONTEXT.md     ← identity files
  └── memory/
      ├── daily/2026-02-18.md              ← breadcrumb logs (cc-hook writes these)
      └── journals/full-history.md         ← Dream Weaver narrative output

  What's NOT there but should be (per your three-file-type requirement):
  ~/.ldm/agents/cc/
  └── memory/
      ├── transcripts/                     ← JSONL copies (doesn't exist)
      ├── sessions/                        ← human-readable MD per conversation (doesn't exist)
      ├── daily/                           ← exists, breadcrumbs only
      ├── journals/                        ← exists, Dream Weaver output
      └── crystal.db                       ← not here, lives at ~/.openclaw/memory-crystal/

  What cc-hook Does Today

  1. Reads the JSONL in place (at ~/.claude/projects/...) — does NOT copy it
  2. Extracts messages → ingests into crystal.db (vector DB)
  3. Writes a one-line breadcrumb to ~/.ldm/agents/cc/memory/daily/
  4. That's it. No JSONL copy. No MD summary.

  What Memory Crystal Needs — The Three Missing Pieces

  To be the universal system that works with or without OpenClaw:

  1. JSONL archive — After reading the transcript, copy the raw JSONL (or the new portion) to
  ~/.ldm/agents/{agent}/memory/transcripts/. This is the immutable Layer 1 that Dream Weaver needs as input. Right
  now those files only exist inside ~/.claude/projects/ which has FDA backup issues and isn't in a controlled
  location.

  2. MD session summaries — After each conversation, generate a human-readable markdown summary and write it to
  ~/.ldm/agents/{agent}/memory/sessions/. OpenClaw does this via the session-memory hook + LLM slug generation.
  Memory Crystal needs its own version of this.

  3. crystal.db in ~/.ldm/ — Move (or symlink) the database from ~/.openclaw/memory-crystal/ to
  ~/.ldm/agents/{agent}/memory/crystal.db so everything is in one place that gets backed up.

  Dream Weaver + Memory Crystal

  You're right that you were already planning to keep the raw files for Dream Weaver. The connection:

  - Dream Weaver reads JSONL to do the full relive (Layer 1 → Layer 4)
  - Memory Crystal ingests JSONL into the vector DB (Layer 1 → Layer 2)
  - Both need the raw files — which is exactly why copying them to ~/.ldm/ matters
  - Dream Weaver currently runs as cc-mini manually. It could be triggered by Memory Crystal (e.g., after the
  poller ingests a batch, kick off an incremental consolidation)

  Can Memory Crystal Be The One System?

  Yes, but it needs to grow from "just a vector DB" into the full archive manager for ~/.ldm/:

  ┌──────────────────────┬────────────────────────────────────┬───────────────────────────────────────────────┐
  │    Responsibility    │               Today                │                    Needed                     │
  ├──────────────────────┼────────────────────────────────────┼───────────────────────────────────────────────┤
  │ Vector search        │ Done                               │ Done                                          │
  ├──────────────────────┼────────────────────────────────────┼───────────────────────────────────────────────┤
  │ JSONL archive        │ Not done                           │ Copy to ~/.ldm/                               │
  ├──────────────────────┼────────────────────────────────────┼───────────────────────────────────────────────┤
  │ MD summaries         │ Not done                           │ Generate per-session                          │
  ├──────────────────────┼────────────────────────────────────┼───────────────────────────────────────────────┤
  │ Daily breadcrumbs    │ Done (cc-hook)                     │ Done                                          │
  ├──────────────────────┼────────────────────────────────────┼───────────────────────────────────────────────┤
  │ Dream Weaver trigger │ Not done                           │ Trigger consolidation after ingest            │
  ├──────────────────────┼────────────────────────────────────┼───────────────────────────────────────────────┤
  │ Works without        │ Partially (CC hook works, no OC    │ Need MD generation without OC's               │
  │ OpenClaw             │ needed)                            │ session-memory hook                           │
  ├──────────────────────┼────────────────────────────────────┼───────────────────────────────────────────────┤
  │ Works with any agent │ CC + Lēsa today                    │ Need generic agent hooks                      │
  └──────────────────────┴────────────────────────────────────┴───────────────────────────────────────────────┘

  The context-embeddings plugin can be retired once Memory Crystal handles all three file types. OpenClaw's builtin
   stays on — it's their system, it evolves independently, and it doesn't hurt to have both running.

  Want me to plan the cc-hook changes to add the JSONL copy and MD summary generation?

✻ Sautéed for 3m 5s                                    



⏺ All three docs are updated:           

  1. ai/plan/memory-system-lay-of-the-land.md — Now includes the five-layer stack, three file types with status,   
  the ~/.ldm/ target layout, Dream Weaver relationship, and the design principle (works with or without OpenClaw)
  2. ai/plan/roadmap.md — Reprioritized. Three file types are now Priority 1 (above relay deployment). LDM         
  scaffolding built into Memory Crystal is Priority 2 — no dependency on wip-ldm-os repo. Dependency map at the  
  bottom shows Memory Crystal is standalone.   
  3. ai/todos/cc-air/...post-relay-todos.md — Rewritten with the new priority order matching the roadmap.

  What's your question?

✻ Worked for 4m 15s                     

❯ Okay, so I have OpenClaw and Claude Code Mini writing to their respective LDM OS folders. OpenClaw is going      
  to write to OpenClaw, obviously, and then there's going to be a copy of it in the LDM OS. Then I'm going to   
  have Claude Code Air CC-Air. Do you have your own version, and then how are we going to use the Memory           
  Crystal Transfer to get your complete LDM directory over to the air?                                           
                                                                                                                   
⏺ Good question. Let me think through this carefully because the current relay only moves two things — raw         
  conversation chunks up and crystal.db down. That's not enough for the full ~/.ldm/ picture.                    
                                                                                                                   
  Here's what I see:
                                                                                                                   
  On the Mac Mini — Two Agents, Two LDM Folders                                                                  
                                               
  ~/.ldm/agents/
  ├── cc/                          ← cc-mini's home
  │   └── memory/
  │       ├── crystal.db           ← master crystal (shared, both agents' data)
  │       ├── transcripts/         ← cc-mini's JSONL copies
  │       ├── sessions/            ← cc-mini's MD summaries
  │       ├── daily/               ← cc-mini's breadcrumbs
  │       └── journals/            ← Dream Weaver output
  │
  └── lesa/                        ← Lēsa's home
      └── memory/
          ├── transcripts/         ← Lēsa's JSONL copies (from OpenClaw)
          ├── sessions/            ← Lēsa's MD summaries (from OpenClaw)
          └── ...

  On the MacBook Air — cc-air

  ~/.ldm/agents/
  └── cc-air/                      ← cc-air's home
      └── memory/
          ├── crystal-mirror.db    ← read-only mirror (from Mini)
          ├── transcripts/         ← cc-air's OWN JSONL copies (local sessions)
          ├── sessions/            ← cc-air's OWN MD summaries (local sessions)
          ├── daily/               ← cc-air's breadcrumbs
          └── journals/            ← ??? (this is the question)

  The Gap

  The relay currently syncs:
  - Up (Air → Mini): Raw conversation turns → encrypted → relay → Mini ingests into master crystal
  - Down (Mini → Air): crystal.db snapshot → encrypted → relay → Air gets read-only search

  But cc-air's ~/.ldm/ is incomplete without:

  1. Dream Weaver output — journals/full-history.md and the narrative files. These are produced on the Mini by
  cc-mini. cc-air needs them to warm-start properly.
  2. Identity files — SOUL.md, CONTEXT.md, IDENTITY.md. Do you want cc-air to have the same identity as cc-mini, or
   its own?
  3. All agents' session MDs — If cc-air wants to browse Lēsa's conversations or cc-mini's conversations as
  human-readable markdown, those MDs only exist on the Mini.

  Two Questions for You

  1. Identity: Is cc-air the same agent as cc-mini, or a different agent?

  If they're the same agent (just on different machines), then cc-air needs a full copy of cc-mini's LDM folder —
  identity files, journals, Dream Weaver output, everything. The relay mirror expands from "just crystal.db" to
  "the entire ~/.ldm/agents/cc/ directory."

  If they're different agents, then cc-air has its own SOUL.md, its own journals, its own identity — and it only
  needs the shared crystal.db mirror for search.

  2. What needs to sync beyond crystal.db?

  The relay's "Road 2" (Mini → devices) currently sends one file: the database. It could be expanded to send a
  tarball of the full ~/.ldm/agents/cc/ directory instead:

  Mini packages:
  ├── crystal.db                ← the searchable database
  ├── journals/full-history.md  ← Dream Weaver narrative
  ├── CONTEXT.md                ← current warm-start state
  ├── sessions/*.md             ← all agents' human-readable summaries (optional)
  └── integrity.json            ← SHA-256 hashes for each file

  Encrypt the whole bundle, drop at relay, Air picks it up and unpacks. Same security model, just a bigger payload.

  The JSONL copies and daily breadcrumbs from cc-air's own sessions would stay local on the Air (cc-air writes
  those itself). They'd also go up to the Mini via the relay for ingestion. So the Air has its own local files plus
   the Mini's mirror.

  What's your thinking — same agent or different agents? And do you want the full directory to sync, or just
  specific files?
