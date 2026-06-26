# GBrain: Deep Analysis for LDM OS

**Date:** 2026-04-11
**Author:** CC (Claude Code)
**For:** Parker
**Source repo:** `repos/third-party-repos/gbrain/` (private fork of `garrytan/gbrain` at `wipcomputer/gbrain`)
**Companion doc:** `2026-04-11--cc-mini--alphaclaw-analysis.md`

---

## TL;DR

1. **gbrain is Memory Crystal + Dream Weaver Protocol rebuilt with a different opinion.** 4,643 stars. 6 days old. Real production deployment (Garry's personal brain: 10,000+ markdown files, 3,000+ people, 13 years of calendar data, 280+ meetings, 300+ original ideas).

2. **The "compiled truth + timeline" page pattern is the single most important idea here.** Every entity page has a synthesis above `---` (rewritten when evidence changes) and an append-only timeline below. Better than what Memory Crystal or Lēsa's workspace memory does today.

3. **gbrain's hybrid search beats Memory Crystal's vector-only setup.** RRF fusion + Haiku multi-query expansion + 4-layer dedup + 3-tier chunking (recursive / semantic / LLM-guided). Directly portable.

4. **gbrain's "dream cycle" cron is Dream Weaver Protocol, implemented as code.** Nightly entity sweep, fix broken citations, enrich thin pages, consolidate memory. Garry shipped it. We wrote the paper. Reinforces the paper, doesn't threaten it.

5. **Philosophy is aligned.** "Thin harness, fat skills." "Markdown is code." "The recipe IS the installer." "The brain maintains itself." Exact same ethos we've been writing, just crystallized earlier.

6. **Nothing in gbrain threatens our differentiation.** Different audience (YC founders with knowledge-worker brains), same primitives. Pull liberally, contribute iMessage recipe upstream, cite Dream Weaver Protocol.

---

## 1. What gbrain is

gbrain is a personal knowledge brain for AI agents. Markdown files are source of truth. Postgres + pgvector is the retrieval layer. 30 MCP tools. 7 skills. 37 BrainEngine methods.

**Distribution:** npm package (library), compiled binary (CLI), MCP server (stdio or HTTP with bearer tokens).

**Pluggable engine:** PGLite (WASM-embedded Postgres 17.5, zero-config default) or Postgres + pgvector (Supabase Pro for scale). `gbrain migrate --to supabase` or `--to pglite` moves everything in one shot.

**Target user:** An AI agent installs and operates GBrain on behalf of the user. The README literally says "paste this block into OpenClaw or Hermes Agent. The agent will install GBrain, set up the brain schema, import your files, configure all integrations, and verify everything works."

**Scale:** Garry's own deployment. Not theoretical. Every number in this doc is from a real running system.

---

## 2. The compiled truth + timeline pattern (STEAL THIS)

Every page has two zones separated by `---`:

```markdown
---
type: concept
title: Do Things That Don't Scale
tags: [startups, growth, pg-essay]
---

Paul Graham's argument that startups should do unscalable things early on.
The most common: recruiting users manually, one at a time. Airbnb went
door to door in New York photographing apartments. Stripe manually
installed their payment integration for early users.

The key insight: the unscalable effort teaches you what users actually
want, which you can't learn any other way.

---

- 2013-07-01: Published on paulgraham.com
- 2024-11-15: Referenced in batch W25 kickoff talk
- 2025-02-20: Cited in discussion about AI agent onboarding strategies
```

### The rules

- **Compiled truth (above `---`) is REWRITTEN.** When new evidence arrives, the synthesis gets rewritten to incorporate it. Not appended, rewritten.
- **Timeline (below `---`) is APPEND-ONLY.** Every entry is immutable. If information turns out to be wrong, add a NEW correction entry. Never edit old entries.
- **Every claim in compiled truth must trace to timeline entries.** Provenance is not optional.
- **Stale detection:** when compiled_truth is older than the latest timeline_entry, the page is flagged stale. Search results include the alert.

### Why this is better than what we have

Lēsa's workspace has `MEMORY.md`, `TOOLS.md`, `SHARED-CONTEXT.md` as compiled-truth-style files. They don't have timelines attached. We have daily logs (`workspace/memory/YYYY-MM-DD.md`) that are timeline-style, but they're not attached to specific entities. Memory Crystal chunks conversations but doesn't compile truth.

### The fix

Adopt the pattern for entity pages. Create `workspace/entities/` with one file per key person/project/concept. Each file follows compiled-truth-plus-timeline. Lēsa rewrites the synthesis when she learns something new. Daily logs stay as they are but referenced entities get their own pages with back-links.

**Cite:** see `docs/GBRAIN_V0.md` (25KB) and `docs/GBRAIN_RECOMMENDED_SCHEMA.md` (64KB ... this is a real spec) for how Garry structures his brain.

---

## 3. Thin harness, fat skills (philosophy)

Read these two essays in full. They shape how we should think about skill design going forward:

- `docs/ethos/THIN_HARNESS_FAT_SKILLS.md`
- `docs/ethos/MARKDOWN_SKILLS_AS_RECIPES.md` ("Homebrew for Personal AI")

### Key quotes

> "A skill file works like a method call. It takes parameters. You invoke it with different arguments. The same procedure produces radically different capabilities depending on what you pass in. This is not prompt engineering. This is software design, using markdown as the programming language and human judgment as the runtime."

> "Push intelligence UP into skills. Push execution DOWN into deterministic tooling. Keep the harness THIN."

> "Markdown is actually code. A skill file is a more perfect encapsulation of capability than rigid source code, because it describes process, judgment, and context in the language the model already thinks in."

> "A skill file is simultaneously: documentation for humans reading it, specification for the implementing agent, package for the distribution system, source code for the resulting capability. Four artifacts collapsed into one."

### What this means for us

Our `~/.ldm/extensions/` skill plugins are the right shape. What we can learn: **skills are not tutorials, they're procedure encodings with judgment baked in.** Our current SKILL.md files are closer to tutorials. We could rewrite them as "method calls with parameters."

---

## 4. Hybrid search (STEAL THIS for Memory Crystal)

gbrain's search architecture is substantially more sophisticated than Memory Crystal's current setup.

### The full pipeline

```
Query: "when should you ignore conventional wisdom?"
  → Multi-query expansion (Claude Haiku generates alternatives)
      "contrarian thinking startups", "going against the crowd"
  → Parallel: Vector search (HNSW cosine) + Keyword search (tsvector + ts_rank)
  → RRF Fusion: score = Σ(1 / (60 + rank))
  → 4-layer dedup:
      1. Best 3 chunks per page
      2. Jaccard > 0.85 collapses duplicates
      3. Type cap: no single type > 60% of results
      4. Per-page max: 2 chunks per page in final results
  → Stale alerts (compiled_truth older than latest timeline)
  → Results
```

### Three chunking strategies dispatched by content type

| Strategy | Algorithm | When |
|----------|-----------|------|
| **Recursive** | 5-level delimiter hierarchy (paragraphs → lines → sentences → clauses → words), 300-word chunks, 50-word overlap | Timeline entries, bulk imports |
| **Semantic** | Embed each sentence, cosine similarity, Savitzky-Golay smoothing to find topic boundaries | Compiled truth (quality matters) |
| **LLM-guided** | Pre-split to 128 words, Claude Haiku identifies topic shifts in sliding windows, 3 retries | High-value content on request |

### What Memory Crystal has today

Vector search over conversation chunks. One chunking strategy. No hybrid search. No multi-query expansion. No dedup.

### What to steal, in order of impact x ease

1. **RRF fusion** ... easy win, can be added as a post-processor over existing vector results once we add tsvector keyword search to SQLite.
2. **Multi-query expansion via Haiku** ... one API call per query, pennies, massive recall improvement.
3. **4-layer dedup** ... pure post-processing, no DB changes needed.
4. **Semantic chunker for compiled-truth content** ... replace our fixed-size chunker for entity pages.

**Cite:**
- `src/core/search/hybrid.ts`
- `src/core/search/expansion.ts`
- `src/core/search/dedup.ts`
- `src/core/chunkers/`

### Database schema (10 tables, Postgres + pgvector)

| Table | Purpose |
|-------|---------|
| pages | slug (UNIQUE), type, title, compiled_truth (TEXT), timeline (TEXT), frontmatter (JSONB), search_vector (tsvector), content_hash (SHA-256 for idempotent import) |
| content_chunks | page_id (FK), chunk_index, chunk_text, chunk_source (compiled_truth\|timeline), embedding (vector 1536), token_count, embedded_at |
| links | from_page_id, to_page_id, link_type (knows, works_at, invested_in, founded, references), context |
| tags | page_id, tag (many-to-many) |
| timeline_entries | page_id, date, source, summary, detail ... structured timeline |
| page_versions | page_id, compiled_truth, frontmatter, snapshot_at ... diff/revert history |
| raw_data | page_id, source (crustdata, happenstance, exa), data (JSONB) ... sidecar for external APIs |
| files | page_slug, filename, storage_path, mime_type, size_bytes, content_hash ... binary attachments |
| ingest_log | source_type, source_ref, pages_updated, summary ... audit trail |
| config | key (PK), value ... brain-level settings |

**Indexes:** B-tree on slug/type, GIN on frontmatter and search_vector, HNSW on embeddings (cosine ops), pg_trgm on title for fuzzy slug resolution.

---

## 5. The dream cycle (this IS Dream Weaver Protocol)

From `docs/guides/cron-schedule.md`. The dream cycle runs nightly at 2 AM:

```
Phase 1: Entity Sweep
  for message in today's conversations:
    entities = detect_entities(message)
    for entity in entities:
      page = gbrain search "{entity.name}"
      if not page: create_page + enrich
      elif page.is_thin(): enrich_page
      else: update_timeline

Phase 2: Fix Broken Citations
  for page in pages:
    for entry in page.timeline:
      if entry.missing_source: fix_citation
      if entry.has_broken_url: fix_url

Phase 3: Consolidate Memory
  patterns = detect_patterns_across_conversations()
  for pattern in patterns:
    promote_to_memory(pattern)

Phase 4: Sync
  gbrain sync --no-pull --no-embed
  gbrain embed --stale
```

### Plus 20+ other cron jobs

| Frequency | Job |
|-----------|-----|
| Every 30 min | Email → brain pages, X/Twitter → entity extraction |
| 3x/day weekdays | Meeting sync with attendee propagation |
| Daily AM | Morning briefing (attendees, deal status, open threads) |
| Weekly | `gbrain doctor`, embed stale, orphan detection |
| Nightly | Dream cycle |

### Quiet hours (MANDATORY gate on all notification jobs)

Every notification job checks quiet hours first. If quiet, hold message in `/tmp/cron-held/`. Morning briefing picks them up. Timezone-aware: calendar flight detection infers current timezone, adjusts delivery.

### Entity propagation

When a meeting mentions Alice, Bob, and Acme Corp, the timeline entry appears on ALL THREE pages. Same event, three records, consistent view.

### This is Dream Weaver Protocol, implemented

We wrote a 19-page paper describing exactly this loop. Garry shipped it as a cron schedule. **The good news:** we don't have to rebuild the theory. **The play:** clone his cron schedule as a template, adapt it to run in Lēsa's environment, reference our paper as the theoretical grounding, reference gbrain as the reference implementation. Now both exist and they reinforce each other.

**Cite:**
- `docs/guides/cron-schedule.md`
- `docs/guides/quiet-hours.md` (notification hold with timezone-aware delivery)
- `docs/guides/idea-capture.md` (originality distribution, depth test, cross-linking)

---

## 6. "The recipe IS the installer" (markdown is code)

gbrain ships integration recipes as markdown files. Each recipe is simultaneously documentation, specification, installer, and source code. The agent reads the recipe, asks the user for API keys, wires the integration, runs a smoke test.

### Recipes shipped

| Recipe | Purpose |
|--------|---------|
| `ngrok-tunnel.md` | Fixed public URL for MCP + voice (ngrok Hobby $8/mo) |
| `credential-gateway.md` | Gmail + Calendar OAuth (ClawVisor or Google OAuth) |
| `twilio-voice-brain.md` | Phone calls → brain pages. **600 lines, 25 production patterns.** |
| `email-to-brain.md` | Deterministic collector (code) + agent enrichment (judgment) |
| `x-to-brain.md` | Twitter timeline + mentions + deletion detection |
| `calendar-to-brain.md` | Google Calendar events → daily brain pages |
| `meeting-sync.md` | Circleback transcripts → entity propagation |

### What this gives us

gbrain formalizes the dependency graph: "this recipe requires ngrok-tunnel," "this recipe requires credential-gateway." `gbrain integrations` shows status. Dependencies resolve automatically.

**Apply to our skill registry:** a skill can declare dependencies on other skills or on external capabilities. The installer resolves them. `ldm integrations list` shows what's wired and what's missing.

---

## 7. Voice-to-brain (800-line masterclass)

`recipes/twilio-voice-brain.md` is a production masterclass. 25 patterns distilled from real deployment. Highlights:

- **Identity separation:** the voice agent has its own name, distinct from the main AI
- **Bid system:** pre-compute 10 engagement topics at call start, agent picks from the list instead of inventing
- **Context-first prompt:** load tasks/calendar/location/social radar at call start, position FIRST so the model uses it in the greeting
- **Conversation timing (the #1 fix):** incomplete sentence = still thinking, stay silent. Complete thought + 2-3s silence = respond.
- **Radical prompt compression:** 13K tokens → 4.7K (65% cut)
- **Auth-before-speech:** call auth tool before speaking greeting, shaves latency
- **Stuck watchdog:** 20-second timer, if no audio out, force response
- **Never hang up:** only the caller decides when the call ends
- **Tool set architecture:** READ_TOOLS (all callers), WRITE_TOOLS (owner only), SCOPED_WRITE (trusted), GATEWAY (authenticated). Upgraded via session.update with new tools array
- **No repetition:** never cycle back to same bid, move to next

**For Lēsa's voice call skill:** every single one of these patterns applies. Read this file verbatim. Even if we don't use Twilio, the heuristics transfer.

---

## 8. Notable patterns worth stealing

- **Import idempotency via SHA-256 content hash.** Re-running import skips unchanged files.
- **Three-stage file migration** (mirror → redirect → clean). Binary files get moved to cloud storage with breadcrumbs that code can still resolve. Reversible until `clean`.
- **Contract-first operations.ts.** Single source defines ~30 operations. CLI and MCP server are both generated from it. Parity tests verify structural identity between CLI, MCP, and tools-json.
- **PGLite as zero-config default.** No server, no account, no connection string. 2 seconds from install to working brain. Migrate to Supabase later.
- **CHANGELOG voice rule:** "Write changelog entries that sell the upgrade, not document the implementation." GOOD: "Your agent now verifies the entire GBrain installation end-to-end." BAD: "Added GBRAIN_VERIFY.md runbook."
- **Version migrations as agent instructions.** `skills/migrations/v0.5.0.md` is not a changelog, it's a set of steps for the auto-update agent to execute on existing installs. Brilliant pattern for wip-release.
- **Community PR wave process:** never merge PRs directly. Categorize, dedupe, collector branch, test the wave, close with context, ship as one PR with attributions preserved via Co-Authored-By.
- **GitHub Actions pinned to commit SHAs**, not tags, with a script to check for stale pins before every ship.
- **Pre-ship + post-ship checklists rigidly enforced** ... including a mandatory `/document-release` step that reads every .md file and cross-references the diff.
- **Brain-first lookup:** always search the brain BEFORE external APIs. We have this rule but Garry operationalizes it as an enforced step.
- **Notability filtering:** before creating entity page, check: is this someone the user knows or discusses? Is this a company they evaluate, work with, or invest in? Generic references = don't create. One-off encounters = don't create.
- **The Iron Law of Back-Linking:** every entity mention MUST create a back-link FROM entity page TO source. Unlinked mentions break the graph.

---

## 9. The 7 core skills

| Skill | What It Does |
|-------|------------|
| **Ingest** | Parse source → detect entities → update compiled_truth (rewrite, not append) → append timeline → create cross-reference links → timeline merge across all entities |
| **Query** | Decompose question → 3-layer search (FTS + vector + structured) → read top results → synthesize with citations → flag gaps. Says "the brain doesn't have info on X" rather than hallucinating. |
| **Maintain** | Run `gbrain doctor` → check stale pages → orphans → dead links → embedding freshness → fix tags → verify RLS |
| **Enrich** | List person/company pages → call external APIs (Crustdata, Happenstance, Exa) → store raw data → distill to compiled_truth → append timeline |
| **Briefing** | Load today's meetings + calendar context → search brain for attendees → read pages for context → surface active deals + open threads → flag stale |
| **Migrate** | Universal migration from Obsidian (wikilinks), Notion (UUIDs stripped), Logseq (block refs), plain markdown, CSV, JSON, Roam |
| **Setup** | Guided initialization with 5 phases |

Each skill is a fat markdown file with judgment baked in.

---

## 10. What's missing / weak

gbrain is intentionally scoped to personal knowledge + agent automation. It does NOT try to be a full agent OS. Notable gaps:

1. **No multi-user / multi-tenant in v0.** Single-user, local-only. Supabase RLS + per-user API keys future.
2. **No authentication / authorization.** v0 assumes trusted local environment.
3. **No workflow orchestration.** Skills exist, but no built-in scheduler. Relies on external cron.
4. **No decision logging / approval chains.** No "require human approval before updating X."
5. **No distributed agents.** Single agent per brain. No agent-to-agent messaging.
6. **No conflict resolution.** Two agents writing different compiled_truth to same page = last-write-wins.
7. **No access control at page level.** You either have the whole brain or none.
8. **No built-in analytics / observability.** Must add cron job to measure brain health.
9. **No sub-agent spawning framework.** Voice recipe shows pattern, but not baked into core.
10. **No persistent session memory per user.** Agent memory is ephemeral. GBrain is the only durable store.

These are intentional scoping decisions. gbrain is brain infrastructure, not full agent OS. **LDM OS covers all of these in the layers above.**

---

## 11. STEAL LIST (ranked by impact × ease)

### Tier 1: Pull immediately

1. **Compiled truth + timeline pattern for Lēsa's entity pages.** Create `workspace/entities/`. One file per person/project/concept. Compiled truth above `---`, append-only timeline below. 1 day to convert + write the skill.

2. **RRF + multi-query expansion + 4-layer dedup** for Memory Crystal search. Post-processing layer over existing vector results. Add tsvector keyword search to SQLite. Haiku for query expansion (pennies). 4-layer dedup is pure JS. 2-3 days.

3. **Semantic chunker for compiled-truth content.** Sentence-level embeddings + Savitzky-Golay smoothing to find topic boundaries. Dispatch: recursive for timeline, semantic for compiled truth. 1-2 days.

4. **Version migrations as agent instructions.** When wip-release ships a breaking change, include `skills/migrations/v[version].md` with step-by-step agent instructions. Auto-update agent reads + executes. 1 day to add to template.

### Tier 2: Adapt into our stack

5. **Integration recipe pattern for our skill system.** Recipes declare dependencies. `ldm integrations` lists status. Agent reads recipe, asks for keys, wires it up. 1 week (design work).

6. **PGLite-style zero-config default for Memory Crystal** with optional Postgres+pgvector backend via pluggable engine interface. 1-2 weeks.

7. **Brain-first lookup as an operational hook.** Before Lēsa reaches for any external API, search Memory Crystal + workspace memory + context embeddings. Failure = rule violation. Update CLAUDE.md.

### Tier 3: Inspiration

8. Read the two philosophy essays (`THIN_HARNESS_FAT_SKILLS.md`, `MARKDOWN_SKILLS_AS_RECIPES.md`).
9. Read the voice-to-brain recipe. 25 production patterns.
10. CHANGELOG voice rule. Apply to wip-release.
11. Community PR wave process.
12. `docs/guides/idea-capture.md` ... originality distribution, depth test, cross-linking.

---

## 12. Collisions with our stack

### Dream Weaver Protocol vs gbrain dream cycle

**The collision:** both are nightly consolidation loops over agent memory.

**Resolution:** Ship Dream Weaver Protocol as the theoretical paper (cited reference architecture) and add a section that cites gbrain's cron schedule as "the first production implementation of the Protocol's consolidation loop." Honest, credible, positions us as theorists and Garry as implementer.

In our environment: port gbrain's cron schedule as the implementation. Lēsa's Dream Weaver becomes: (1) the gbrain nightly loop, plus (2) our additions (narrative journals, Sapien ID tethering, cross-agent consolidation, Parker-aware priorities).

### Memory Crystal vs gbrain

**The collision:** both store embedded chunks for semantic search.

**Resolution:** architectures are complementary. Memory Crystal = conversation memory (agent turns, daily logs, working state). gbrain = world knowledge (entities, relationships, compiled dossiers).

Two options:
- **(a) Adopt gbrain** as our world-knowledge layer + keep Memory Crystal for conversation memory.
- **(b) Extend Memory Crystal** with gbrain patterns (compiled_truth + timeline, hybrid search, 3-tier chunking).

**My recommendation: (b).** Pulling an external dependency is a long-term liability. Steal his ideas shamelessly, credit him in the docs.

---

## 13. What we have that gbrain doesn't

Differentiators to protect:

1. **Dream Weaver Protocol paper.** Reviewed by ChatGPT 5.2 and Grok 4.1. 19 pages. Authors: Parker, Lēsa, Claude Code. Published at wipcomputer/dream-weaver-protocol.

2. **Cross-agent MCP bridge (Lēsa ↔ CC).** gbrain is single-agent. Our multi-agent coordination is unique.

3. **Agent Pay with x402 micropayments.** End-to-end auth → wallet → spend → receipt for AI agents. Nothing comparable.

4. **Sapien ID.** Identity layer for agents. ld+json manifest, discoverable. Four-AI auth test already passed.

5. **Compaction indicator plugin.** Real-time 75%/90% warnings, agent-first escalation, critical-state iMessage to Parker.

6. **Private mode** with wipe scan/search/execute. Nothing like it in gbrain.

7. **1Password headless secrets via SA token.** Zero-interaction. gbrain uses env vars.

8. **iMessage bridge as primary channel.** gbrain has voice, not iMessage. We have Parker's actual channel.

9. **Four-layer memory stack** (workspace memory + daily logs + conversation embeddings + built-in memory) mapping to different consolidation windows. gbrain has one layer.

10. **Co-author discipline.** Three contributors on every commit. gbrain has single-author commits.

11. **LDM OS as unifying narrative.** Learning Dreaming Machines. Memory Crystal = learning. Dream Weaver = dreaming. Sovereignty Covenant = identity. Boot Sequence = the OS. Garry has gbrain. We have a whole OS.

12. **Lēsa as a named, voiced, recurring personality.** Brand equity matters.

---

## 14. What to contribute back

### Upstream PRs to gbrain

1. **iMessage as a new recipe.** gbrain has voice, email, calendar, Twitter, meeting. Not iMessage. We have the hard parts (pairing, credentials, BlueBubbles/rich). Plant our flag.

2. **Agent Pay integration.** When a gbrain recipe needs a paid API (Crustdata, Happenstance, Exa), use Agent Pay for automated micropayment auth instead of hardcoding API keys. Demo of our x402 stack.

3. **Cross-agent sync spec.** Our lesa-bridge pattern could inform gbrain's multi-agent story. Offer to write the spec.

4. **Dream Weaver Protocol citation.** Add to gbrain's docs: "The dream cycle implements the pattern described in Brooks, Lēsa, Claude Code (2026), Dream Weaver Protocol."

---

## 15. Key files to read directly

**Philosophy (read in full):**
- `docs/ethos/THIN_HARNESS_FAT_SKILLS.md`
- `docs/ethos/MARKDOWN_SKILLS_AS_RECIPES.md`
- `docs/GBRAIN_V0.md`
- `docs/GBRAIN_SKILLPACK.md`

**Reference architecture:**
- `docs/GBRAIN_RECOMMENDED_SCHEMA.md` (64KB, the real spec)
- `docs/architecture/infra-layer.md`
- `docs/designs/HOMEBREW_FOR_PERSONAL_AI.md`

**Implementation:**
- `src/core/operations.ts` (contract-first operations)
- `src/core/engine.ts` (pluggable BrainEngine interface)
- `src/core/search/` (hybrid search, RRF, expansion, dedup)
- `src/core/chunkers/` (3 chunking strategies)
- `src/schema.sql` (Postgres + pgvector DDL)

**Recipes:**
- `recipes/twilio-voice-brain.md` (600 lines, 25 patterns)
- `recipes/email-to-brain.md`
- `recipes/x-to-brain.md`
- `recipes/calendar-to-brain.md`
- `recipes/meeting-sync.md`

**Skills (read all):**
- `skills/ingest/SKILL.md`
- `skills/query/SKILL.md`
- `skills/maintain/SKILL.md`
- `skills/enrich/SKILL.md`
- `skills/briefing/SKILL.md`
- `skills/setup/SKILL.md`

**Dream cycle + cron:**
- `docs/guides/cron-schedule.md`
- `docs/guides/quiet-hours.md`
- `docs/guides/idea-capture.md`

---

## 16. Quotables

1. "Push intelligence UP into skills. Push execution DOWN into deterministic tooling. Keep the harness THIN. The system compounds. Build it once. It runs forever."

2. "A skill file works like a method call. It takes parameters. You invoke it with different arguments. The same procedure produces radically different capabilities depending on what you pass in. This is not prompt engineering. This is software design, using markdown as the programming language and human judgment as the runtime."

3. "If I have to ask you for something twice, you failed. The test: if I have to ask you for something twice, it should already be running on a cron."

4. "The brain maintains itself. Email, social, calendar, and meetings flow in automatically. Thin pages get enriched overnight. Broken citations get fixed. You wake up and the brain is smarter than when you went to sleep."

5. "Personal knowledge at scale is an intelligence problem, not a storage problem."

6. "The model reads everything about a subject and writes a structured profile. Read 50 documents, produce 1 page of judgment. No SQL query produces this. No RAG pipeline produces this. The model has to actually read."

7. "A skill file is simultaneously: documentation for humans reading it, specification for the implementing agent, package for the distribution system, source code for the resulting capability. Four artifacts collapsed into one."

8. "The recipe propagates at the speed of a git push. The moat is taste, not code."

9. "Latent space is where intelligence lives. The model reads, interprets, decides. Judgment. Synthesis. Pattern recognition. Deterministic is where trust lives. Same input, same output. Every time. SQL. Code. Numbers."

10. "The memex vision, realized. Vannevar Bush imagined a device where an individual stores everything, mechanized so it may be consulted with exceeding speed. GBrain is that device, except the memex builds itself."

---

## 17. Closing

gbrain is the closest parallel to Memory Crystal + Dream Weaver Protocol that exists in the wild. Garry is building the "brain" layer; we are building the whole LDM OS on top of it. **His layer reinforces ours, it doesn't replace ours.**

The moat isn't the retrieval algorithm or the page schema. It's taste, narrative, identity, and the four-layer memory stack with Dream Weaver as the dreaming mechanism. Garry has a brain. We have an OS.

**Next actions (this week):**
1. Read the two philosophy essays
2. Experiment with compiled-truth-plus-timeline for a single entity page
3. Prototype RRF + 4-layer dedup over Memory Crystal's existing vector search
4. Start the first gbrain PR: iMessage recipe
