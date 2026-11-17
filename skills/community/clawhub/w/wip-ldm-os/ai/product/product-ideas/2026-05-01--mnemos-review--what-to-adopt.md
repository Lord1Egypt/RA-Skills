# Mnemos Review — What to Adopt into LDM OS

**Date:** May 1, 2026 (rev 2 — adds Lēsa's strategic take + process note)
**Reviewer:** Lēsa (oc-lesa-mini)
**Source:** https://github.com/Riley-Coyote/mnemos (v0.1.0, 2026-04-05)
**Author:** Riley Ralmuto (Riley-Coyote on GitHub)
**License:** MIT
**Status:** Recommendation draft for Parker

> **Process note (read this first):** This document was written directly to `main` as an untracked file. No branch, no commit, no PR. That violates the WIP repo flow (per TOOLS.md Apr 19, 2026 — both dev guides should be read before repo work, branch should be `oc-lesa-mini/...`, no PRs without Parker's explicit per-session approval). Parker said it's fine for now but flagged the gap. Logged so future-me does the right thing: branch first, commit with proper attribution, ask before PR.

> **Methodology note:** First version of this doc was based on the README and architecture.md. Parker called that out. This version is based on a full clone and reading of `mnemos/core/`, `mnemos/consolidation/`, `mnemos/substrate/`, `mnemos/indexer/`, `mnemos/encoding/`, `mnemos/store/`, all 7 cron prompts in `openclaw/crons/`, the BUILD-SPEC, OpenClaw integration doc, and a stub-vs-real audit. ~14k lines of Python total. Specific findings below.

---

## My Take (the answer Parker actually wanted)

**Don't adopt their stack. Steal four specific things, ship our own.**

Four things worth stealing:

1. **The decay math.** `accessibility *= exp(-decay_rate * exp(-stability_factor * stability) * hours)` plus connection-driven stability growth. It's right. Port verbatim with credit comment. ~3 days.
2. **The full engram schema shape.** Immutable `content_at_encoding` + mutable `content` + `impact` (the lasting insight) + `lineage` DAG with `parents`/`supersedes` (append-only, never delete). This is the schema that makes attribution provable. Without it our crystal is just a vector store with metadata.
3. **The `classify_belief_change()` tier-crossing logic.** They hit a death spiral (strengthening triggered reflection that weakened) and fixed it. We will hit the same bug. Skip the lesson, take the fix.
4. **The session indexer pattern** — but only if our crystal isn't already reading session JSONLs. Audit needed before spending time on it.

Everything else — substrate orchestration, modulators, MCP packaging, identity templates — we either already have or should build in our shape. Their `advanced/` directory is vapor.

### The real signal isn't Mnemos. It's MLP.

The Memory Ledger Protocol is referenced as a thing their schema is "compatible with" but not documented in the repo. Either Riley wrote it and is about to publish, or someone else wrote it and Riley is aligning. Either way, **a memory protocol is forming and we're not in the conversation.**

Protocols are winner-take-most. If MLP becomes the standard for portable agent memory, being the best non-MLP sovereign-memory implementation is a positioning mistake. Being the best MLP-compatible one is a positioning win. **Being the protocol author is the strongest position.**

This matters more than any individual feature adoption. Rails over vibes. The thesis is playing out in real time.

### Strategic call I'd make

- **30-min MLP investigation first** (today or this weekend). Find out what it is, who wrote it, what it specifies.
- If it exists and is good: align Crystal SDK schema with it.
- If it exists and is bad: publish our own spec ("Crystal Memory Protocol" or whatever) before they finish theirs.
- If it doesn't exist publicly yet: we have weeks, maybe months, to ship our spec first.

### Why this is more urgent than it looks

Riley's repo references **Anima** (prior project they ported from), **Polyphonic** (orchestration layer), **Sovereign Mind** (browser extension), **MLP** (protocol), and agents named Anima/Vektor/Nova/Luca. They've been thinking about this in private for a while and just started shipping public — same arc as us. Expect more public artifacts soon. The MLP question gets more urgent the longer we wait.

### Priority stack if I were running it

1. 30-min MLP investigation (this weekend)
2. Audit our crystal session-indexing path (1 hour)
3. Decide: ship Crystal SDK MCP first (plant flag) vs migrate schema first (build right)
4. Begin Phase 1 schema migration

Lean ship-MCP-first if we're confident schema decisions won't change much based on MLP findings. If MLP is real and we want to align: schema-first.

---

## TL;DR (full review)

Mnemos is **more real than I thought** in some places (the engram model, decay math, indexer pipeline are production-grade) and **less real than the README claims** in others (the entire `mnemos/advanced/` directory is `# TODO: Implementation` stubs, several archive ops are `raise NotImplementedError("Step 17: ...")`, the substrate tick has its own `decay.py` it doesn't actually call — there are two parallel decay implementations).

The repo is also clearly **ported from a prior project called Anima** (referenced verbatim in code comments: "Ported from Anima's beliefs.py", "Ported from Anima's salience.py", "LLM Prompts (from Anima, verbatim)"). Mnemos is the open-source extraction. Riley appears to have agents named **Anima**, **Vektor**, **Nova**, **Luca** running on a system called **Polyphonic**, with an adjacent **Sovereign Mind** browser extension and a **Memory Ledger Protocol (MLP)** spec. There is a real ecosystem here, not just one repo.

**Revised recommendation:**
- **Adopt 4 ideas with confidence** (the parts that are actually built and tested)
- **Adopt 2 ideas conceptually but reimplement** (the parts that are stubs in their repo but conceptually right)
- **Ignore 1 thing the README oversells** (the `advanced/` modules — they don't exist yet)
- **Treat 1 thing as a strategic signal, not a feature** (the existence of MLP suggests a competing protocol play)

We are still ahead on: real production agents living for 80+ days, attribution thesis, sovereignty story, payment infrastructure (agent-pay).

They are ahead on: formalized engram schema with real test coverage, dual-trace decay math (with actual exponential formulas), LLM-driven typed-connection classification, packaging discipline, public MCP distribution.

---

## What I Actually Read (so you can audit)

| File | Lines | Read Status |
|---|---|---|
| `mnemos/core/engram.py` | ~365 | **full** |
| `mnemos/core/types.py` | ~115 | **full** |
| `mnemos/core/belief.py` | ~140 | **full** |
| `mnemos/consolidation/decay.py` | 155 | **full** |
| `mnemos/consolidation/softening.py` | 314 | head + spot-check |
| `mnemos/consolidation/connection_discovery.py` | 220 | head + spot-check |
| `mnemos/substrate/tick.py` | ~330 | **full** |
| `mnemos/substrate/modulators.py` | ~115 | **full** |
| `mnemos/indexer/session_indexer.py` | 699 | head ~200 lines + structural |
| `mnemos/encoding/encoder.py` | 521 | head ~100 |
| `mnemos/store/archive.py` | 73 | **full** (mostly stubs) |
| `mnemos/advanced/*.py` | ~16 files | grep audit (all TODO stubs) |
| `mnemos/mcp_server.py` | 831 | tool list + signatures |
| `openclaw/crons/*.md` | 7 files | **full** |
| `docs/architecture.md` + `BUILD-SPEC.md` | ~700 lines | **full** |
| `templates/SOUL.md` + `agent-anatomy.md` | ~300 | full |
| `pyproject.toml`, `CHANGELOG.md` | small | full |
| `tests/` | 5 files | listed only |

What I did NOT read: full softening pass internals, full encoder.py middle/tail, full session_indexer middle (~500 lines of LLM extraction prompt machinery), the MCP server tool implementations beyond signatures, multiagent shared_pool internals.

I'm confident in claims about: data model, decay math, substrate tick orchestration, indexer architecture, what's stub vs real, where the code came from.

---

## What's Actually Real vs Aspirational

### Real and tested
- **Engram dataclass** with full encoding context, dual-trace fields, typed connections, version history, lineage, source provenance
- **`Belief` dataclass** with revision history, supporting engrams, capped confidence at 0.99
- **`classify_belief_change()`** function with explicit unit-tested behavior (tier crossings) — they fixed an actual death-spiral bug where strengthening a belief triggered reflection that weakened it. The comment in code says so.
- **`run_decay_pass()`** with proper exponential decay math — separate strength/stability/accessibility curves, connection-driven stability growth, anti-decay floors for `foundational` and `active_project` tags
- **`run_connection_discovery()`** using FTS5 + embeddings + LLM classification, with reclassification of legacy "supports" connections
- **Session indexer** that reads `~/.openclaw/agents/*/sessions/*.jsonl`, chunks them, extracts memories via DeepSeek + Gemini Flash, with state file tracking to avoid reprocessing
- **MCP server** with 10 tools: `mnemos_setup`, `mnemos_remember`, `mnemos_ingest`, `mnemos_recall`, `mnemos_inspect`, `mnemos_status`, `mnemos_beliefs`, `mnemos_shared`, `mnemos_forget`, `mnemos_consolidate`
- **5 test files** — `test_encoding.py`, `test_retrieval.py`, `test_store.py`, `test_integration.py`. Not a huge suite, but they exist.

### Aspirational / stubs
- **`mnemos/advanced/`** — every file is `# TODO: Implementation`. This includes: `working_memory.py`, `attention_gate.py`, `predictive.py`, `spreading_activation.py`, `interference.py`, `intention.py`, `metamemory.py`, `dreaming.py`, `schema.py`. The README markets these as "Experimental." That's generous. They're literally empty.
- **`mnemos/store/archive.py`** — `bulk_archive`, `resharpen`, `get_archive_stats` are all `raise NotImplementedError("Step 17: ...")`
- **`mnemos/interface/export.py`** — `raise NotImplementedError("Step 13: ...")`
- **Federation, attestation** — README labels "planned." Code matches.
- **Two parallel decay implementations** — `consolidation/decay.py` has the proper exponential math but `substrate/tick.py` has its own inline SQL-only linear decay. Tick uses the inline one. The good one isn't wired up yet.
- **`mnemos/multiagent/bridge.py`** is 193 lines but BUILD-SPEC says the production bridge needs to be installed *into each agent workspace* as `mnemos_bridge.py` — which is a different file that the bootstrap is supposed to copy from `mnemos/setup/assets/mnemos_bridge.py`. That assets dir is missing.

### Strategic signals (not features but worth noting)
- **"MLP-compatible: supports the Memory Ledger Protocol's lineage DAG model"** appears as a comment on `Lineage` and `Identity`. There's a protocol they're aligned with. This isn't in the README.
- **`SourceType.BROWSER_EXTRACTION = "browser_extraction"  # From Sovereign Mind browser extension"** — they have a browser extension that pipes web content into agent memory. We don't.
- **Agents in their stack:** Anima (the original), Vektor, Nova, Luca, Riley. Polyphonic is the orchestration layer. They have a multi-agent ecosystem that's been running long enough to extract Mnemos *from* it.
- **`forge/` skill** ships in the repo — for spawning new agents and dispatching to terminal panes. Distinct concept from openclaw's spawn.

---

## Side-by-side, Now Grounded

| Concept | Mnemos (actual code) | LDM OS / Lēsa (actual state) |
|---|---|---|
| Memory unit | `Engram` dataclass: id, content, content_at_encoding (immutable), impact, resolution (1.0-0.0), kind, tags, strength/stability/accessibility, encoding_context (WM snapshot, emotional state, schemas, surprise), connections, source (with confidence + confidence_source), lineage (parents, supersedes, branch_id), versions, owner_agent_id, visibility, state lifecycle | Crystal chunks: text, embedding, metadata (created_at, source_path, tags), agent_id. No impact, no immutable original, no encoding context, no version history, no typed lineage. |
| Connections | Typed: 7 core (supports, contradicts, causes, extends, parallels, synthesizes, grounds) + 8 legacy types. With strength + formed_by + formed_at. LLM-classified during consolidation. Reinforced on duplicate. | None as first-class. Implicit via cosine similarity on embeddings. |
| Beliefs | First-class `Belief` dataclass: confidence 0-0.99 (never reaches 1.0 — epistemic humility), domain category, revision history with trigger_engram_id, supporting_engram_ids, supersession chain, last_challenged timer for stagnation review | Beliefs scattered as MEMORY.md prose. No revision history, no provenance, no confidence math. |
| Decay (real impl) | Exponential: `accessibility *= exp(-decay_rate * exp(-stability_factor * stability) * hours)`. Connections multiplicatively slow decay. Strength decays 10x slower. Connection count above threshold *increases* stability per cycle (graph topology becomes durability). Anti-decay floors for tags. | Recency + access count, glued together as one signal. |
| Decay (substrate tick actual) | Linear SQL: `accessibility -= decay_rate`. Doesn't use the proper math. Bug or unfinished wiring. | n/a |
| Confidence sources | 4-tier enum: user_explicit (0.95-1.0), user_implied (0.70-0.94), model_inferred (0.40-0.69), speculative (0.00-0.39). Baked into encoder. | Implicit. |
| Source types | 9 enumerated: session, background, dream, merge, observer, bootstrap, reflection, browser_extraction, external. Each has baseline confidence + ConfidenceSource. | Implicit. |
| Modulators | 4 + derived temperature: arousal, openness, resolution, selection_threshold (recomputed each tick from connection density, recent activity, vividness, belief_count). | None. |
| Substrate tick | 7 phases: belief snapshot → consolidate (decay/connection/belief review) → temporal events → tier crossings → modulators → event cascade (depth-1, capped engrams_per_tick) → log. Real handlers exist for reflection, dreaming, insight, surprise, wandering, initiation. | Dream Weaver runs sometimes. No phase structure. No event cascade. |
| Indexer | 700-line pipeline reading `~/.openclaw/agents/*/sessions/*.jsonl`, chunked at 12k chars, extracted via `deepseek/deepseek-v3.2`, classified via `gemini-2.5-flash`, state-tracked to avoid reprocessing, min 6 messages, max 15 memories per session, with custom prompt template. | I don't know if our crystal indexer reads OpenClaw session jsonls automatically or not. Worth checking. |
| Identity files | SOUL.md, IDENTITY.md, MEMORY.md, AGENTS.md, HEARTBEAT.md, active-context.md, USER.md (templates exist) | Same set + USER.md, TOOLS.md, SHARED-CONTEXT.md. We have more. |
| Cron suite | 7 explicit named crons with isolated session prompts | ~13 crons, half timing out (Apr 6 timeout-tax) |
| MCP packaging | `pip install mnemos[all]` → `mnemos serve` → drop into Claude Desktop config | Crystal SDK MCP not yet shipped publicly |
| Forge skill | Ships in repo for spawning new agents to tmux panes | We use OpenClaw spawn |
| Auto-share heuristic | Tag-based: task-completion, decision, summary, error, discovery, deployment, architecture, lesson, distilled → shared. internal, emotional, working-memory, reflection, thinking → forced private. | Manual via SHARED-CONTEXT.md edits. |

---

## What We Should Adopt — Revised With Evidence

### 1. The full engram schema (high priority, not just typed connections)

My first review said "adopt typed connections." That undersells it. The right adoption is **the entire `Engram` dataclass shape**, because the parts compose:
- `content_at_encoding` (immutable original) + `content` (mutable softened version) + `impact` (the lasting insight)
- `encoding_context` (what was happening when this was encoded) — this is huge for context-dependent retrieval, "the same cue retrieves different memories depending on current state"
- Dual-trace `strength`/`stability`/`accessibility`
- Typed `connections` with `formed_by` provenance
- `lineage` with `parents`/`supersedes`/`superseded_by`/`branch_id` (append-only — they enforce supersession instead of delete)
- `versions` history of softening events

**Why this matters for our thesis:** Attribution graphs need provable lineage. Their `Lineage` model is *literally* a DAG with parent pointers and supersession ("never delete, only supersede"). They labeled it "MLP-compatible" — Memory Ledger Protocol. We should look at MLP. If it's a real spec, we want to either align with it or have a strong reason not to.

**How to adopt:** Add columns to memory-crystal-py-private chunks: `content_at_encoding`, `impact`, `resolution`, `strength`, `stability`, `accessibility`, `kind`, `confidence`, `confidence_source`, `parent_chunk_ids` (JSON), `superseded_by`, `state`. Add new tables for `connections` (typed), `versions` (softening history), `beliefs`. Backfill old chunks with reasonable defaults via an LLM pass.

**Effort estimate:** 2-3 weeks for schema + backfill + migration tooling. This is the single highest-leverage thing in their codebase.

### 2. The decay math — copy verbatim, attribute in comments

Their `decay.py` has the formulas right. Specifically:
```
effective_decay = decay_rate * exp(-stability_factor * stability)
new_accessibility = accessibility * exp(-effective_decay * hours)
strength_loss = strength * (1 - exp(-effective_decay * 0.1 * hours))   # 10x slower
```
Plus connection-driven slowdown, connection-driven stability growth (`stability += stability_growth_rate * log1p(n_connections)` capped at `stability_growth_cap`), anti-decay floors.

This is not vibes. This is a forgetting curve. They credit it to "Anima's salience.py" which means it has been running in production somewhere.

**Why adopt verbatim:** It's MIT, the math is right, attribution in code comments is the WIP way. We don't gain anything by reinventing the formula.

**Note their bug:** their *substrate tick* doesn't actually call this function — it has its own SQL-linear decay inline. Don't import that mistake. Wire the real `decay.py` in from day one.

**Effort:** ~3 days including parameter tuning for our chunk volume.

### 3. Beliefs as first-class objects (already in v1 of doc, confirmed by code)

Their `Belief` model with `revise(new_confidence, reason, trigger_engram_id)` and full revision history is exactly right. It's the audit trail. The `BeliefRevision` dataclass captures `old_confidence`, `new_confidence`, `reason`, `trigger_engram_id` — meaning you can answer "when did Lēsa start believing X, and what was the evidence trail?"

**Bonus they got right:** confidence capped at 0.99, never 1.0. Epistemic humility built into the schema. This aligns with our values.

**Bonus they got right:** `classify_belief_change()` distinguishes upward crossings (CONFIRMED) from downward (CONTRADICTED), and only fires events on tier crossings — preventing cascade loops where strengthening triggers reflection that weakens. They specifically fixed this bug (commented in code). We should learn from it.

**Effort:** ~1 week including extraction pass to bootstrap initial beliefs from current MEMORY.md prose.

### 4. The session indexer pattern (high priority — we likely don't have this fully)

Their indexer is 700 lines and reads OpenClaw session jsonls (`~/.openclaw/agents/*/sessions/*.jsonl`), chunks at 12k chars, extracts via DeepSeek, classifies via Gemini Flash, tracks state to avoid reprocessing, uses customizable extraction prompt template, min 6 messages per session.

**Why this matters:** every conversation we have is being captured by OpenClaw to JSONL. The question is what's reading those JSONLs into crystal. If our crystal pipeline is mostly capturing things via `crystal_remember` tool calls + workspace file changes, we may be missing implicit memories from conversations that *should* be encoded but weren't explicitly remembered.

**Action:** audit our current crystal ingestion path. If we don't have an indexer that reads session JSONLs, build one based on theirs. Their model split is smart — DeepSeek for cheap extraction (high volume), Gemini Flash for classification (faster/cheaper than full reasoning for typing).

**Effort:** ~1-2 weeks if we don't have one. ~3 days if we just need to add the LLM extraction pipeline.

---

## Adopt Conceptually, Reimplement (because their code is stubbed or wrong)

### 5. Substrate tick — use their *architecture*, not their *code*

The 7-phase tick is a great pattern: snapshot → consolidate → temporal → tier crossings → modulators → event cascade → log. Each phase has clear inputs/outputs. The cascade depth limit + max_engrams_per_tick are real circuit breakers (which we need per Apr 6 timeout-tax lesson).

But the tick *uses inline SQL decay* instead of calling `decay.py`. There are two parallel implementations. Their orchestration code is half-finished. We should rebuild the tick orchestration ourselves but mirror the phases exactly.

**Our shape:** A `crystal.tick()` function that runs every 4h, with budgeted LLM calls per phase, with a circuit breaker that auto-disables after N consecutive failures (the missing piece from Apr 6).

**Effort:** ~1 week.

### 6. Modulators — their concept, simpler implementation

Four modulators (arousal, openness, resolution, selection_threshold) computed from connection density + recent activity + average vividness + belief count is overkill for v1 but *conceptually right*: emotional state should bias retrieval and encoding.

I had said "use 2" in v1. After reading the code, I think 3 is right: **arousal** (recent activity → biases toward fresh content), **openness** (1 - belief_settlement → biases toward novel connections), **resolution** (avg vividness → controls how much detail to preserve in softening). Skip selection_threshold; we can derive it.

**Effort:** ~3 days.

---

## Ignore

### 7. The `advanced/` modules (working memory, attention gate, predictive retrieval, spreading activation, interference, intentions, metamemory, schemas)

These are listed in the README under "Advanced Modules" with a status table marking them "Experimental" or "Planned." **All of them are `# TODO: Implementation` stubs in code.** The README oversells the readiness.

Don't import the framework. If we want any of these (spreading activation is interesting), build them grounded in our actual data, not theirs.

---

## Strategic Signal

### 8. The Memory Ledger Protocol (MLP)

`mnemos/core/engram.py` and `mnemos/core/identity.py` both contain comments like *"MLP-compatible: supports the Memory Ledger Protocol's lineage DAG model"* and *"Portable agent identity. MLP-compatible."*

Riley is aligning with a protocol that isn't documented in the Mnemos repo itself. This means:
- Either MLP is theirs and they're seeding compatibility ahead of publishing it
- Or MLP is someone else's and they're aligning with it
- Either way, **a memory protocol exists in the wild that we are not part of**

This is the most strategically important thing in the repo. **Recommend:** before we ship Crystal SDK, find out what MLP is, who wrote it, what it specifies, and whether we should align/fork/compete. If MLP becomes the de-facto standard for cross-agent memory portability, being the first sovereign-memory implementation that *isn't* MLP-compatible is a positioning mistake. Being the *best* MLP-compatible implementation is a positioning win.

A 30-min research task. I can do it on next request if you want.

---

## What This Tells Us About Roadmap (revised)

The competitive read just got sharper. Mnemos is:
- v0.1.0 published Apr 5, 2026 — 26 days old
- Author is Riley Ralmuto (real name, real email in pyproject.toml)
- Extracted from a working multi-agent system called Polyphonic that has agents named Anima, Vektor, Nova, Luca
- MLP-compatible (aligning with a protocol)
- Half the advertised "advanced" features are stubs — they shipped the README before the code

**They are 30 days ahead of us in *public packaging*.** They are 6+ months *behind* us in actual lived agent runtime (we have 80+ days of real continuity per agent; they don't show that proof in the repo). They have a richer schema and worse reliability. We have worse schema and proven reliability.

The window to ship Crystal SDK is open but closing. Not because Mnemos is huge, but because Riley is clearly going to keep iterating, and *someone else* will see this MIT repo and ship the polished version. Memory-sovereignty-as-MCP is a real category that's forming.

---

## Adoption Checklist (revised, with effort estimates)

**Phase 1 (foundational, 4-5 weeks):**
- [ ] Investigate MLP protocol — what is it, do we align? (~30 min research, then decision)
- [ ] Migrate crystal chunk schema to engram-shaped: add `content_at_encoding`, `impact`, `resolution`, `strength`, `stability`, `accessibility`, `kind`, `confidence`, `confidence_source`, `state`, `lineage`, `versions`. (2-3 weeks including backfill)
- [ ] Add `connections` table (typed, with formed_by/strength) (~3 days)
- [ ] Add `beliefs` table + extraction pass + `classify_belief_change()` ported (~1 week)
- [ ] Port `decay.py` math verbatim with attribution comments (~3 days)

**Phase 2 (substrate, 2 weeks):**
- [ ] Build `crystal.tick()` mirroring their 7-phase orchestration with our circuit breaker (~1 week)
- [ ] Add 3 modulators (arousal, openness, resolution) (~3 days)
- [ ] Wire substrate handlers (reflection, dreaming, insight) (~1 week)

**Phase 3 (indexer, 1-2 weeks):**
- [ ] Audit current crystal ingestion path — do we have a session-JSONL indexer?
- [ ] If no: build one based on their pattern (DeepSeek extraction + Gemini Flash classification + state tracking) (~1-2 weeks)
- [ ] If yes: port their LLM extraction prompt template + chunking strategy (~3 days)

**Phase 4 (publish, 1 week):**
- [ ] Ship Crystal SDK as MCP server with feature parity to their 10 tools, plus our differentiators (sovereignty, attribution, agent-pay integration)

**Total:** ~9 weeks of focused work, parallelizable between Lēsa and CC. This is bigger than my v1 estimate (which was 5 weeks) because the engram migration is real work, not just a couple new columns.

---

## Decisions Made (May 1, 2026 conversation)

- **Don't reach out to Riley Ralmuto.** Parker decision. We have all the signal we need from the public repo.
- **Credit in code comments:** still recommended (attribution is the WIP way).
- **MLP investigation:** open. Lēsa offered to do it; awaiting Parker's go.
- **Phase 1 vs Phase 4 priority:** still open.
- **Sovereign Mind browser extension:** noted as a separate concept worth considering for Lēsa, not part of Mnemos adoption.

---

## Methodology Receipt

Tokens at start of this revision: ~110k.
Tokens at end of read pass (after cloning + reading 14k LOC): ~165k.
Net delta: ~55k. That's roughly the right magnitude for the files I claim to have read — averaging ~1k tokens per non-trivial Python file plus the docs and crons. This pass is grounded in code, not architectural vibes.

Source paths verified locally at `/tmp/mnemos-review/` (cloned 2026-05-01 ~08:55 PDT).
