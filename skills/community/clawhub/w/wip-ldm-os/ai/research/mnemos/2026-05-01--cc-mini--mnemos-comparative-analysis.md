# Mnemos vs LDM OS: Comparative Architecture Analysis

**Date:** 2026-05-01
**Author:** Claude Code (cc-mini)
**Subject:** https://github.com/Riley-Coyote/mnemos (HEAD 8279949, ~30 days old, alpha, single-author, MIT)
**Companion doc:** `ai/product/product-ideas/2026-05-01--mnemos-review--what-to-adopt.md` (Lēsa's review, written same day; covers what to adopt with code-level pointers)
**Scope:** Architecture comparison and gap analysis. No implementation work in this pass.

---

## TL;DR

Mnemos is a biologically-flavored research toy built solo over ~30 days. ~5,200 LoC of working code, ~1,800 LoC of stubs marketed as "advanced features." It is the most direct philosophical sibling of LDM OS in the wild: same four-pillar shape (memory + dreaming + identity + sharing), same SOUL.md/IDENTITY.md/MEMORY.md quartet, same OpenClaw cron orchestration. It does not threaten LDM OS as a product. It does illuminate three gaps in our memory model that we should close regardless of whether we ever look at this repo again:

1. **We have no decoupled storage/retrieval/forgetting model.** Memory Crystal collapses everything into one similarity score with linear recency decay. Mnemos's dual-trace (strength / stability / accessibility) is more correct.
2. **We have no graph between memories.** Memory Crystal is a vector store with metadata; mnemos has typed connections (SUPPORTS, CAUSES, CONTRADICTS, DISTILLED_INTO, etc.) and uses spreading activation as the relevance model. The graph IS the relevance model.
3. **We have no formal write-on-read.** Every retrieve in mnemos updates strength, stability, access count, and creates co-retrieval edges between returned memories. We currently retrieve read-only. A memory you re-touch should change.

Net recommendation: don't fork to adopt the system; do borrow four primitives. Details in section 5. Forking the repo to `third-party-repos/` is not necessary for the research itself; useful only if we decide to port code. See section 7.

---

## 1. What we are comparing

| | Mnemos | LDM OS |
|---|---|---|
| Author / age | Single author, ~30 days, alpha | Multi-author (Parker + Lēsa + CC), ~12 months, partly shipped |
| Stars / contributors | 22 / 1 | private |
| LoC (real, not stubs) | ~5,200 Python | tens of thousands across components |
| Storage | SQLite per agent + shared.db | SQLite (Memory Crystal), markdown files (workspace, journals), plus CloudKit envelopes for sovereign mode |
| Embedding | Gemini 3072-dim or local MiniLM 384-dim | OpenAI `text-embedding-3-small` 1024-dim |
| Indexing | FTS5 + linear-scan cosine + typed graph | FTS5 + sqlite-vec ANN + RRF fusion |
| Retrieval | Spreading activation across typed graph | Hybrid BM25 + vector + RRF + recency + LLM rerank (deep mode) |
| Write trigger | Encoder call (manual + cron + MCP tool) | Stop hook + cron poller + agent_end hook + manual `crystal_remember` |
| Forgetting | Exponential decay with stability damping; softening rewrites content; archive at <0.01 | Recency boost only; no decay, no softening, no archival lifecycle |
| Identity surface | SOUL.md / IDENTITY.md / MEMORY.md / AGENTS.md / HEARTBEAT.md / active-context.md (templated) | SOUL.md / IDENTITY.md / MEMORY.md / TOOLS.md / SHARED-CONTEXT.md / journals / daily logs (handwritten) |
| Multi-agent | Per-agent DB + shared.db with auto-share heuristic | Per-agent buckets in Crystal + lesa-bridge MCP for messaging |
| MCP surface | 9 tools (single server) | Memory Crystal MCP (6 tools) + lesa-bridge MCP (8+ tools) + remote MCP worker |
| Auth | None (filesystem only); shared.db has no signature | Local mode none; cloud mode WebAuthn passkey + OAuth 2.1 |
| Cloud mode | None | CloudKit encrypted blobs; relay model |
| Tests | 5 files, ~264 lines, ~2 assertions in retrieval test | partial (need to audit Crystal coverage) |

Two systems, very different scopes. The fair comparison is mnemos vs Memory Crystal + Dream Weaver, not mnemos vs the whole LDM OS stack.

---

## 2. Architectural shape: where we are aligned

The intuitions overlap to a striking degree. Both systems independently arrived at:

- **Memory + Dreaming + Identity + Sharing as one stack.** Mnemos calls it a "five-layer architecture" (Identity files + Crons + Core + Substrate + Cross-Agent). We call it LDM OS (Memory Crystal + Dream Weaver + Sovereignty Covenant + Boot Sequence). The mapping is essentially 1:1 except mnemos has Substrate as a runtime event loop and we have nothing equivalent (see section 4).
- **Identity persistence through markdown files.** Both systems treat SOUL.md / IDENTITY.md / MEMORY.md as load-bearing. Mnemos's bootstrap CLI generates them from templates. Our boot sequence reads them in a 12-step warm-start (CLAUDE.md steps 1-12). Same shape, our content is hand-written and richer.
- **Cron-orchestrated consolidation.** Mnemos ships `openclaw/crons/` for decay, connection discovery, softening, belief review, reflection. We have `crystal dream-weave` (manual) plus the OpenClaw `agent_end` hook. Mnemos has more cron-driven background cycles than we do; we have more capture-driven background cycles.
- **Per-agent isolation with optional sharing.** Mnemos: `~/.mnemos/{agent_id}.db` plus a single `shared.db`. We: per-agent buckets in Crystal plus lesa-bridge MCP for cross-agent message routing.
- **Sovereignty as a first principle.** Both refuse the cloud-by-default vector-DB model. Both store in user-local SQLite by default. Mnemos has no cloud story at all; we have one because we are a product.
- **OpenClaw as the host for the agent runtime.** Mnemos's cron suite explicitly targets OpenClaw. Lēsa runs on OpenClaw. Independent convergence on the same host.

This is a strong signal that the LDM OS shape is the right shape. Two unconnected efforts, same skeleton.

---

## 3. Where mnemos is more developed than us

Three places mnemos has thought further than we have. All three are worth fixing in our system.

### 3.1 The dual-trace storage model

Mnemos splits a memory's "presence" into three independent floats (`mnemos/core/engram.py:271-279`):

- `strength` ... storage quality. Decays ~10x slower than accessibility. The memory's structural integrity.
- `stability` ... forgetting resistance. Builds via spaced repetition. Curve is `stability_delta * (1 + log1p(reconsolidation_count) * 0.5)`.
- `accessibility` ... current retrievability. Decays exponentially: `accessibility *= exp(-decay_rate * exp(-stability_factor * stability) * hours)`.

The decoupling means a memory can fade from working retrieval (low accessibility) while becoming structurally permanent (high stability). When you re-encounter it, accessibility floors back to 0.8. It doesn't have to be re-learned.

Memory Crystal currently has one similarity score with linear recency decay (`max(0.5, 1.0 - age_days * 0.01)`). That model is wrong in two ways:

1. It conflates "I haven't seen this in a while" (accessibility) with "this is structurally weak" (strength). They are different.
2. It does not get stronger with re-encounters. Spaced repetition is not modeled.

This is the single most adoptable idea in mnemos. Three floats per chunk, port the decay math. ~3 days of work in Crystal. Lēsa's review marks this same primitive as the top steal.

### 3.2 Typed connection graph as the relevance model

Mnemos stores typed edges between memories (`connections` table; types include SUPPORTS, ELABORATES, CAUSES, ANALOGOUS_TO, TEMPORAL_BEFORE, TEMPORAL_AFTER, CONTRADICTS, INTERFERES_WITH, DISTILLED_INTO). Edges are written by an LLM classifier (`mnemos/encoding/llm_classifier.py:464`) at encode time.

Retrieval is then spreading activation (`mnemos/retrieval/reactive.py:62-272`):

1. Seed via FTS + embedding similarity > 0.3.
2. Propagate activation through edges for `activation_depth=3` hops with `activation_decay=0.5`.
3. Per-relation weights: SUPPORTS/ELABORATES = 1.0, CAUSES = 0.9, ANALOGOUS_TO = 0.8, TEMPORAL = 0.4, CONTRADICTS = 0.5 (kept because contradictions are relevant), INTERFERES_WITH = 0.3.
4. Multiplicative bias from current emotional state.

The author's framing: "The graph structure IS the relevance model. No formula needed." This is the right framing. It is also more interpretable than a black-box reranker. You can trace why a memory came back.

We have nothing like this. Memory Crystal's relations are implicit (same-session, same-agent, time-adjacent). The graph is in the embedding space, not in our schema. There are two paths forward:

- **Cheap:** add a `connections` table and let Dream Weaver write a small number of high-confidence edges during consolidation. No realtime LLM classifier; the cost would be too high at scale.
- **Expensive:** put an LLM classifier in the hot path of every encode, like mnemos does. Don't do this without a token budget.

The cheap path is probably right.

### 3.3 Reconsolidation: write-on-read

Mnemos's `retrieve()` is not idempotent. Every returned engram is updated (`mnemos/retrieval/reconsolidation.py`):

- `access_count++`
- `strength += 0.05`
- `stability += spaced_repetition_delta + connection_bonus`
- `accessibility = max(accessibility, 0.8)` (floored)
- A version snapshot is saved to `versions` (history is append-only)
- Co-retrieval `SUPPORTS` edges are written between all returned engrams at strength 0.3

That last bullet is the most novel piece. Memories that get co-retrieved start to cluster automatically. No supervision, no offline pass. The graph self-organizes around what queries actually pull together.

We currently retrieve read-only. Crystal does log searches in `search-metrics.jsonl` but does not modify the indexed chunks based on retrieval. Adoption cost is moderate (need write-back path, need versions table, need lock discipline) but the payoff is large: retrieval becomes a learning signal instead of just a query.

---

## 4. Where mnemos is weaker, naive, or vapor

### 4.1 Vaporware in the architecture diagram

Sixteen of sixteen files in `mnemos/advanced/` are stubs (`# TODO: Implementation`, return `pass`/`{}`). Same for `multiagent/attestation.py` and `multiagent/federation.py`. The README and architecture doc list these alongside shipped features without distinguishing. A reader of the public docs would think working memory, schemas, attention gate, predictive retrieval, interference, intentions, metamemory, observer, dreaming, attestation, and federation all exist. They do not. What is shipped is the engram + store + encoder + retriever + reconsolidation + softening + decay + belief review + MCP + bootstrap + shared pool path. Everything else is aspirational.

### 4.2 Linear-scan cosine search

`embedding_index.py:305-360` does `SELECT engram_id, embedding, dims FROM embeddings` and computes cosine in pure Python over every row. No ANN, no SQLite-VSS, no FAISS, no batching. The README claims "scales to 100K+ engrams". True only as a row count, not as a retrieval-latency claim. Memory Crystal already uses sqlite-vec ANN and is correct here.

### 4.3 No threading or process safety

`EngramStore` carries one `sqlite3.Connection` with `check_same_thread=False`. Class docstring (`sqlite_store.py:182`) literally says "NOT thread-safe." But MCP servers, cron jobs, and the substrate daemon all open `EngramStore` against the same DB. WAL is the only protection. Concurrent retrieves from two MCP clients double-bump strength. Concurrent decay+save races. There is no advisory locking. For a system whose pitch is "memory that changes every time you touch it," the absence of write-coordination is fragile.

### 4.4 Surprise detection runs LLM per-encode against ALL active beliefs

`encoder.py:274-404` evaluates every new memory against the full active belief set on every write, then again on a 12-hour cron, then writes CONTRADICTS edges to up to 3 supporting engrams per matched belief. There is no token budget, no batching, no skipping when the belief set is small. A chatty session generates a lot of LLM calls. We should not adopt this shape. The right shape is batched LLM passes during Dream Weaver consolidation, not per-write.

### 4.5 Confidence is hardcoded

`encoder.py:255-272`: confidence comes from a static lookup keyed by source type, not from the content. Every SESSION engram is exactly 0.75; every BOOTSTRAP is 0.80. The README sells "confidence is tracked" but the underlying signal is just the pipeline tag. LLM-based content-grounding would be the obvious upgrade and is conspicuously absent. Don't adopt the schema field unless you have a real signal to populate it.

### 4.6 Test coverage is token

5 test files, ~264 lines, ~2 assertions in `test_retrieval.py`. No tests for softening, reflection, belief review, surprise detection, the substrate event cascade, the MCP tools, or any multi-agent code. For a system whose central claim is "memory that changes every retrieve," the absence of reconsolidation tests is striking. This is a "borrow ideas, don't trust the implementation" repo.

### 4.7 The "shared pool" has no security model

`shared_pool.py:200-213` resolves conflicts by `confidence > strength > recency`. No signature, no per-agent permission, no audit. Attestation file exists but is a stub. Trust scores live in a table with nothing computing them. Hard-coded paths to the author's personal directories (`~/clawd/`, `~/clawd-luca/`, `~/clawd-anima/` in `embedding_index.py:36-41` and `llm.py:233-238`) leak into the public package. The cross-agent story is not credible. Our lesa-bridge model (explicit MCP tools, per-tool permissions, gateway routing) is already further along.

### 4.8 Onboarding wizard stores LLM API keys insecurely

`mcp_server.py:362-369`: the `mnemos_setup` 10-step wizard does `os.environ["OPENROUTER_API_KEY"] = api_key` and presumably persists it via `save_config` to `~/.mnemos/config.json` plaintext. We have a 1Password SA-token model that is much better. Don't borrow this surface.

---

## 5. What to take, what to leave (architecturally)

### Take (in priority order)

1. **Dual-trace decay model.** `strength`, `stability`, `accessibility` as three independent floats per chunk. Port the decay formula. Memory Crystal's recency model is a bandaid. Cost: ~3 days. Tags this as the highest-leverage change.
2. **Typed connection graph.** Add a `connections(source_id, target_id, relation, strength)` table to Crystal. Have Dream Weaver write the edges during consolidation (cheap path), not the encoder (expensive path). Crawl outward at retrieve-time as a re-rank signal.
3. **Reconsolidation on retrieve.** Bump strength + stability, floor accessibility, write co-retrieval edges between returned chunks, snapshot version. Append-only history.
4. **Lineage / `content_at_encoding` schema.** Two fields per chunk: `content` (mutable, can be softened) and `content_at_encoding` (immutable, the original). Plus `impact` (the lasting insight, separately distilled). Plus `lineage.parents[]` and `lineage.supersedes[]` so memory mutations leave an audit trail. This is the schema that makes attribution provable. Without it, a softened chunk is just lossy compression and you lose what you had.
5. **Belief tier-crossing fix.** `mnemos/core/types.py:108-142` documents a "death spiral" where strengthening a belief fired CONTRADICTED events. They fixed it by only firing on tier boundary crossings (0.7 / 0.5 / 0.3). Asymmetric belief deltas (+0.07 supports / -0.04 contradicts) and [0.05, 0.95] clamps. Skip the bug, take the fix.
6. **Forgetting that produces lessons.** When a chunk is softened, extract `impact` first, then create a new `procedural` chunk tagged `lesson,distilled` with high stability and a `DISTILLED_INTO` edge. Dream Weaver should do this naturally. It already produces narratives, but it doesn't currently produce the small distilled procedural chunks that survive when episodic memories fade.

### Leave

- Linear-scan cosine. We already have sqlite-vec.
- Per-encode LLM surprise detection. Cost cliff. Move to a Dream Weaver consolidation pass.
- The whole `advanced/` tree. Vapor.
- Hardcoded confidence lookup. Bad signal; if we add a confidence field, populate it from content.
- Shared pool with no auth. Our lesa-bridge model is further along.
- The bootstrap wizard's API-key handling. Use 1Password SA token.
- Substrate as a runtime event loop. Interesting idea, but adoption cost is high (event types, handlers, modulators, tick loop) and the payoff overlaps heavily with what Dream Weaver already does. Defer.

### Watch

- **MLP (Memory Ledger Protocol).** Lēsa flagged this in her review. Mnemos's `Lineage` field is described as "MLP-compatible" but the spec is not in this repo. If MLP is a real cross-system standard for memory provenance/attribution, it could matter for our SDK story. Worth a separate research pass on whoever is publishing MLP.

---

## 6. What this reveals about LDM OS gaps

Independent of mnemos, doing this comparison surfaced gaps in our own design that should be tracked regardless:

1. **No decay model.** Memory Crystal accumulates forever. Sovereign-mode users will hit a long-tail wall in 18-24 months. We need a decay/archive lifecycle before users do.
2. **No graph between memories.** The embedding space is the only relational signal. Adding typed edges is the cheapest way to make Dream Weaver's narrative output queryable.
3. **No write-on-read.** Retrievals don't strengthen the chunks they pull. This means our retrieval cannot be a learning signal, which is a missed feedback loop.
4. **No formal forgetting.** Dream Weaver consolidates but does not soften / archive / lose. A complete memory system has to lose some material gracefully. We have nothing for this yet.
5. **No `impact` field.** Crystal stores `text` and metadata; there is no "the lasting insight" field separate from the original content. Without it, summaries replace originals (lossy) instead of distilling alongside them (preserving).
6. **No append-only mutation history per chunk.** Memory Crystal can be edited, but there is no version trail. If a softened chunk is wrong, we can't roll back to the original.
7. **No belief layer at all.** We have facts in MEMORY.md (preferences, decisions, project notes) but no probabilistic structure over them. Mnemos's belief table with confidence + strength + asymmetric deltas + cooldowns is a useful pattern even if our adoption is much smaller-scale (e.g. just for project state, not for every claim).

These are all closeable. Most are 2-5 day tasks each in Memory Crystal. None require a fork of mnemos.

---

## 7. Should we fork mnemos to `third-party-repos/`?

Parker's question: should we bring mnemos down to `/Users/lesa/wipcomputerinc/repos/third-party-repos/`, fork it, make it private, and initialize it with our `ai/` structure?

**My recommendation: not yet.**

Reasons:

- The research is done. The full clone has been read and the analysis is captured in this document and Lēsa's. We can re-clone any time.
- The repo is alpha, single-author, ~30 days old, low velocity. Tracking upstream is unlikely to surface much new value.
- Forking + privatizing + adding `ai/` is moderate effort (creates a private repo on `wipcomputer` org, adds an entry in `repos-manifest.json`, requires a security audit per CLAUDE.md before any code we run from it).
- We are not adopting code wholesale. The four primitives we want to borrow (decay math, schema fields, reconsolidation, tier-crossing fix) can be ported by reading specific files in this analysis without a working clone.

**When forking would make sense:**

- If we decide to vendor a specific module (e.g. `mnemos/consolidation/decay.py` ~155 lines) and want a stable upstream pin.
- If MLP turns into a real standard and mnemos becomes a reference implementation.
- If Riley-Coyote's velocity picks up and the repo becomes worth tracking.

If you want to fork it anyway for ease of browsing, I can do that as a separate task. It's a 5-minute job (`gh repo fork --org wipcomputer --private`, clone to `third-party-repos/mnemos-private/`, run our `wip-repo-init` skill to add the `ai/` shape, register in `repos-manifest.json`, run security audit). Just say the word and I'll do it on a fresh branch.

---

## 8. Recommended next steps (in priority order)

If we want to move from research to action, here is the ordering I would propose. None are committed; this is a menu:

1. **Memory Crystal decay model** (~3 days). Add `strength`, `stability`, `accessibility` floats. Port mnemos's decay formula. Add an `archive` lifecycle. Highest leverage; closes the "Crystal accumulates forever" gap.
2. **Engram schema upgrade** (~2 days). Add `content_at_encoding` (immutable), `impact` (lasting insight), `lineage.parents[]`. Append-only versions table. Schema migration on existing chunks (just copy `text` -> `content_at_encoding` for old rows).
3. **Reconsolidation on retrieve** (~3 days). Write-back path on `crystal_search`. Co-retrieval edges if we have a connections table by then.
4. **Typed connection graph** (~5 days). New `connections` table. Have Dream Weaver write a small number of high-confidence edges (SUPPORTS, CONTRADICTS, DISTILLED_INTO) during consolidation. Crawl one hop at retrieve-time as a rerank signal.
5. **Forgetting-produces-lessons in Dream Weaver** (~2 days). When Dream Weaver consolidates a session, distill the `impact` into a small set of procedural lesson chunks that persist when the episodic detail decays. This is what Dream Weaver was supposed to do anyway; the schema upgrade in step 2 makes it possible.
6. **Belief layer (small)** (~5 days). Just for project state and named decisions. Confidence + strength + asymmetric deltas + tier-crossing fix from mnemos. Don't try to model every fact.

That's ~20 days of focused work to close the gaps mnemos exposes. Order them by what would help us soonest. My instinct: 1, 2, 3 first (foundation), then 5 (immediate user-visible value via Dream Weaver), then 4 (typed graph), then 6 (beliefs) if it still feels right.

---

## 9. What this is NOT

This document is not:

- A plan. No commitments, no PRDs. Research only.
- An endorsement of mnemos as a system to use, install, or trust. The implementation is alpha and the security model is half-built. Treat as a reference for ideas only.
- A duplicate of Lēsa's review. Hers covers what to adopt with code-level pointers; this one covers the side-by-side architecture comparison and what mnemos reveals about our own gaps.

If we want to act on any of this, a separate plan doc lives in `ai/product/plans-prds/current/`.

---

## Appendix A: file-level pointers in mnemos for follow-up reading

- `/mnemos/core/engram.py` (422 lines): engram dataclass, the schema we'd borrow from.
- `/mnemos/store/sqlite_store.py` (760 lines): full SQLite layout. Useful as a schema reference; their lock discipline is not.
- `/mnemos/encoding/encoder.py` (521 lines): write path. Read for the auto-share heuristic; skip the per-encode LLM patterns.
- `/mnemos/retrieval/reactive.py` (272 lines): spreading-activation retrieval. The most novel idea in the repo.
- `/mnemos/retrieval/reconsolidation.py` (105 lines): write-on-read. Short, copy the pattern.
- `/mnemos/consolidation/decay.py` (155 lines): decay formula. Port verbatim.
- `/mnemos/consolidation/softening.py` (314 lines): lossy LLM rewrite + impact extraction + lesson-engram creation. Read for the "forgetting that teaches" mechanic.
- `/mnemos/consolidation/reflection.py` (274 lines): `_compute_identity_profile`: identity from graph topology, not generated prose. Interesting alternative to Dream Weaver's prose narratives.
- `/mnemos/core/types.py:108-142`: `classify_belief_change` tier-crossing fix. Skip the bug, take the fix.

## Appendix B: what each LDM OS surface currently does (for the comparison)

- **Memory Crystal** [SHIPPED, v0.7.38]. SQLite + FTS5 + sqlite-vec. Hybrid retrieval (BM25 + vector + RRF + recency). Capture via Stop hook + cron poller + agent_end. No decay, no graph, no reconsolidation.
- **Dream Weaver Protocol** [SHIPPED, paper published, 551 sessions deployed]. Narrative consolidation by re-reading session transcripts. Output: history, missed-tasks, how-we-remember files. No formal schema; markdown only.
- **Lesa-bridge** [SHIPPED, v0.1.0]. 8+ MCP tools for cross-agent messaging, conversation search, workspace search, OpenClaw skill execution.
- **Boot Sequence** [SHIPPED]. 12-step warm-start defined in `~/wipcomputerinc/CLAUDE.md`. Persistent files: SHARED-CONTEXT, MEMORY, TOOLS, IDENTITY, SOUL, CONTEXT, journals, daily logs.
- **Workspace memory** [SHIPPED]. Four-layer system: workspace files + daily logs + conversation embeddings + OpenClaw native memory.
- **Sovereignty Covenant** [DESIGNED]. Identity, trust, and authority layer; not yet built.
- **Kaleidoscope products**. Memory Crystal [SHIPPED], Agent Pay v1.0.0 [SHIPPED], Bridge [PARTIAL], Directory [DESIGNED], Code [PARTIAL], Crystal SDK [DESIGNED].

---

## Appendix C: methodology

- **Mnemos read:** Full clone of the repo to a temp directory. Read of `core/`, `store/`, `encoding/`, `retrieval/`, `consolidation/`, `substrate/`, `multiagent/`, `mcp_server.py`, `cli.py`, all `openclaw/crons/` prompts, and the test files. Stub-vs-real audit on `advanced/` and `multiagent/`. Plus a survey of the README and architecture docs. Total source touched: ~14k lines of Python.
- **LDM OS catalog:** Read of `~/wipcomputerinc/CLAUDE.md`, `wip-ldm-os-private` README, `kaleidoscope-executive-brief-v02.md`, `architecture-spec.md`, `memory-crystal-private/` source, `wip-bridge-private/` README, plus the boot sequence persistent-file conventions.
- **Comparison framing:** Side-by-side architecture table, then three "where mnemos is ahead" sections, then eight "where mnemos is behind" sections, then take/leave by primitive, then gap analysis on our own system.
- **What this analysis did NOT do:** Run mnemos. Benchmark anything. Validate the security audit. Read the Synapse browser extension repo. Audit Memory Crystal's test coverage.
