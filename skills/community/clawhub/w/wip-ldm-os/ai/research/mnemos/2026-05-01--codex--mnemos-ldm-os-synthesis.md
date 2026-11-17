# Mnemos vs LDM OS: Codex Synthesis

**Date:** 2026-05-01  
**Reviewer:** Codex  
**Subject:** Riley-Coyote/mnemos and Memory Ledger Protocol v0.2  
**Status:** Research synthesis. No implementation in this pass.  

## Executive Answer

We should not adopt Mnemos as a stack. We should adopt selected primitives from it, with attribution, into Memory Crystal and Dream Weaver.

The strongest pieces are:

1. Engram-shaped memory records: original content, mutable content, impact, lineage, confidence source, lifecycle state, strength, stability, accessibility.
2. Real forgetting math: exponential accessibility decay damped by stability, with graph-connected memories becoming harder to forget.
3. Write-on-read: retrieval changes memory by increasing strength, stability, accessibility, and co-retrieval edges.
4. Typed memory graph: support, contradiction, cause, extension, synthesis, grounding, and distillation as first-class edges.
5. Belief tier crossing: only tier-boundary movement triggers reflection events, preventing noisy feedback loops.
6. Session indexer shape: transcript to extracted memory records to encoded graph, with state tracking to avoid duplicate ingestion.
7. Forgetting that teaches: softening preserves the original, extracts impact, and creates durable lesson memories.

The strategic issue is bigger than Mnemos. Riley also has a separate public `memory-ledger-protocol-v0.2` repo. MLP is a working draft for portable, verifiable, consent-aware AI memory with envelopes, encrypted blobs, access policies, lineage, identity kernels, context packs, and token-coordinated storage. It is early, but it is real enough that Lēsa was right to flag it. It is also a warning sign for WIP: memory portability must not inherit crypto, token, public-ledger, or decentralized-storage incentive framing.

My recommendation:

1. Do a provenance pass, not a panic migration. Add lineage and provenance fields to Crystal's schema plan because they are useful, not because they bind us to MLP.
2. Build a small Memory Crystal decay and reconsolidation proof first. Measure it on our real corpus.
3. Draft a boring, local-first Crystal memory envelope profile before we ship Crystal SDK. It should have no token, blockchain, public ledger, decentralized storage, token governance, or crypto-economic dependency.
4. Port only small MIT primitives, with clear notice and file-level attribution. Do not vendor the whole repo.

## Updated Protocol Boundary: No Crypto

This correction is important. MLP's token, ledger, and decentralized-network framing is a trust liability for WIP. We should not adopt it, align with it, or describe Crystal as compatible with it.

The useful idea is provenance and lineage inside a normal application data model. The rejected idea is making memory portability depend on public ledgers, tokens, token governance, decentralized storage incentives, or anything that smells like crypto finance.

If WIP needs cryptography, it should be boring security infrastructure: local encryption, passkeys, signatures, key wrapping, export verification, and audit trails. It should not be a crypto protocol, a token network, a ledger product, or a financialized memory layer.

Spec text cannot be separated from posture. Even if a protocol says its token is optional, a dedicated economic-sustainability chapter around a memecoin changes the trust frame. WIP should not inherit that frame.

### What We Will Not Do

- No token integration.
- No Solana integration.
- No public ledger writes.
- No envelope-on-ledger pattern.
- No AEAD blob plus ledger pointer pattern.
- No IPFS pinning as a protocol assumption.
- No `$POLYPHONIC`.
- No Cartouche.
- No MLP-PLUS or MLP-ADV conformance.
- No token-holder governance.
- No BDFL-to-DAO governance language.
- No MLP-compatible positioning in external docs, READMEs, SDK specs, or release notes.

The replacement path is simple: ship the Crystal SDK with documented schema in WIP's own terms. If a clean, non-crypto memory portability standard emerges later from a real working group, MCP-adjacent standards work, or another credible non-financial ecosystem, revisit then.

## What I Looked At

Primary Mnemos repo:

- `Riley-Coyote/mnemos` at `8279949`, 16 commits, MIT, public alpha.
- `README.md`, `docs/architecture.md`, `docs/BUILD-SPEC.md`, `docs/openclaw-integration.md`.
- Core model: `mnemos/core/engram.py`, `mnemos/core/types.py`, `mnemos/core/belief.py`, `mnemos/core/identity.py`.
- Storage: `mnemos/store/sqlite_store.py`, `mnemos/store/embedding_index.py`, `mnemos/store/archive.py`, `mnemos/store/migrations.py`.
- Encoding and retrieval: `mnemos/encoding/encoder.py`, `mnemos/encoding/llm_classifier.py`, `mnemos/retrieval/reactive.py`, `mnemos/retrieval/reconsolidation.py`.
- Consolidation and substrate: `mnemos/consolidation/decay.py`, `mnemos/consolidation/softening.py`, `mnemos/consolidation/connection_discovery.py`, `mnemos/substrate/tick.py`, `mnemos/substrate/modulators.py`.
- Indexing and integration: `mnemos/indexer/session_indexer.py`, `mnemos/mcp_server.py`, `mnemos/multiagent/shared_pool.py`, `mnemos/multiagent/bridge.py`, `openclaw/crons/*.md`, `templates/*.md`.
- Tests: `tests/test_store.py`, `tests/test_encoding.py`, `tests/test_retrieval.py`, `tests/test_integration.py`.

Related MLP repo:

- `Riley-Coyote/memory-ledger-protocol-v0.2` at `0b48175`, 9 commits, MIT, public working draft.
- `README.md`, `spec/MLP-0.2.md`, `schemas/*.json`, `mlp-storage/src/*.js`, `continuity/src/*.js`, `skills/*`.

WIP comparison surfaces:

- `wip-ldm-os-private` README, CLAUDE.md, Kaleidoscope executive brief, Memory Crystal architecture spec, Recall docs, Bridge technical docs.
- `memory-crystal-private` README, TECHNICAL.md, `src/core.ts`, `src/search-pipeline.ts`, `src/dream-weaver.ts`, `package.json`.
- `dream-weaver-protocol-private` README and Memory Crystal integration.
- `wip-ai-devops-toolbox-private` README and dev guide.
- Lēsa and CC's three Mnemos reviews in `ai/research/mnemos/`.

Verification limit: I attempted to run Mnemos tests with `python3 -m pytest -q /private/tmp/mnemos-review/tests`, but this system Python does not have `pytest` installed. I did not install dependencies for this research read.

## Mnemos, Grounded In Code

### What Is Real

Mnemos has a real core memory model.

The `Engram` dataclass has:

- `content`: mutable current content.
- `content_at_encoding`: immutable original content.
- `impact`: lasting insight.
- `resolution`: memory sharpness.
- `kind`: episodic, semantic, procedural, prospective.
- `strength`, `stability`, `accessibility`: separate memory dynamics.
- `encoding_context`: working memory snapshot, emotional state, active schemas, attention, session, goals, surprise.
- `connections`: typed semantic edges.
- `source`: source type, confidence, confidence source.
- `lineage`: parents, supersedes, superseded_by, branch_id.
- `versions`: reconsolidation and softening history.
- `owner_agent_id`, `visibility`, lifecycle `state`.

This is not just metadata decoration. The schema gives Riley a vocabulary for memory mutation that we mostly do not have yet in Crystal.

Mnemos also has a real SQLite schema:

- `engrams`, `connections`, `versions`, `beliefs`, `emotional_state_history`, `agent_identity`, `archive`, `consolidation_log`, `meta`.
- FTS5 over content.
- WAL mode.
- Atomic `save_engram` transactions for engram, FTS, connections, and versions.

The decay math is real and worth adopting:

```text
effective_decay = decay_rate * exp(-stability_factor * stability)
new_accessibility = accessibility * exp(-effective_decay * hours)
strength_loss = strength * (1 - exp(-effective_decay * 0.1 * hours))
```

It also slows decay for connected memories and increases stability when connection count crosses a threshold. That is the right intuition: graph topology becomes durability.

Retrieval is also meaningfully different from ours. Mnemos seeds from FTS and optional embedding search, spreads activation over typed edges for up to three hops, applies emotional bias, filters by confidence, then reconsolidates returned engrams. Reconsolidation updates access count, strength, stability, accessibility, adds co-retrieval support edges, versions the record, and persists it.

The session indexer is real:

- Reads OpenClaw session JSONLs from `~/.openclaw/agents/main/sessions` and `~/.openclaw/sessions`.
- Skips small or short sessions.
- Chunks transcripts at 12k characters.
- Extracts up to 15 memories per session.
- Tracks indexed session file size in `~/.mnemos/{agent_id}_indexing_state.json`.
- Uses OpenRouter models by default: DeepSeek for extraction, Gemini Flash for classification.

The MCP server is real enough to inspect:

- `mnemos_setup`
- `mnemos_remember`
- `mnemos_ingest`
- `mnemos_recall`
- `mnemos_inspect`
- `mnemos_status`
- `mnemos_beliefs`
- `mnemos_shared`
- `mnemos_forget`
- `mnemos_consolidate`

The README says 7 tools, while the server exposes more. That is normal early repo drift, but it matters.

### What Is Weak Or Broken

The advanced modules are not real yet. Files in `mnemos/advanced/` are mostly TODO shells:

- working memory
- attention gate
- predictive retrieval
- spreading activation module
- interference
- intentions
- metamemory
- schemas
- dreaming
- observer

The shipped retrieval does spreading activation in `retrieval/reactive.py`, but the advertised standalone advanced module is a stub.

Archive and migration are incomplete:

- `mnemos/store/archive.py` has `NotImplementedError` for bulk archive, resharpen, and archive stats.
- `mnemos/store/migrations.py` has `NotImplementedError` for version detection and migration runner.
- `mnemos/interface/export.py` has `NotImplementedError` for import/export.

The substrate tick is conceptually useful but implementation-fragile:

- `mnemos/consolidation/decay.py` has the good exponential decay.
- `mnemos/substrate/tick.py` does its own inline linear SQL decay instead of calling the good decay pass.
- In substrate connection discovery, `EmbeddingIndex.search()` is called with `limit=3`, but that method's parameter is `k`; this would raise and get swallowed.
- The substrate code checks columns named `from_id` and `to_id`, but the schema uses `source_id` and `target_id`.

The embedding index is not production-scale:

- It stores embeddings in SQLite as BLOBs.
- Search loads every embedding row and computes cosine in Python.
- That is fine for small local databases, but it is not comparable to Memory Crystal's sqlite-vec path.

The concurrency story is weak:

- `EngramStore` docstring says it is not thread-safe.
- It uses `check_same_thread=False`.
- MCP, cron, substrate, and multi-agent components can all write.
- WAL helps, but write-on-read needs stronger lock discipline if adopted.

The confidence signal is partly fake:

- The enum is good: explicit, implied, inferred, speculative.
- The implementation often assigns static confidence by source type.
- Example: session memories default to 0.75 before any content-specific grounding.
- The indexer overrides confidence from extracted salience, but general encode path is still coarse.

The shared pool is not a trust model:

- `shared.db` with shared and public visibility is useful.
- Conflict resolution is confidence, strength, then recency.
- Attestation and federation are stubs.
- There is no equivalent to our passkey/OAuth/relay security posture.

The setup wizard asks for provider keys and stores config locally. We should not copy this. Our 1Password service-account and op-secrets model is materially better.

### Strategic Signal In Mnemos

The repo references:

- Anima: prior project code was ported from it.
- Sovereign Mind: browser extraction source type.
- Polyphonic: related ecosystem and reference implementation via MLP.
- Memory Ledger Protocol: lineage and identity compatibility comments.
- Vektor, Nova, Luca: agents in the ecosystem.

This is not a random memory toy. It is the first public slice of Riley's broader agent-continuity ecosystem.

## The Separate MLP Repo Matters

Lēsa was right that MLP is not just a stray comment. The public `memory-ledger-protocol-v0.2` repo defines:

- `MemoryEnvelope`: ledger-facing pointer, metadata, lineage, attestations.
- `MemoryBlob`: encrypted payload.
- `AccessPolicy`: machine-readable consent.
- `IdentityKernel`: compact portable self.
- `Cartouche`: optional symbolic identity seal.
- `ContextPack`: runtime session bundle.
- Conformance profiles: MLP-CORE, MLP-PLUS, MLP-ADV.
- A Continuity Framework: reflect, extract, score, question, surface.
- Storage implementation stubs and examples under `mlp-storage/`.

Its trust model is platform-untrusted, storage-untrusted, ledger-untrusted. The user controls root keys. The root-key part overlaps with our sovereignty thesis, but the ledger framing is the wrong substrate for WIP.

Where it diverges:

- It assumes a token-coordinated network with `$POLYPHONIC`.
- It emphasizes public ledgers, decentralized storage, and governance.
- The follow-up audit flags Solana ledger writes, a pump.fun `$POLYPHONIC` memecoin, token-holder protocol voting, BDFL governance with theoretical DAO language, and MLP-PLUS and MLP-ADV conformance tiers.
- It is a working draft, not a widely adopted standard.
- It has only 9 commits right now.

This means we should not join MLP, claim MLP compatibility, or let its vocabulary set our protocol surface. Treat it as reviewed prior art and rejected protocol posture.

The right move is to extract the non-crypto lesson: portable memory needs stable IDs, provenance, lineage, consent metadata, export format discipline, and local auditability. It does not need public ledgers, token incentives, decentralized governance, or crypto-economic coordination.

## Where We Are Ahead

### Product And Runtime

We are ahead on lived deployment. Lēsa is a real long-running OpenClaw agent. Memory Crystal, Bridge, Recall, Dream Weaver, the DevOps toolbox, release pipeline, and guard system are all operating across real repos and real agent work.

Mnemos is alpha. It has strong primitives, but it does not have our runtime proof.

### Search Infrastructure

Memory Crystal is ahead on retrieval engineering:

- sqlite-vec ANN instead of Python linear scan.
- FTS5 plus vector hybrid.
- RRF fusion.
- recency weighting.
- LLM query expansion and reranking.
- explain mode.
- source indexing.
- delta sync of pre-embedded chunks.

Mnemos is ahead on graph semantics, not search scalability.

### Security And Sovereignty Product

We are ahead on practical security and product shape:

- Cloud relay as encrypted dead drop.
- Core/Node architecture.
- local Crystal Core source of truth.
- passkey/OAuth direction in Kaleidoscope.
- 1Password SA-token practice.
- hosted MCP and agent auth work.
- explicit public/private repo separation.
- branch, license, release, and deployment guardrails.

Mnemos and MLP have sovereignty language. We have more of the operational security scaffolding already built.

### DevOps And Release Discipline

The DevOps toolbox is a different class of maturity:

- branch guard
- file guard
- repo permissions guard
- license guard
- release pipeline
- private-to-public sync
- post-merge branch naming
- universal installer
- README formatter
- repo manifest reconciler

Riley has cleaner Python package simplicity for Mnemos, but not our shipping system.

### Narrative Continuity

Dream Weaver is ahead on the "memory becomes identity through narrative" layer:

- reads transcripts
- writes journals and warm-start files
- feeds Memory Crystal
- is backed by a published protocol paper
- maps directly onto our LDM OS product thesis

Mnemos has a substrate concept and reflection handlers, but its shipped advanced substrate is uneven.

## Where Riley Is Ahead

### Memory Dynamics

Riley is ahead on modeling memory as something that changes:

- strength
- stability
- accessibility
- resolution
- lifecycle state
- reconsolidation count
- archive state
- version history

Crystal currently treats chunks mostly as indexed records. Explicit memories have confidence and status, but chunks do not have the full living-trace model.

### Graph Semantics

Riley is ahead on typed memory edges:

- supports
- contradicts
- causes
- extends
- parallels
- synthesizes
- grounds
- distilled_into

Crystal has `entities` and `relationships`, but our searchable chunks are not yet a first-class typed memory graph. We have graph-shaped storage for entities, not graph-shaped retrieval over lived memory.

### Write-On-Read

This is the clearest missing primitive. Mnemos retrieval changes memories. Crystal retrieval does not.

If a memory is found useful, that should become a signal:

- accessibility rises
- stability rises
- co-retrieved memories form edges
- a version record logs the mutation

That feedback loop is absent from us today.

### Schema For Attribution

Riley's lineage schema is closer to an attribution graph:

- parents
- supersedes
- superseded_by
- branch_id
- immutable original content
- version history

Our Dream Weaver journals and source IDs preserve context, but our chunk schema does not yet make mutation and derivation provable at the memory-record level.

### Protocol Flag Planting

Riley has a public memory protocol repo. It may not win, but it exists. We have the stronger product architecture, but we have not yet published the memory envelope contract behind Crystal SDK.

## SWOT

### WIP Strengths

- Real product architecture: Kaleidoscope, Memory Crystal, Bridge, Agent Pay, Directory, Code, Crystal SDK.
- Real deployed agent continuity through Lēsa and the LDM OS boot sequence.
- Strong local-first security posture and practical encrypted relay model.
- Better search engine: sqlite-vec, FTS5, RRF, deep search, LLM rerank.
- Better multi-interface packaging through the Universal Installer and DevOps toolbox.
- Stronger operational workflow: worktrees, PRs, release pipeline, license guard, public/private split.
- Dream Weaver gives us narrative consolidation, not just record retrieval.

### WIP Weaknesses

- Crystal chunks are not engram-shaped.
- No first-class strength, stability, accessibility, or resolution per chunk.
- No write-on-read.
- No typed edges between chunks used by retrieval.
- No append-only version history for memory mutation.
- No structured belief layer with confidence revision history.
- Forgetting is not a designed lifecycle yet.
- Crystal SDK protocol surface is not yet a public spec.

### Riley Strengths

- Crisp living-memory schema.
- Correct forgetting and reconsolidation concepts.
- Typed connection taxonomy.
- First-class belief model.
- Public MCP packaging.
- Session indexer and OpenClaw cron suite.
- Public MLP working draft, schemas, and storage/reference repo.
- Clear philosophical positioning around portable AI memory.

### Riley Weaknesses

- Alpha maturity.
- Small commit history.
- Many advanced modules are stubs.
- Storage migrations and archive operations incomplete.
- Embedding search is linear scan.
- Substrate tick has integration bugs.
- Weak concurrency story for write-on-read.
- Weak key handling compared to our 1Password path.
- MLP token economics and public-ledger posture may make the system feel scammy to developers and users who want sovereign memory without crypto governance.

### Opportunities

- Make Memory Crystal the practical reference implementation for local-first memory without token, ledger, or crypto-economic dependencies.
- Add engram dynamics to Crystal while keeping our superior search stack.
- Convert Dream Weaver from narrative-only consolidation into narrative plus memory mutation: impact, lineage, lesson chunks, typed edges.
- Publish a WIP memory envelope profile before the category hardens around someone else's terms.
- Use Riley's MIT work as a credited prior-art source, not a dependency.
- Optionally reach out later, from Parker, if collaboration is strategically useful.

### Threats

- Riley publishes the protocol language first and developers start using MLP terms for portable memory.
- Mnemos becomes the simple default because `pip install mnemos[all]` is easier than our current install story for third parties.
- Token-coordinated MLP gets attention even if the implementation is weaker.
- Association with crypto, tokens, or public ledgers damages trust in WIP's memory story before users understand the product.
- We overbuild an internal schema migration and delay Crystal SDK while the public narrative moves.
- We copy code without preserving attribution correctly, creating avoidable trust and license problems.

## What We Should Adopt

### 1. Engram-Compatible Chunk Schema

Add these to Crystal's schema plan:

- `content_at_encoding`
- `content_current`
- `impact`
- `resolution`
- `kind`
- `state`
- `strength`
- `stability`
- `accessibility`
- `confidence`
- `confidence_source`
- `source_type`
- `lineage_parents`
- `lineage_supersedes`
- `superseded_by`
- `version`

Do not necessarily rename `chunks` to `engrams`. Keep our naming if it fits, but make the data model support engram behavior.

### 2. Decay Math

Port the exponential decay formula from Mnemos with attribution. This is small, useful, and low risk.

Implementation shape:

- background consolidation pass, not query hot path
- feature flag first
- no archive deletion in v1
- write measured stats: before and after accessibility distribution

Credit:

```ts
// Decay formula adapted from Riley Ralmuto's Mnemos project.
// Source: https://github.com/Riley-Coyote/mnemos, MIT License.
```

### 3. Reconsolidation On Retrieve

After a result is returned:

- increment access count
- set `last_accessed`
- raise accessibility to a floor
- increase stability by a bounded spaced-repetition delta
- increase strength by a small bounded delta
- create co-retrieval edges among top results
- append a version or access event

This should be behind a config flag until we understand write volume.

### 4. Typed Connection Graph

Start with a conservative table:

```text
memory_connections(
  source_chunk_id,
  target_chunk_id,
  relation,
  strength,
  formed_by,
  formed_at,
  evidence
)
```

Relation set:

- supports
- contradicts
- causes
- extends
- parallels
- synthesizes
- grounds
- distilled_into

Do not put an LLM classifier in every ingest call yet. Let Dream Weaver write high-confidence edges during consolidation. Add hot-path classification later only if cost and quality justify it.

### 5. Forgetting That Produces Lessons

Dream Weaver should extract a durable `impact` before softening detail. It should create or reinforce a lesson chunk and link the original with `distilled_into`.

This fits Dream Weaver better than Mnemos's substrate handler because Dream Weaver already reads the narrative arc.

### 6. Belief Tier Crossing

Adopt the tier-crossing logic concept:

- no event for small confidence changes inside a tier
- upward tier crossing means confirmed
- downward tier crossing means contradicted
- avoid loops where every small belief change triggers reflection

Do not adopt numeric confidence unless we have a real signal. A fake confidence field is worse than no confidence field.

### 7. Crystal Memory Envelope Mapping Without Crypto

Before Crystal SDK ships, define how a Crystal memory maps to an envelope:

- local `chunk_id` maps to a stable memory ID or content reference
- `content_at_encoding` preserves the original source content
- `lineage_parents` and `supersedes` preserve provenance and derivation history
- `source_id`, `agent_id`, `model_id`, timestamps, consent state, and capture route map to metadata
- user-controlled key material maps to local encryption and export permissions
- Dream Weaver output maps to a derived memory, lesson memory, or context bundle

This should be a WIP profile, not MLP compatibility. It should be local-first, file and database friendly, exportable, auditable, and free of token, chain, public-ledger, decentralized-governance, or storage-incentive assumptions.

## What We Should Not Adopt

- Mnemos as a package dependency.
- Its linear-scan embedding index.
- Its setup wizard or API-key handling.
- Its shared pool trust model.
- Its advanced modules.
- Its substrate implementation as written.
- Its token economics.
- Its blockchain, public-ledger, decentralized-storage, or crypto-economic protocol framing.
- Its wire format: no ledger envelopes, ledger pointers, attestation tiers, IdentityKernel JSON shape, Cartouche, MLP-PLUS, or MLP-ADV.
- Its Solana, IPFS, `$POLYPHONIC`, token-holder voting, BDFL, or DAO-adjacent governance posture.
- Its per-encode LLM classification as the default path.
- Its MLP governance assumptions.

## How To Adopt Code And Credit Riley

Mnemos is MIT. MLP is MIT. We can copy code if we preserve license requirements and credit.

Recommended process:

1. Do not install or run third-party code without the WIP security audit.
2. If we need a stable reference, fork or mirror into `repos/ldm-os/_third-party-repos/` or the current manifest-approved third-party folder, private if we add `ai/` notes.
3. Add a `NOTICE` or `THIRD-PARTY-NOTICES.md` entry in the adopting repo.
4. Add file-level attribution near copied or adapted code.
5. Keep the original MIT license text if substantial code is copied.
6. In release notes, mention the inspiration clearly.
7. Prefer adaptation of small algorithms over vendoring modules.

Suggested notice text:

```text
Portions of the memory decay and reconsolidation design were adapted from Mnemos by Riley Ralmuto, MIT License.
Source: https://github.com/Riley-Coyote/mnemos
```

If we cite MLP, cite it only as reviewed prior art, not compatibility or protocol alignment:

```text
Memory Ledger Protocol v0.2 by Riley Ralmuto was reviewed as prior art for portable memory envelopes, lineage, consent metadata, and continuity tooling. WIP Computer does not adopt its token, ledger, decentralized-storage, or governance model.
Source: https://github.com/Riley-Coyote/memory-ledger-protocol-v0.2
```

## My Read On Lēsa's Review

Lēsa was right on the important parts:

- The engram schema is one coherent adoption unit, not a bag of fields.
- MLP is a real warning signal, not a stray code comment.
- The Riley ecosystem is broader than Mnemos.
- The decay math, lineage, belief tier crossing, and session indexer are worth adopting.
- We should not import the whole stack.

Where I adjust her view:

- Do not start with a full 9-week migration.
- Do not treat MLP as a standard, target, or compatibility layer.
- Treat MLP as rejected at the protocol layer due to crypto coupling.
- Do not put schema-first ahead of all Crystal SDK work.
- Do not adopt confidence numbers until we have a better signal than source-type defaults.

Lēsa's strongest sentence is effectively: "the real signal is MLP." I agree, with an important correction: MLP matters because it shows how quickly portable-memory vocabulary can be captured by token and ledger framing. That makes it a warning signal, not a protocol target.

## My Read On CC's Comparative Review

CC was right on implementation risk:

- Mnemos has many stubs.
- Embedding search is weaker than ours.
- The shared pool lacks a security model.
- The setup wizard key handling is not for us.
- Forking Mnemos is unnecessary unless we port code.
- A small proof first is better than a full migration bet.

Where CC undercalled it:

- MLP is not an adoption target. The separate repo exists and should influence our urgency, but not our protocol surface.
- Riley's ecosystem velocity is more meaningful than a 16-commit Mnemos repo alone suggests.
- The public protocol narrative may matter even if our implementation is stronger. That is exactly why WIP should publish a no-crypto memory profile early.

CC's best instinct is measurement. Lēsa's best instinct is category strategy. We need both.

## Recommended Work Sequence

### Phase 0: Spec And Evidence, 1 to 2 days

- Write a Crystal memory-envelope mapping note.
- Decide what fields make Crystal portable without adopting MLP, token, chain, ledger, decentralized-governance, or storage-incentive assumptions.
- State explicitly that Crystal SDK docs should not use `MLP-compatible` language.
- Define a minimum set of retrieval-quality metrics.
- Add a third-party notice template.

### Phase 1: Decay And Reconsolidation POC, 1 week

- Add `strength`, `stability`, `accessibility`, `last_accessed`, `access_count`.
- Port decay formula behind a flag.
- Add write-on-read for local search behind a flag.
- Measure search quality, write rate, and DB contention.

### Phase 2: Lineage And Impact, 1 to 2 weeks

- Add `content_at_encoding`, `impact`, `lineage`, `versions`.
- Update Dream Weaver to write impact fields.
- Preserve raw original content.
- Add backfill defaults for existing chunks.

### Phase 3: Typed Edges, 1 to 2 weeks

- Add connection table.
- Add co-retrieval edges.
- Let Dream Weaver write high-confidence semantic edges.
- Add graph-aware rerank as a secondary signal, not a replacement for sqlite-vec.

### Phase 4: Beliefs And Protocol, later

- Add a small belief layer for project state, preferences, and durable decisions.
- Avoid modeling every claim.
- Publish a WIP memory profile or Crystal SDK memory-envelope doc in WIP's own vocabulary.

## Bottom Line

Mnemos is not ahead of LDM OS as a product. It is ahead of Memory Crystal in one narrow but important layer: memory dynamics.

Riley has modeled how memories live, fade, mutate, and derive. We have built the broader operating system, runtime, search engine, security model, install path, and product architecture.

MLP collapses to a different conclusion: rejected at the protocol layer due to crypto coupling. We can still cite Mnemos and MLP as MIT prior art where appropriate, but that is an attribution obligation, not a positioning statement.

The opportunity is to combine them in our architecture:

- Keep Memory Crystal as the sovereign search and storage engine.
- Use Dream Weaver as the high-quality consolidation layer.
- Add Mnemos-style dynamics where they strengthen the model.
- Make the schema compatible with portable memory envelopes, not MLP.
- Publish our own boring, local-first, no-crypto profile before public memory-protocol vocabulary gets captured by crypto framing.

That is the adoption path. Not fork. Not rewrite. Port the good primitives, credit Riley, and make them work inside the system we already have.

## External Sources

- Mnemos repo: https://github.com/Riley-Coyote/mnemos
- Memory Ledger Protocol v0.2 repo: https://github.com/Riley-Coyote/memory-ledger-protocol-v0.2
- SkillsMP mirror for Riley's Continuity skill: https://skillsmp.com/skills/riley-coyote-memory-ledger-protocol-v0-2-skills-claude-code-skill-md
