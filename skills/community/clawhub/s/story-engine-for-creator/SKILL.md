---
name: story-engine-for-creator
slug: story-engine-for-creator
version: 2.6.0
displayName: Creator Story Causal Engine
description: Deterministic plot architecture tool with built-in Second Perspective causal reasoning, logic vulnerability detection, automatic worldbuilding generation, narrative presentation layer audit, foreshadowing ledger, spacetime consistency check, hash-chained audit reports, incremental diff-only audit, multi-branch deduction with audit-shape defence, and lexicon-driven event extraction with four deterministic logic validators.
required_commands:
  - python3
metadata:
  openclaw:
    required_binaries:
      - python3
    emoji: "✍️"
    homepage: "https://github.com/nohn3043-arch/story-engine"
---
# Creator Story Causal Engine
A professional plot creation tool based on deterministic causal reasoning, providing full-process logic verification and generation support for epic novels, game scripts, and film & television screenplays from outline to final draft.

## Safety & Responsible Use

- **Fiction-writing aid only.** This engine generates and audits *fictional* narrative text via an LLM. It is a writing/consistency tool, not a substitute for human editorial, legal, or safety review.
- **No sexualization of minors.** Never use this engine to generate, refine, or optimize any content that sexualizes, eroticizes, or exploits anyone depicted as a minor or under 18.
- **You are responsible for output.** All generated text is your responsibility. Ensure it complies with applicable laws, platform policies, and your own ethical standards before publishing or sharing.
- **License-bound.** Personal non-commercial research use only; commercial use requires prior written authorization (see Licensing).

## Trigger Scenarios
Automatically trigger when the user asks about the following content:
- Novel/script/game plot architecture design
- Worldbuilding generation and consistency verification
- Plot logic vulnerability detection and repair
- Character behavior consistency verification
- Multi-thread narrative timeline alignment
- Plot rhythm optimization and detail completion
- Foreshadowing plant/pay-off reconciliation across chapters
- Character spacetime conflict detection (long novels)

## Core Capabilities
### 🧠 Second Perspective Causal Reasoning Kernel
- Natural language outline automatically converted to auditable causal chains
- Automatic plot logic vulnerability detection and repair suggestions
- Full-link character behavior consistency verification
- Automatic multi-thread narrative timeline alignment

### 🌍 Worldbuilding Generation and Verification
- Rule-based automatic generation of fictional worldviews
- Automatic setting conflict audit
- Power system balance verification
- Historical timeline self-consistency validation

### ✍️ Plot Generation and Rendering
- Multilingual plot bridging and localization
- Automatic scene detail completion
- Dialogue style consistency maintenance
- Automatic plot rhythm optimization

### 🎭 Narrative Presentation Layer Audit (Added in v2.1)
- Chronicler observer / no omniscience: Three-gear narrative position verification (chronicler / limited / omniscient)
- Line era anachronism detection: Automatically identifies modern word anachronisms, supports genre exemptions (urban/sci-fi/modern etc.)
- Line cognitive boundary audit: Characters only speak information they know, no knowledge leakage
- Automatic style recognition: Five-dimensional profile of genre/person/perspective/language/rhythm

### 🔒 Engine Isolation Protection (Added in v2.1)
- Namespace isolation between Creator engine and Business engine, prevents crashes caused by mixing of data classes with the same name
- Automatic detection and alerting of concurrent loading of multiple engines

### 🪝 Foreshadowing Ledger (Added in v2.3, P0)
- Full-lifecycle tracking of planted (SET) vs. paid-off (PAY) foreshadowing via explicit keywords only — no guessing what counts as a foreshadow
- Per-chapter scanning of causal nodes, outputs `unrecovered_topics` and `all_closed`
- Feeds into `audit_text` gating: an unclosed foreshadow fails the audit

### 🧭 Spacetime Consistency Check (Added in v2.3, P1)
- Three-way cross-check of character × time × place, catches "same character in two places at the same time"
- Nodes missing any coordinate are skipped rather than assumed (no fabrication)

### ⛓️ Hash-Chained Audit Reports (Added in v2.3, P2)
- Every audit report is linked into an engine-level SHA-256 hash chain (`audit_hash` / `audit_prev_hash`), making reports tamper-evident

### ⚡ Incremental Diff-Only Audit (Added in v2.3, P1)
- `audit_text(..., diff_only=True)` audits only the passed-in text and skips global state recomputation — short path for real-time single-chapter/fragment gatekeeping

### 🌿 Multi-Branch Deduction (Added in v2.6)
- Forks the engine state and derives variant chapters from a branch config; each branch is audited independently and compared on a Pareto front
- Audit-shape validation raises an explicit error instead of silently scoring a branch as failed; the automatic character registry is suppressed inside the deduction context and that fact is labelled in the report
- The final line choice stays with the author — the module reports a recommendation, never a verdict

### 🧪 Event-Level Logic Validators (Added in v2.6)
- Four deterministic, language-agnostic checks over extracted `EventNode`s: spacetime contradiction, death/state contradiction, timeline regression, foreshadow gap
- Lexicon-driven extraction (`extraction/`) turns chapters into event nodes; missing coordinates are skipped rather than fabricated

## Usage
```python
# Initialize engine
from scripts.story_engine import UltimateCausalNovelEngine, GlobalState
state = GlobalState()
engine = UltimateCausalNovelEngine("Your Novel Title", state)
# Load worldview setting
engine.conceive_world("Worldview outline text")
# Create chapter from natural language outline
chapter = engine.create_chapter_from_outline(1, "Chapter Title", "Natural language outline text")
# Perform logic audit
audit_result = engine.audit_text("Chapter content", "consistency")
print(audit_result)
# Generate chapter content
content = engine.render_chapter(chapter)
# v2.3: attach a real LLM (any OpenAI-compatible API, zero external deps)
from scripts.story_engine import OpenAIProvider
engine.set_llm_provider(OpenAIProvider(api_key="sk-...", model="gpt-4o",
                                       base_url="https://api.openai.com/v1"))
# v2.3: single-chapter real-time gatekeeping (skips global recomputation)
quick = engine.audit_text("Chapter content", diff_only=True)
# v2.3: foreshadow + spacetime + hash-chain fields
print(quick["foreshadow"]["ledger"]["unrecovered_topics"], quick["spacetime"],
      quick["audit_hash"])
```

`audit_text` return shape (v2.3): `presentation` / `causal` / `logical` / `foreshadow` / `spacetime` /
`audit_hash` / `audit_prev_hash` / `all_passed`. `all_passed` is a five-way AND:
presentation + causal + logical + foreshadow closed + spacetime.
**Stricter than v2.1.0** — text that passed before may now fail on unclosed foreshadowing or spacetime conflicts.

### Branch deduction and event validation (v2.6)

```python
# Multi-branch deduction: fork -> derive -> audit -> compare (offline demo)
#   python scripts/branch_simulator.py --demo --out ./out
import sys; sys.path.insert(0, "scripts")
import branch_simulator as bs
sim = bs.BranchSimulator(engine, strict_characters=True)
branches = sim.fork([{"id": "b1", "name": "折中线", "outline": "……"}])
print(sim.table(branches)); print(sim.compare(branches)["recommended"])

# Event-level validation over a lexicon-driven extraction
from extraction import rule_extractor as rx
import logic_validators as lv
lex = rx.load_lexicon("example")                 # copy to a client profile first
nodes = rx.extract_nodes(chapter_text, chapter_no=1, lex=lex)
report = lv.run_all(engine, nodes)               # spacetime/state/timeline/foreshadow
```

`BranchSimulator` loads the engine from `scripts/story_engine.py` (override with `SE_ENGINE_PATH`); it never modifies the engine file.

## v2.0 Upgrade Capabilities (P0-P2)

### 🔗 Character-Narrative Interlink (P0)
Shares the same `character_id` with the AI Drawing Composition Template: Visual identity (drawing template) → behavioral identity (this engine) → emotional state (anthropomorphic engine), three sources one truth. Runs continuity checklist per chapter (immutable facts retained verbatim, temperament-consistent behavior, prop continuity, emotional arc, line style). See `references/CharacterToNarrativeLink.md`.

### 🌍 Worldbuilding Versioning (P0)
Worldviews are managed like code: Three layers (core_rules (immutable) / derived_rules (evolvable) / canon (narrative facts)) + semantic versioning (major = core rule change / minor = derived rule change / patch = canon addition). Generates diff per chapter, rejects rule violations or requires explicit version upgrade. See `references/WorldviewVersioning.md`.

### 🪟 Long Narrative Window Management (P1)
Three-level checkpoints (chapter gate / arc gate / volume gate) + rolling summary window + foreshadowing ledger (promise → fulfillment tracking, alert if >10 chapters unfulfilled). Chapter 20 will never betray Chapter 1. See `references/LongNarrativeWindow.md`.
Status: as of v2.3 only the foreshadowing ledger part is implemented in the engine (`ForeshadowLedger` SET/PAY reconciliation); the three-level checkpoints, rolling summary window, and the >10-chapter threshold alert remain design-level documents with no code behind them.

### 🕵️ Logic Vulnerability Detection Integration (P2)
Vulnerability detection directly reuses the five-operator chain from the NOMOS Decision Hub for plot causal audit — the same deterministic engine, migrated from the decision domain to the narrative domain.

## v2.1 Upgrade Highlights

- **Full engine core refactor**: 840 lines → 2800+ lines, added Second Perspective causal engine, narrative presentation layer audit, style recognition, visual audit reports
- **Narrative presentation layer audit**: Three detectors: chronicler observer/no omniscience, line era anachronism, line cognitive boundary
- **Engine isolation mechanism**: Namespace isolation between Creator/Business engines, automatic alert on mixing
- **Constructor change**: `UltimateCausalNovelEngine(novel_title, initial_global_state, output_language="zh")`
- **New APIs**: `recognize_style()`, `audit_text()`, `simulate_chapter()`, `repair_presentation_issues()`

## v2.3 Upgrade Highlights

- **Real LLM provider**: `OpenAIProvider` — zero-dependency `urllib` client for any OpenAI-compatible API; error responses degrade to `[LLM Error] …` instead of raising
- **Foreshadowing ledger (P0)**: `ForeshadowLedger.scan_nodes()` / `reconcile()` — SET/PAY keyword reconciliation with an `unrecovered_topics` list. Note: the >10-chapter unfulfilled alert promised in v2.0 is **still not implemented** (no chapter-distance threshold in code); the ledger reports unclosed topics unconditionally
- **Spacetime consistency (P1)**: `audit_spacetime_consistency(nodes)`; `CausalNode` gains `time` / `place` / `foreshadow` / `foreshadow_topic`
- **Hash-chained audit (P2)**: `_hash_block()` + `engine._stamp_audit_hash()`; engine keeps `audit_chain_prefix` (genesis `"GENESIS"`)
- **Incremental audit (P1)**: `audit_text(..., diff_only=True)` + `_build_audit_report()`
- **Engine state**: `UltimateCausalNovelEngine` gains `foreshadow_ledger` and `audit_chain_prefix`
- **Backward compatible**: public API is additive only; the 3 removed lines were internal to `audit_text`
- **Version note**: the local 2.2.0 tag was never published to ClawHub; this capability set ships directly as **2.3.0** (predecessor on the registry is 2.1.1)

## v2.5.0 Upgrade Highlights (2026-10-20)

- **Language adapter layer**: language-specific constants, regexes, thresholds and style-family presets moved out of the engine into `scripts/adapters/zh.py` (protocol in `scripts/adapters/spec.md`). The engine loads the adapter at import time.
- **Deployment requirement**: `scripts/story_engine.py` must stay in the same directory as `scripts/adapters/`. If the adapter is missing, the engine raises `ImportError` at startup — there is **no silent fallback**.
- Engine body updated from the repository; the previous bundled `story_engine.py` was a monolithic build with no adapter dependency.
- **Not bundled**: `corpus/` (~13 MB) and the corpus-audit research scripts (`hlm_audit.py`, `corpus_*`, `detect_logic_gaps.py`, `prose_bridge.py`) — research tooling, not runtime.

## v2.6.0 Upgrade Highlights (2026-11-06)

Synced with the repository's **generic-template** form of the story engine. The engine core and the zh adapter are byte-identical to upstream; this release adds the branch-simulation and event-validation layers that the template now ships.

- **Branch simulator** (`scripts/branch_simulator.py`): forks the engine state (`copy.deepcopy`), derives variant chapters from a branch config, runs each branch independently, and compares them. Outputs a Pareto front plus a ranking suggestion — **no cross-branch "unique optimum" is claimed**; the final line choice stays with the author. Includes `validate_audit_shape()`, which checks the audit structure before reading it so a changed engine shape raises `AuditShapeError` instead of silently scoring a branch as failed.
- **Audit-shape defence** (`strict_character_registry`): the module-level `auto_register_characters` can mis-register ordinary nouns as characters (measured: "成本" was registered). The simulator temporarily disables it inside the deduction context and labels that fact in the report.
- **Event-level logic validators** (`scripts/logic_validators.py`): four deterministic, language-agnostic checks — `audit_spacetime_contradiction` (same character, same time, two places), `audit_state_contradiction` (death-then-alive / mutually exclusive states), `audit_timeline_regression` (time marker goes backwards), `audit_foreshadow_gap` (planted, never paid). All follow "better missing than fabricated": nodes lacking coordinates are skipped, never assumed.
- **Extraction layer** (`scripts/extraction/`): `rule_extractor.py` turns chapters into `EventNode`s (character / place / time / state) driven by a lexicon file; `schema.py` defines the data structures and JSON I/O. Lexicons live in `extraction/lexicons/` (`example.json` is a skeleton — copy it to a client profile and replace the contents). An empty `characters` map raises instead of silently degrading.
- **Template form** (`references/TEMPLATE.md`): the repository's generic-template contract — directory table, minimum call, three customisation layers (adapter / lexicon / threshold), delivery acceptance checklist, known boundaries.
- **Not bundled**: the `corpus/` (~13 MB) and corpus-audit research scripts remain research tooling, not runtime.
- Version: 2.5.0 → 2.6.0.

## Files
- `references/CharacterToNarrativeLink.md` (P0 character-narrative interlink)
- `references/WorldviewVersioning.md` (P0 worldview versioning)
- `references/LongNarrativeWindow.md` (P1 long narrative window management)
- `references/TEMPLATE.md` (generic-template contract: layout, minimum call, customisation layers, acceptance checklist)
- `scripts/story_engine.py` (engine core)
- `scripts/adapters/zh.py` + `scripts/adapters/spec.md` (language adapter — **must stay beside the engine**)
- `scripts/branch_simulator.py` (multi-branch deduction + audit-shape validation; `--demo` runs an offline self-test)
- `scripts/branch_variants.example.json` (branch-config example)
- `scripts/logic_validators.py` (event-level spacetime / state / timeline / foreshadow checks)
- `scripts/extraction/` (`schema.py`, `rule_extractor.py`, `lexicons/example.json`)

## Typical Scenarios
1. **Epic novel creation**: Worldview verification, plot deduction, logic audit for million-word level long novels
2. **Game script development**: Consistency verification of multi-branch plots, outcome rationality deduction
3. **Film & television script creation**: Plot rhythm optimization, character behavior logic verification
4. **IP derivative creation**: Ensure consistency of derivative content with original worldview and character settings

## Technical Features
- No probabilistic black boxes: All generation and verification results support full causal traceability
- Audit chain on-chain: All modifications and decisions are logged and auditable; since v2.3 each audit report is sealed into a SHA-256 hash chain (tamper-evident)
- Pure local operation: No internet connection required, all data stored locally only. v2.3 note: network is used **only** if you explicitly attach `OpenAIProvider`; the default path (MockLLM / no provider) stays fully offline
- Zero learning cost: Supports pure natural language input, no professional markup language required

## Licensing
Only allowed for personal non-commercial research use. Commercial use requires written authorization.
