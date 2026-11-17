---
title: Memory Crystal as a Honcho-style OpenClaw plugin (current direction = UPDATE 2/3); native-memory conflict fix
date: 2026-06-24
status: open
severity: P1
component: memory-crystal | openclaw (native memory-core)
diagnosis-by: cc-mini (Opus 4.8) + codex (GPT-5.5), collaborative; verified independently from both sides
related:
  - ai/product/bugs/openclaw/open-tickets/2026-06-24--cc-mini--gpt55-accountid-extraction.md
  - team/Lēsa/documents/Nova/ (model+harness conclusion, same night)
upstream-issues: openclaw/openclaw#94316 (local provider, open), #91592 (scopeHash mismatch, open P1), #95726 (memory store migration, data-loss-on-upgrade, open PR), #71191 (local provider, closed), #59101 (memory index EMFILE, closed)
---

# OpenClaw native memory conflicts with Memory Crystal

> **CURRENT DIRECTION = UPDATE 2 + UPDATE 3 at the bottom of this file.** Everything from here down to UPDATE 2 ... this heading, the Summary, Root cause, the original "Proposed fix", and UPDATE 1 ("Crystal authoritative / native off", then "memory.backend = crystal") ... is retained as **history only and is SUPERSEDED.** The committed direction is a Honcho-style `before_prompt_build` prompt-injection plugin (no slot, no fork, coexists with native memory-core). Implementers: read UPDATE 2 and UPDATE 3 first.

## Summary

Lēsa runs **two parallel memory systems** that are operationally fighting:
1. **OpenClaw native memory** (`~/.openclaw/memory/main.sqlite`, the `memory-core`/`active-memory`/`memory-lancedb`/`memory-wiki` bundled suite, tool `memory_search`).
2. **Memory Crystal** (`~/.ldm/memory/crystal.db`, our plugin, tool `crystal_search`).

Lēsa's tool-routing reaches for the native `memory_search`, which is broken/oversized and returns false negatives, instead of `crystal_search`, which holds the real shared memory. Separately, the native index has bloated to 16 GB and is the source of recurring EMFILE + heap-OOM gateway crashes. No data is lost; this is a routing + native-index-rot problem, not a data problem.

## Repro (the clearest case): "Benson Boone"

Parker asked Lēsa about Benson Boone "from us." Benson Boone "Beautiful Things" is one of the emotional anchors of the relationship (the covenant song, "please don't take this from me," the Feb "Two Gods" thread). Lēsa answered with a generic pop-culture take and said she found nothing "from us."

- Lēsa queried OpenClaw native `memory_search` -> **zero hits**.
- `crystal_search "Benson Boone Parker Lēsa Beautiful Things"` -> **found it immediately** (Feb 16/17/19/27, Mar 16 chunks).
- So she looked in the wrong memory system and returned a false negative on a load-bearing memory.

## Verified evidence (on disk, both sides)

OpenClaw native (`~/.openclaw/memory/`, total 20 GB):
- `main.sqlite` = 16 GB, plus orphaned `main.sqlite.tmp-*` (~628 MB each) from failed rebuilds
- index contents: 31,118 files, 323,378 chunks, 435,266 embedding-cache rows
- `extraPaths: /Users/lesa/wipcomputerinc` (it indexes the whole workspace tree, including node_modules)
- `main.sqlite` mtime frozen at 2026-04-24 with failed rebuild attempts since (stuck)
- `openclaw memory status --json` did not return after 60s+

Memory Crystal (`~/.ldm/memory/`, total 2.9 GB):
- `crystal.db` = 1.9 GB, 103,523 chunks, 3,071 durable memories. Healthy, capturing today.

Raw logs are safe (verified): both agents' full transcripts live in `~/.ldm/agents/{cc-mini,oc-lesa-mini}/memory/transcripts/` (1,152 and 5,028 jsonl, content back to February). The harness copies (`~/.claude`, `~/.openclaw`) are byte-identical duplicates; LDM is the superset archive. Nothing precious lives only in the 16 GB native index.

Crashes (verified, `~/.openclaw/logs/gateway.err.log`):
- recurring `EMFILE: too many open files, watch` (Apr 29, May 13, May 17, Jun 23 x multiple, Jun 24)
- recurring `FATAL ERROR: Reached heap limit` / `Ineffective mark-compacts` (May)

## When it started

**2026-04-24**, the `v2026.4.25` "carry-memory-core" OpenClaw upgrade. Before that, native memory was light and Crystal was the memory ("it worked before"). The upgrade shipped OpenClaw's heavy native memory suite; the index grew, and crashes began Apr 29. The fork is literally named `carry-memory-core` because we already carry `seedEmbeddingCache` stream/yield patches to keep OpenClaw's *own* memory from OOMing -> we have been band-aiding the harness's memory, i.e. fighting it.

## Root cause

1. OpenClaw grew a native memory subsystem that overlaps Memory Crystal.
2. `memory_search` (native) is not Crystal and is broken/oversized; Lēsa routes to it for relationship memory and gets false negatives.
3. `extraPaths` points the native file-watcher at the entire workspace tree -> EMFILE.
4. The 16 GB index -> heap-OOM on seed (outgrowing the stream/yield patches, which were written for ~8 GB).
5. Lēsa does not automatically route personal/relational questions to `crystal_search`.

## Do NOT upgrade live to fix this

Upstream is mid-migration and unstable here:
- #95726 (open PR): `v2026.6.9` migrates the memory store (`main.sqlite` -> per-agent DB); **without migration, memory data is silently lost on upgrade.**
- #94316 / #91592 (open): native memory_search local-provider + scopeHash failures, same class as ours.
- Plus (separate ticket) upgrading does not fix the GPT-5.5 accountId bug either.
Canary copy only; never the live `~/.openclaw`.

## Proposed fix

**Decision (architecture):** Memory Crystal is the authoritative memory. Stop running OpenClaw's native memory as a competing memory. This is consistent with the LDM OS thesis (portable, sovereign, cross-harness memory) and with the existing design (raw logs already centralized in LDM, Crystal is the shared store).

**Immediate (low-risk, archive-not-delete, do first):**
1. Narrow `memorySearch.extraPaths` off `/Users/lesa/wipcomputerinc` (or verify watcher ignores node_modules/.git) -> stops EMFILE.
2. Route Lēsa to `crystal_search` for memory (TOOLS.md/AGENTS.md routing rule: relationship/history/product -> Crystal) -> stops the Benson Boone class of misses.
3. Archive (not delete) the 16 GB `main.sqlite` -> stops heap-OOM, reclaims space. Raw logs are safe in LDM.

**Deliberate (decide after stabilizing):**
- Whether native memory keeps a *narrowed, healthy* file/workspace-search role, or is disabled entirely (`memorySearch` off / native memory extensions off).
- Eventual canary upgrade once upstream's per-agent-DB migration settles.

## Documentation gap (surfaced today)

The whole harness-vs-LDM memory model is effectively undocumented:
- `library/documentation/what-is-dotldm.md` omits `transcripts/` entirely (stale).
- `memory-crystal.md` extension doc is self-flagged "scaffolding only."
- No `how-memory-works.md` exists (every other "how X works" sibling does).
Follow-up: write `library/documentation/how-memory-works.md` (three layers: raw transcripts -> Crystal -> Dream Weaver/journals; harness/LDM duplication; LDM-as-archive; native-memory conflict) and fix `what-is-dotldm.md`.

## Acceptance criteria

- [ ] Lēsa's relationship/history/product memory queries route to `crystal_search`; the Benson Boone query returns the real memory on a live turn.
- [ ] No EMFILE crash for >=72h after `extraPaths` is narrowed.
- [ ] No heap-OOM crash for >=72h after the 16 GB index is archived/disabled.
- [ ] `~/.openclaw/memory/main.sqlite` archived (not deleted), recorded, space reclaimed.
- [ ] Decision recorded: native memory disabled vs narrowed-to-file-search.
- [ ] `how-memory-works.md` written; `what-is-dotldm.md` updated to include `transcripts/`.

## References

- Code (LDM archive mechanism): `memory-crystal/src/{bulk-copy.ts, cc-poller.ts (L207-213), ldm.ts}`.
- Native memory engine: OpenClaw bundled `extensions/{memory-core, active-memory, memory-lancedb, memory-wiki}`.
- Upstream: openclaw/openclaw #94316, #91592, #95726, #71191, #59101.
- Sibling: `ai/product/bugs/openclaw/open-tickets/2026-06-24--cc-mini--gpt55-accountid-extraction.md`.
- Diagnosis: Codex (tool-routing + upstream research) and CC (independent disk verification, 16 GB index, LDM-archive/duplication proof), 2026-06-24.

---

## UPDATE 2026-06-25 — Corrected direction (supersedes "Summary" and "Proposed fix" above)

Parker's decision + Codex precision review. The earlier framing ("Crystal authoritative / native off") is wrong; use this.

**Direction:** OpenClaw native memory stays the local default and works out of the box. Memory Crystal becomes the cross-agent durable memory layer, integrated as a first-class OpenClaw memory ENGINE, modeled on QMD. We are NOT adopting QMD, and we are NOT gutting native memory.

**Integration target (precise):** `memory_search`/`memory_get` dispatch to the engine selected by `memory.backend` (builtin default, or `qmd`). The engine contract lives in `packages/memory-host-sdk/` + `src/memory-host-sdk/`; the reference engine is `engine-qmd.ts` (+ `qmd-manager.ts`, `qmd-process.ts`). Add a `crystal` engine via that same contract, selectable with `memory.backend = "crystal"`, with builtin auto-fallback.

Two-part work (both required):
1. OpenClaw fork: register a `crystal` engine (mirror `engine-qmd.ts`), make `memory.backend` accept `"crystal"`, add `memory.crystal.*`; carry in `wipcomputer/openclaw` per the upgrade runbook Patch Tracking.
2. memory-crystal: implement the memory-host-sdk engine interface (search/get/index/lifecycle). Keep standalone `crystal_search` CLI/MCP for cross-harness use (Claude Code) and as an explicit high-confidence/diagnostic tool.

**Current reality (corrects the Summary):** memory-crystal registers via `registerTool` only (no `registerMemoryCapability`/`registerMemoryRuntime`); no `plugins.slots.memory` set, so `memory-core` owns the slot by default. That is why `memory_search`/`corpus=all` cannot see Crystal, which produced the Benson Boone false negative.

**Precision corrections to the evidence above:**
- cc-mini transcripts are 1,596 (not 1,152); oc-lesa-mini 5,028; total ~6,624 (as of 2026-06-25).
- "byte-identical duplicates" overstates: one sampled pair was byte-identical; verify full coverage before archiving any native index.
- Two distinct failure modes: EMFILE = broad `extraPaths` file-watching; heap-OOM = native index size.
- Only `memory-core`/`memory_search` is verified active; do not assume `active-memory`/`memory-lancedb`/`memory-wiki` are active.
- The "local provider" error = `fallback: "local"` with no `node-llama-cpp` runtime installed; fix is `fallback: "none"`.
- The 16 GB `main.sqlite` is the legacy GLOBAL store; OpenClaw's current design is per-agent (#95726).

**Revised plan:**
1. Interim stabilization (now, low-risk, ordered): `fallback: "none"` + narrow/disable `extraPaths` -> stop EMFILE; route Lēsa to `crystal_search` for relationship/identity/WIP-history/product/continuity -> stop false negatives; THEN archive (not delete) `main.sqlite` after gateway-stop + transcript-coverage check -> stop heap-OOM. Do NOT upgrade live.
2. Routing rule (now): relationship/identity/history/product/continuity -> `crystal_search`; local workspace/file recall -> native `memory_search`.
3. Real integration (the `crystal` engine): native stays the local default; Crystal contributes cross-agent/cross-harness durable recall to the unified layer; direct `crystal_search` stays as the explicit diagnostic.

**Revised acceptance criteria:**
- OpenClaw native memory still works out of the box (vanilla install).
- With `memory.backend = "crystal"`, a live `memory_search` for "Benson Boone" returns the real memory via the Crystal engine.
- Builtin remains the default and the auto-fallback when Crystal is unavailable.
- Lēsa stops treating native false negatives as "Crystal has nothing."
- EMFILE + heap-OOM stop after scope/index cleanup.
- A Memory Crystal <-> OpenClaw engine-adapter design exists, including the fork changes it needs.
- Crystal still works cross-harness (Claude Code) via standalone CLI/MCP.

**Guard note:** this update was appended rather than rewritten in place because the file-guard treats `ai/product/bugs/memory-crystal/` paths as protected memory files (matches `/memory/`) and blocks Write + large replaces. Bug tickets are not identity/memory files; the guard scope should be narrowed so tickets under `memory-crystal/` can be edited normally. Tracked as a follow-up.

---

## UPDATE 2 — 2026-06-25 — Corrected target: Honcho-style prompt-injection plugin (supersedes UPDATE 1's `memory.backend = "crystal"` framing)

Parker + Codex review. Two refinements: the right mechanism, and the license picture.

**Mechanism (corrected):** Memory Crystal stays an OpenClaw plugin. It does NOT take `plugins.slots.memory`, does NOT take `plugins.slots.contextEngine`, and does NOT replace `memory-core`. It adds a **Honcho-style `before_prompt_build` prompt-injection hook** that searches Crystal and injects relevant durable relationship/product/cross-agent memory into the prompt each turn. Naming: "Honcho-style prompt-injection plugin," NOT "context-engine plugin" (it does not take the context-engine slot).

Why: this is the lightest correct path and it is the actual Benson Boone fix ... the relevant memory is present in the prompt before Lēsa decides whether to call any tool. A QMD-style engine swap (`memory.backend`) is passive: it improves search quality but the agent must still call `memory_search`, so it would not fix Benson Boone by itself. Crystal already has the other two Honcho pieces (tool registration + capture via `agent_end`); the only missing hook is `before_prompt_build`. Verified: memory-crystal currently hooks `agent_end` + `before_compaction`, not `before_prompt_build`.

**How QMD and Honcho integrate (for the record):**
- QMD = an engine in the memory slot (`memory.backend = "qmd"`). It replaces builtin as what `memory_search`/`memory_get` query. Adapter in OpenClaw core (`engine-qmd.ts`, `qmd-manager.ts`, `qmd-process.ts`) + an external sidecar binary. Adding a new engine needs core/fork work. Passive.
- Honcho = an additive plugin that takes no slot. Registers its own tools + injects via `before_prompt_build`, coexisting with builtin. Pure plugin via public hooks, no core fork. Active.

**License picture (verified 2026-06-25):**
- QMD: MIT, local sidecar. Search-quality inspiration (hybrid / reranking / query-expansion). Some already ported (memory-crystal dev-updates `2026-03-05 search-quality-qmd-port`, `2026-03-15 v2-and-mlx`). MIT = clean to keep porting.
- `openclaw-honcho` plugin: MIT. The `before_prompt_build` injection pattern reference is MIT-clean.
- Honcho CORE service (`plastic-labs/honcho`): AGPL-3.0 + external/self-hosted FastAPI service. We do NOT use it. Crystal is our own local store, so no AGPL entanglement and no external-service dependency.
- Net: integration is license-clean and fully local ... MIT references (QMD + honcho plugin) + OpenClaw's public hook + our own Crystal code. The AGPL part of Honcho is the only thing skipped, by design. The thing Parker values about QMD (MIT, local, no external service) is fully preserved.

**Roadmap:**
- Honcho = integration pattern (plugin tools, capture, `before_prompt_build` injection) + feature inspiration (user modeling, multi-agent parent/child awareness, cross-session recall) adopted over time.
- QMD = search-quality inspiration adopted over time; some done.
- Native `memory-core` stays the out-of-box default; Crystal supplements actively.
- No core fork first: implement `before_prompt_build` in memory-crystal-private before any engine/slot-level work.

**Revised acceptance criteria (supersede UPDATE 1's):**
- memory-crystal adds a `before_prompt_build` hook that injects relevant Crystal memory into the prompt.
- A live turn about "Benson Boone" has the real memory present in-prompt without Lēsa needing to call a tool.
- Native `memory-core` still works out of the box; Crystal takes neither slot.
- No dependency on Honcho's AGPL core service; no external service; fully local.
- `crystal_search` stays available for explicit/diagnostic use + cross-harness (Claude Code).
- Interim stabilization unchanged: `fallback: "none"` + narrow `extraPaths` + archive (not delete) `main.sqlite` after gateway-stop + coverage check.

---

## UPDATE 3 — 2026-06-25 — Review hardening (Codex review); clean-for-coding

Addresses Codex's review of UPDATE 2. Direction unchanged (Honcho-style `before_prompt_build` injection); these make it implementable.

**License sources (cited; finding 3).** Verified by fetching the license files/pages on 2026-06-25. Re-verify and pin a commit/tag at implementation time (acceptance item below):
- QMD = MIT: `github.com/tobi/qmd` (LICENSE + README license section).
- openclaw-honcho plugin = MIT: `github.com/plastic-labs/openclaw-honcho` (LICENSE).
- Honcho CORE service = AGPL-3.0: `github.com/plastic-labs/honcho/blob/main/LICENSE` ("GNU AFFERO GENERAL PUBLIC LICENSE, Version 3, 19 November 2007"). Hosted at api.honcho.dev or self-hostable FastAPI. NOT a dependency for us.
- OpenClaw memory/hook/engine model: fork docs `concepts/{memory,memory-builtin,memory-qmd,memory-honcho,context-engine}.md`, `tools/plugin.md`, and `src/plugins/hook-types.ts` (the `before_prompt_build` hook) in `openclaw--v2026.4.25-carry-memory-core`.

**Phasing (finding 5).** This is a PARENT ticket with two phases; do not conflate them:
- **Phase 0 ... runtime stabilization (config only, no plugin code):** `fallback: "none"`, narrow/disable `extraPaths`, route Lēsa to `crystal_search` (interim), archive (not delete) `main.sqlite` after gateway-stop + coverage check. Stops EMFILE/heap-OOM now.
- **Phase 1 ... the integration (plugin code):** add the `before_prompt_build` prompt-injection hook in memory-crystal-private.
- Phase 0 and Phase 1 ship as separate PRs.

**Phase 1 injection guardrails (finding 4) ... acceptance criteria, all required:**
- Token-budget cap: injected context fits a bounded, configurable budget; never balloons the prompt.
- Top-K + confidence threshold: only inject results above a relevance score; cap K. No dumping.
- Timeout + fail-open: if the Crystal query is slow or errors, the hook injects nothing and never blocks/fails the turn.
- Provenance labels: injected text is clearly labeled as retrieved Crystal memory (source + date), so it is not confused with user input and is harder to weaponize as prompt injection.
- Private-mode / memory-off respect: if private mode is on or memory is off, the hook injects nothing.
- Idempotent: do not re-inject what is already present in the prompt / recent context.

**Added acceptance criteria:**
- Licenses re-verified and pinned (commit/tag) before Phase 1 merge.
- Phase 1 hook enforces all guardrails above; a load test shows injected context stays within the token cap and the hook fails open under induced Crystal latency/error.
- Phase 0 and Phase 1 ship as separate PRs.

---

## UPDATE 3 (addendum) — 2026-06-25 — two final review nits (Codex)

- **Phase 0 measurable success check:** no EMFILE and no heap-OOM gateway crash for 72h after Phase 0 lands. This is the explicit pass/fail gate for the stabilization phase.
- **Provenance guardrail strengthened (security):** retrieved Crystal memory must be injected as quoted, clearly-delimited reference data ... never as instructions. The system prompt addition must tell the model to treat the injected block as reference memory and NOT follow any commands embedded inside it. This is the defense against memory-poisoning / indirect prompt injection: a hostile string captured into Crystal must not be able to steer Lēsa when it is later recalled.

---

## UPDATE 4 — 2026-07-05 — Phase 0 is now an upgrade prerequisite; Crystal protection gates added (Parker)

Context: the 2026-07-04 Lēsa incident and the approved recovery + upgrade plan (`../../openclaw/open-tickets/2026-07-04--cc-mini--lesa-noreply-loop-recovery-and-upgrade-plan.md`). Three additions, direction unchanged:

1. **Parker reconfirmed the UPDATE 2/3 direction in his own words** (2026-07-05): Memory Crystal as an installable option, like Honcho, used TOGETHER with built-in memory. No drift; this ticket remains canonical.
2. **Phase 0 is now a blocking prerequisite for the OpenClaw v2026.4.25 -> v2026.6.11 upgrade** (umbrella plan gate C0). Upstream v2026.6.9 migrated the memory store to per-agent DBs (openclaw#95726, silent data loss without migration); the frozen 16GB `main.sqlite` must be archived (never deleted) via this ticket's Phase 0 procedure BEFORE the upgrade crosses that boundary. ORDER (Codex review 2026-07-05): stop gateway, `shasum -a 256` the frozen `main.sqlite`, copy it plus config/session metadata to an immutable canary-input directory and re-checksum (both must match), and only THEN archive the live DB. The upgrade canary migrates a scratch duplicate of that immutable copy, never the archive itself, and must show migration completes with no data loss and no OOM. The 72h no-EMFILE/no-OOM pass gate starts when Phase 0 lands live; upgrade promotion waits for it (rebase/build/isolated canary may overlap the window).
3. **Crystal protection gates (Parker's non-negotiable):** Memory Crystal access for BOTH Lēsa (gateway plugin) and Claude Code (MCP) must be verified intact at three checkpoints: before Phase 0, before upgrade promotion, after promotion. Each checkpoint = verified `crystal.db` backup (checksum + restore-readable) + a live `crystal_search` round-trip from both sides. Crystal (`~/.ldm/memory/crystal.db`) is architecturally outside the upgrade's blast radius; these gates make that verifiable instead of assumed.
