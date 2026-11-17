# Kaleidoscope — Wiki Layer (Future): LLM-Maintained Synthesis over Captured Memory

**Status:** Future-layer design note. Deliberately **NOT** part of `SPEC-v0.7.1-FROZEN` (freeze discipline: the frozen spec doesn't grow features). Phasing: post-search, roughly alongside/after Phase 4–5. Schema and page-format design belong to the **repo-aware agents** (Lēsa/Memory Crystal conventions live in the repos).
**Source pattern:** Karpathy's "LLM Wiki" (gist, Apr 2026) — an LLM incrementally builds and maintains a persistent, interlinked wiki over immutable raw sources, instead of RAG re-deriving knowledge per query.

---

## 1. Why it fits Kaleidoscope

The pattern's three layers map onto architecture Kaleidoscope already has:

| LLM Wiki pattern | Kaleidoscope (v0.7.1a) |
|---|---|
| Raw sources (immutable truth) | **Canonical event log + transcripts** (§7) |
| The wiki (LLM-owned, derived) | **← the missing middle layer this note adds** |
| Schema (maintenance contract) | **← Lēsa wiki-schema, repo-owned** |
| Search/index (derived, disposable) | **Embedding spaces + RRF** (§8) |

Today Kaleidoscope captures and *retrieves* conversations. The wiki layer *synthesizes* them: entity pages for recurring people/projects/concepts, "what I've decided about X," "open threads on Y" — a compounding knowledge base about the user's own thinking, maintained by Lēsa. This upgrades the product thesis from "your conversations, captured and searchable" to "your conversations, synthesized into a living memory."

## 2. The one architectural rule (do not get this wrong)

**The wiki is NOT a projection.** §7.5 of the frozen spec defines projections as *deterministic* functions of the event log. LLM synthesis is nondeterministic — calling the wiki a projection would quietly corrupt the category system that keeps the spec sound.

The wiki is a third class — a **curated derivation** — and it stays honest via one move:

> **Every wiki edit is itself recorded as a canonical event** (`wiki.page_updated` with the written content, `wiki.page_created`, `wiki.contradiction_flagged`, `wiki.contradiction_resolved`, `wiki.lint_completed` …), emitted by the Core like any `core.*` event.

This restores replayability at the right level: you cannot re-run the LLM and get the same wiki, but you **can replay the recorded edits** and reconstruct the wiki exactly. The wiki becomes auditable, rebuildable, and versioned through the same event log as everything else — and "who wrote this and from which conversations" is answerable for every page.

Resulting category system:
- **Canonical:** the event log (now including `wiki.*` edit events).
- **Deterministic projections:** transcripts, read model, conversation index — reproducible from log + code version.
- **Derived indexes:** embedding spaces — rebuildable by re-embedding.
- **Curated derivations:** wiki pages — rebuildable by replaying recorded `wiki.*` events; *regenerable* (fresh synthesis from transcripts) as a distinct, lossy operation.

## 3. Operations, mapped to the event model

- **Ingest:** on new `capture.turn_observed` acceptance, Lēsa reads the turn and integrates it — updating the 5–15 relevant pages, each update a `wiki.page_updated` event citing the source `event_id`s. Every wiki claim is **anchored to source turns** (the anti-drift rule: claims cite the immutable log, so hallucination can't quietly become ground truth).
- **Query:** answers read synthesized pages first, drill into cited source turns for receipts. **Good answers file back** as new pages (`wiki.page_created`) — explorations compound instead of evaporating into chat history.
- **Lint:** scheduled health pass — contradictions, stale claims superseded by newer conversations, orphan pages. Scoped to changed-pages + graph neighbors (not O(n²) full-repo); a periodic full sweep is cleanup, not primary defense.
- **Contradictions are first-class:** when a new conversation contradicts a page ("decided X" → later "X was wrong"), emit `wiki.contradiction_flagged` citing both source turns with timestamps — flag, don't silently overwrite. Resolution is its own event carrying the rationale.

## 4. Placement & properties

- Wiki pages live as markdown in the inspectable store (mirrored like transcripts), **opaque filenames**, user-readable, Obsidian-compatible if the user points a vault at the folder.
- Wiki maintenance runs **on-device** (Lēsa local) or via the user's chosen model tier — same plaintext-boundary rules as embedding (§8): sensitive streams' content never leaves device for synthesis without the same explicit opt-in.
- The **schema** (how to file, when to split a page, cross-reference conventions, contradiction severity rules) is the load-bearing config — co-evolved in the repos, versioned, referenced by `wiki.*` events so page history is interpretable.

## 5. Known risks (from the pattern's field reports)

- **Confident-but-stale synthesis** is the dominant long-run failure (field reports: ~day 60+). Mitigations: claim-anchoring to source events, staleness/lint passes, contradiction-flagging over overwriting.
- **Taxonomy drift** (Company vs company vs Organization): schema-governed page types; keep edge semantics minimal.
- **Token economics:** ingest touches many pages; scope reads via the index/read model, never whole-wiki scans.

## 6. Handoff

Repo-aware agents own: the Lēsa wiki-schema, page types/format, the `wiki.*` event-type additions to the canonical catalog (§10/§19.8 of the frozen spec), lint scoping rules, and reconciliation with whatever synthesis conventions Memory Crystal already has. This note is the pattern + the one architectural rule; the instantiation is theirs.
