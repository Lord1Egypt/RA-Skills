# Changelog

## 4.0.23 - 2026-04-27
- Added a real workspace internal hook `super-memori-session-start` that listens to OpenClaw's runtime `agent:bootstrap` event and runs the Super Memori startup self-check through a host-enforced path instead of relying only on startup instructions.
- Added a per-session ledger keyed by `sessionId` so the startup self-check runs once for each new session and does not re-run on ordinary continuation turns of the same session even if bootstrap context is rebuilt.
- Wired the hook through `hooks.internal.load.extraDirs` and `hooks.internal.entries.super-memori-session-start` in `/home/irtual/.openclaw/openclaw.json`.
- Injected a compact session-start report into bootstrap context for the first handled turn so the agent has machine-generated startup state instead of only an instruction contract.
- Advanced the active artifact line to unpublished `4.0.23` for truthful packaging/release surfaces after landing the enforceable per-session startup hardening line.

## 4.0.22 - 2026-04-27
- Added a startup self-check/self-heal surface at `./startup-self-check.sh` so OpenClaw startup flows can re-check health, perform a safe refresh/rebuild pass when the host is degraded, and confirm a real smoke query before trust.
- Enabled the official OpenClaw bundled `boot-md` hook via `openclaw hooks enable boot-md` and added workspace `BOOT.md` so gateway startup now triggers the Super Memori startup self-check and writes a machine-readable report to `memory/index-state/startup-self-check-last.json`.
- Hardened workspace startup guidance in `AGENTS.md` so new sessions explicitly re-run the same startup self-check before trusting memory freshness; this line does not claim a separately verified per-session OpenClaw hook beyond gateway startup + startup instructions.
- Extended packaging/release/test surfaces so `startup-self-check.sh` is now part of the package contract, release gate, and regression runner.
- Advanced the active artifact line to `4.0.22` instead of mutating the already-published `4.0.21` package in place, then published `4.0.22` to ClawHub after the final truthfulness pass.

## 4.0.21 - 2026-04-25
- Completed the user-requested 6-round alternating Dual Thinking rerun without subagents.
- Accepted a final weak-model clarity patch from the clean DeepSeek round-6 review: simplified the `references/release-status.md` stable-line interpretation so it now states what the active line means instead of embedding a long per-patch lineage sentence that duplicated `CHANGELOG.md`.
- Preserved the same release truth while reducing support-surface cognitive load for weak-model and human readers.
- Advanced release surfaces to `4.0.21` for the actual publish step, then published `4.0.21` to ClawHub after the completed 6-round alternating rerun.
- Runtime capability claims unchanged; this is a release-status clarity hardening patch.

## 4.0.20 - 2026-04-25
- Continued the same user-requested 6-round alternating Dual Thinking rerun from accepted `4.0.19` state without subagents.
- Repaired a weak-model validation regression introduced during the readability cleanup: the skill now exposes an explicit `## Execution` anchor above the executable OpenClaw host setup flow, preserving the validator-recognized execution surface without reviving the old empty phantom heading.
- Advanced release surfaces to unpublished `4.0.20` so the accepted post-`4.0.19` patch line remains publish-honest during the ongoing rerun.
- Runtime capability claims unchanged; this is a weak-model-validation / readability correction.

## 4.0.19 - 2026-04-25
- Continued the same user-requested 6-round alternating Dual Thinking rerun from accepted `4.0.18` state without subagents.
- Accepted a clean-failure release-gate hardening patch from the clean Qwen round-5 review: `validate-release.sh` now explicitly requires `references/release-status.md` before the Python sync block reads it, eliminating the last raw-traceback path for a mandatory release surface and preserving deterministic gate failures.
- Removed an empty `## Instructions` heading from `SKILL.md` so weak-model readers no longer encounter a phantom contract section with no content.
- Advanced release surfaces to unpublished `4.0.19` so the accepted post-`4.0.18` patch line remains publish-honest during the ongoing rerun.
- Runtime capability claims unchanged; this is a clean-failure / readability hardening patch.

## 4.0.18 - 2026-04-25
- Continued the same user-requested 6-round alternating Dual Thinking rerun from accepted `4.0.17` state without subagents.
- Accepted a contract-surface sync patch from the second DeepSeek challenge round: `SKILL.md` now documents all four maintenance-only entrypoints already required by the package contract (`audit-memory.sh`, `repair-memory.sh`, `list-promotion-candidates.sh`, `validate-release.sh`) and explicitly keeps them out of the normal weak-model command loop unless maintenance is requested.
- Closed the remaining contract-to-package mismatch where maintenance surfaces were present and release-gated but only partially described in the main skill contract.
- Advanced release surfaces to unpublished `4.0.18` so the accepted post-`4.0.17` patch line remains publish-honest during the ongoing rerun.
- Runtime capability claims unchanged; this is a contract-surface / weak-model-guardrail hardening patch.

## 4.0.17 - 2026-04-25
- Continued the same user-requested 6-round alternating Dual Thinking rerun from accepted `4.0.16` state without subagents.
- Accepted a current-date truth-hardening patch from the second Qwen challenge round: removed the stale version tag from the `RUNTIME CAPABILITY MATRIX` header in `SKILL.md`, eliminating an internal version-drift seam where weak models could encounter conflicting version labels inside the same live artifact.
- Hardened `validate-release.sh` against recurrence by rejecting stale version-tagged section headers in `SKILL.md` when they do not match `_meta.json`'s active version.
- Advanced release surfaces to unpublished `4.0.17` so the accepted post-`4.0.16` patch line remains publish-honest during the ongoing rerun.
- Runtime capability claims unchanged; this is a document-truth / release-gate hardening patch.

## 4.0.16 - 2026-04-25
- Continued the same user-requested 6-round alternating Dual Thinking rerun from accepted `4.0.15` state without subagents.
- Accepted a second release-gate completeness patch from the first DeepSeek challenge round: `validate-release.sh` now also enforces the maintenance-only package-root entrypoints (`audit-memory.sh`, `repair-memory.sh`, `list-promotion-candidates.sh`, `validate-release.sh`) and the publish-evidence files (`references/verification-evidence.md`, `references/reference-test-log.md`) already declared mandatory by `PACKAGING_CHECKLIST.md`.
- Closed the remaining checklist-vs-gate mismatch of the same class as round 1, so the executable release gate now covers the declared public entrypoints, maintenance entrypoints, support evidence files, package-root metadata files, regression runner, `scripts/`, and `references/`.
- Advanced release surfaces to unpublished `4.0.16` so the accepted post-`4.0.15` patch line remains publish-honest during the ongoing rerun.
- Runtime capability claims unchanged; this is a further release-gate / packaging-honesty hardening patch.

## 4.0.15 - 2026-04-25
- Continued the user-requested 6-round alternating Dual Thinking rerun from the already-published `4.0.14` baseline without subagents.
- Accepted a release-gate completeness patch from the first Qwen round: `validate-release.sh` now enforces the package-root artifacts already declared mandatory by `PACKAGING_CHECKLIST.md` (`SKILL.md`, `_meta.json`, `.clawhubignore`, `CHANGELOG.md`, `PACKAGING_CHECKLIST.md`, and the four public entrypoints), requires `scripts/` and `references/`, and blocks if `tests/regression/run-all.sh` is missing or not executable.
- Narrowed the publish-readiness seam between the declared checklist and the executable release gate by actually running `tests/regression/run-all.sh` inside `validate-release.sh`, so future regression additions cannot silently drift past the release gate.
- Fixed the first validation rollback from real evidence: the gate now requires `tests/regression/run-all.sh` to exist and invokes it via `bash` instead of demanding an executable bit, so the release gate matches the repository's real file mode rather than inventing a stronger packaging requirement.
- Advanced `_meta.json` and release surfaces to unpublished `4.0.15` so the post-`4.0.14` patch line does not falsely read as already published before the current rerun completes.
- Runtime capability claims unchanged; this is a release-gate / packaging-honesty hardening patch on top of published `4.0.14`.

## 4.0.14 - 2026-04-25
- Started a fresh user-requested 6-round alternating Dual Thinking rerun without subagents, using Qwen and DeepSeek as the consultant line.
- Accepted the first material hardening patch from that rerun: `validate-release.sh` now enforces release-surface sync against the canonical `_meta.json` version, blocking publish/readiness drift when `SKILL.md`, `CHANGELOG.md`, `references/release-status.md`, `references/verification-evidence.md`, or `references/reference-test-log.md` fall out of sync.
- Accepted a second narrow hardening patch from the rerun: `_meta.json.publishedAt` validation now permits only `null` (unpublished) or a positive integer (real publish timestamp), closing the old ambiguous-sentinel gap where `0` or other non-positive integers could slip through the release gate.
- Accepted a third hardening patch from the rerun: `validate-release.sh` no longer hardcodes the current machine path for `skill_root`; it now validates the current working tree, restoring honest portability for CI, alternate workspaces, and cross-host publish prep inside the intended workspace layout.
- Accepted a fourth narrow truth patch from the rerun: the release surfaces now explicitly document that `validate-release.sh --strict` is a workspace-coupled gate relying on sibling validator tooling under `../skill-creator-canonical/`, rather than pretending it is an isolated package-root check.
- Reset `_meta.json.publishedAt` to the unpublished sentinel for the new `4.0.14` line so the workspace would not falsely imply that this post-`4.0.13` artifact was already published before the real release.
- Published `4.0.14` to ClawHub (`k976efrtejgbwtarytvbw1hek985g6r9`) and synced local metadata/support surfaces to the real publish timestamp `2026-04-25T13:25:24Z` (`publishedAt=1777123524`).
- Runtime capability claims unchanged; this is a publish-honesty / validation-discipline hardening patch on top of `4.0.13`.

## 4.0.13 - 2026-04-25
- Continued the required Dual Thinking rerun from the accepted `4.0.12` state and synchronized the support/package truth surfaces for honest publish readiness.
- Updated the release-support references so they now describe the active `4.0.13` line instead of the older `4.0.10` line.
- Marked the intermediate `4.0.11` changelog block as unpublished work carried forward, so the changelog no longer reads like `4.0.11` shipped independently.
- Published `4.0.13` to ClawHub (`k971cr1q8rss1bxr71cp7hjncd85g7t8`) and synced local metadata to the actual publish timestamp.
- Runtime capability claims unchanged; this is a release-surface / evidence-surface truth-sync patch.

## 4.0.12 - 2026-04-25
- Continued the required Dual Thinking rerun from the accepted `4.0.11` state and landed one more narrow publish-honesty clarification rather than a structural rewrite.
- Added an explicit host-state qualification to `Host-state guidance`: a `WARN` host is still within the qualified `v4.0.12` baseline and does not by itself mean artifact instability, setup failure, or a publication blocker; it simply activates the degraded-mode routing contract.
- Advanced the active line to `4.0.12` because this accepted wording patch materially changed the published-facing contract surface.

## 4.0.11 - 2026-04-25 (unpublished — changes carried forward into `4.0.12` and later `4.0.13`)
- Re-ran Dual Thinking against the stable `4.0.10` baseline and accepted a weak-model/current-date hardening patch before the next consultant handoff.
- Added a one-pass **Weak-Model Decision Matrix** immediately after the OpenClaw quickstart so weak models can resolve `health-check` state, query exit codes, degraded routing, and write/index gating without multi-hop cross-referencing.
- Added a **Design Boundaries / Intentional Exclusions** section that explicitly justifies the four-command public surface and names the modern local-memory patterns this artifact intentionally rejects for safety and operator clarity: background auto-indexing as a public requirement, LLM-driven auto-consolidation into durable memory, and cloud/remote vector dependencies.
- Fixed post-bump truth surfaces for the new unpublished `4.0.11` line: corrected stale in-file version labels, added a direct precedence note telling weak models to read the decision matrix first, and reset `_meta.json.publishedAt` to the unpublished sentinel instead of falsely implying that `4.0.11` was already live.
- Runtime capability claims unchanged; this is a contract-sharpening / current-date-positioning patch release.

## 4.0.10 - 2026-04-25
- Re-ran Dual Thinking from a fresh baseline after tightening `dual-thinking` itself against continuity-summary substitution in fresh/recovery consultant sessions.
- Hardened weak-model degraded-state routing in `SKILL.md`: the OpenClaw quickstart now treats `health-check.sh --json` as the primary degraded-state authority and uses bash exit codes only as hard-stop gates.
- Clarified `query-memory.sh` exit handling so `exit 1` + `degraded=true` must be reported as a degraded miss, and `exit 2` results must be presented explicitly as degraded/partial rather than normal success.
- Tightened the pre-action gate so live inspection wins over any conflicting `applied` change-memory record before writes or maintenance continue.

## 4.0.9 - 2026-04-24
- Published `4.0.8`, then immediately detected a final truth-sync seam: the package/support surfaces still described the line as unpublished and still named `4.0.7` as latest published, which became false the moment the real ClawHub publish completed.
- Advanced to `4.0.9` instead of mutating the already-published `4.0.8` package in place.
- Updated `SKILL.md`, `_meta.json`, and release/support surfaces so the current published line is now described honestly after the real publish.
- Runtime capability claims unchanged; this is a post-publish truth-sync release only.

## 4.0.8 - 2026-04-24
- Re-ran a fresh 6-round alternating Dual Thinking pass requested by the user (Qwen rounds 1/3/5, DeepSeek rounds 2/4/6) starting from the published `4.0.7` baseline and preserving per-orchestrator session continuity.
- Fixed a real packaging-honesty regression before republish: restored the missing package-root `.clawhubignore`, reset `_meta.json.publishedAt` for the new unpublished line, and advanced the artifact line to `4.0.8` instead of mutating the already-published `4.0.7` package.
- Tightened the release path so the next publish is honest-by-construction: strict validation now matches the actual tree again, and package metadata no longer implies that the new line was already published.
- Added a compact **Canonical action routing** table to `SKILL.md` so weak models can resolve the normal query path, no-results handling, durable writes, index/repair work, and hard-stop `FAIL` cases from one summary surface before falling through to the detailed gates and exit-code tables.
- Runtime capability claims unchanged so far in this line; current work is release-surface hardening plus accepted weak-model/operator clarifications from the active 6-round review.

## 4.0.7 - 2026-04-22
- Second 6-round alternating Dual Thinking review (Qwen rounds 1/3/5, DeepSeek rounds 2/4/6) executed directly by the main session without subagents. Qwen required one lawful recovery session mid-series when its persistent chat continuity degraded (`chatUrl: null`, hung follow-up); recovery repasted the latest accepted artifact before continuing.
- Introduced a single **Degraded-State Response Catalog** (`D-WARN-GENERIC`, `D-WARN-WRITE-ROLLBACK`, `D-WARN-INDEX-STALE-ONLY`, `D-WARN-COMBINED`, `D-LOW-AUTHORITY`, `D-FAIL`) as the sole source of mandatory user-visible degraded strings and behavioral rules; the Health & Safety Gate, exit-code tables, and OpenClaw quickstart now cross-reference this catalog by ID instead of restating strings inline, removing the previous drift risk between Health & Safety Gate and the exit-code-1 combined-degraded notice.
- Reworked the file-edit / memorize pre-action gate from dense prose into an explicit numbered procedure with trigger scope, Health & Safety Gate routing per catalog ID, concrete rollback verification step, and mandatory STOP on `FAIL`.
- Flattened Operating Rule 4's nested `Exception:` clause into an explicit precedence chain that defers directly to `D-WARN-COMBINED` vs `D-WARN-GENERIC` instead of re-describing catalog logic.
- Added a positive memorization test to Operating Rule 7: memorize only when the lesson encodes a reusable decision rule, parameter set, or failure pattern predictably recurring across ≥2 sessions or contexts.
- Fixed a real exit-code / degraded-flag contradiction flagged by DeepSeek: exit code `0` now explicitly handles `degraded=true` by routing to the matching `D-WARN-*` catalog row via the Health & Safety Gate rather than claiming "stack healthy" unconditionally.
- Consolidated the top-of-document status cluster (previously `Current truth snapshot` + `Current host limitations` + `Current blocker classification`) into one `Current Release & Host State` block with `Artifact invariants` vs `Host-state guidance` subsections, and dropped the hard-coded stable-host snapshot claim so the document no longer goes stale when a later release uses a different validation host.
- Consolidated the four change-memory paragraphs (`Change-memory authority boundary`, `Change-memory truth`, `Minimal hot-change-buffer`, `Change-memory noise policy`) into two sections (`Change-Memory Authority & Scope` + `Change-Memory Noise Policy`).
- Added an explicit decision rule to Truth Precedence: live filesystem / service / package inspection is mandatory before writes, config changes, service restarts, or any action depending on exact current machine state, and whenever `./health-check.sh` returns `WARN` or `FAIL`; memory-tool outputs alone are sufficient only for read-only queries at `status=OK` with `degraded=false`.
- Updated the OpenClaw quickstart steps 3-4 to emit catalog IDs (`D-FAIL` / `D-WARN-*`) for parity with the rest of the document.
- Runtime capability claims unchanged: this is a documentation / weak-model contract hardening release on top of `4.0.6`.

## 4.0.6 - 2026-04-22
- Completed the required 6-round alternating Dual Thinking review using Qwen (rounds 1, 3, 5 with one lawful recovery session after Qwen continuity degraded) and DeepSeek (rounds 2, 4, 6), then converged honestly without inventing a larger runtime rewrite.
- Rejected an unnecessary runtime-schema expansion for recency-gap reporting after confirming the existing payload already exposes the freshness/authority fields needed for this line.
- Hardened weak-model/operator wording in `SKILL.md`: queue/backlog WARN negative results are now explicitly potentially incomplete; the exit-code-1 combined degraded notice is self-contained; the quickstart now defers to one authoritative trusted-field definition; Operating Rule 2 now explicitly includes per-result `match_authority`; and the pre-edit maintenance rule now points directly to `references/maintenance.md`.
- Trimmed the live `Current blocker classification` section down to active-state truth instead of release-engineering residue.
- Hardened active support surfaces so they no longer carry stale or future-stale release wording: `validate-equipped-host.sh` and `scripts/release-prep.sh` now describe the current active line generically.
- This release does not change runtime capability claims; it is a documentation/support-surface hardening follow-up to `4.0.5`.

## 4.0.5 - 2026-04-22
- Advanced the active artifact line from `4.0.4` to `4.0.5` because the published `4.0.4` package was missing the declared `.clawhubignore` surface even though the packaging checklist required it.
- Restored `.clawhubignore` to the package root and excluded transient/local state deterministically (`.clawhub/`, `__pycache__/`, `*.pyc`, `*.tmp`, `*.pending`, `*.lock`, `.index_state/`, `backups/`, full `reports/`, `reports/test-generated/`, and `tmp_round2_strict.txt`).
- Kept runtime capability claims unchanged: this is a packaging-hygiene republish fix, not a new semantic/runtime feature line.

## 4.0.4 - 2026-04-21
- Advanced the active artifact line from `4.0.3` to `4.0.4` because the final safe latency fix and release validation work happened after `4.0.3`, and publishing over an already-established stable line would be dishonest.
- Fixed the real semantic latency seam by keeping embeddings behind a local semantic daemon instead of cold-loading the model in each short-lived query subprocess, while confirming the daemon stays idle-safe (`/health` reported `idle_cpu_percent_of_total=0.0` during the release check).
- Confirmed warm-path query latency on the current host after the fix: `exact≈0.13s`, `semantic≈0.21s`, `hybrid≈0.22s`, `auto≈0.22s` on the final current-workspace hardening run, with the separate direct timing probe also showing semantic warm calls dropping from cold-start seconds to sub-second daemon-backed execution.
- Re-ran the hardening benchmark on the current workspace (`benchmarks/locomo/results/20260421T093801.239655Z`) and kept accuracy green: `answer_hit_at_1=1.0` / `answer_hit_at_5=1.0` for `auto`, `exact`, `semantic`, and `hybrid`, with `avg_ms` around `212–219 ms` for the semantic/hybrid/auto modes after the safe warm-path fix.
- Fixed one release-test flake in `tests/test_semantic_daemon_surface.py`: the daemon surface gate now asserts stable fast daemon-backed embedding behavior instead of the brittle strict inequality `t2 < t1`, which could fail spuriously when both calls land in the same timing bucket.
- Rebuilt lexical/vector state on the current workspace, cleared transient orphan-vector drift caused by overlapping maintenance/release passes, and finished with clean gates: `./index-memory.sh --full --rebuild-vectors --json` exit `0`, `./validate-release.sh --strict` exit `0`, `audit-memory.sh --json status=ok vector_state=ok`, and benchmark post-index health `OK`.

## 4.0.3 - 2026-04-21
- Advanced the active artifact line from `4.0.2` to `4.0.3` because ClawHub truth inspection showed that `4.0.2` already exists and this workspace now contains additional real changes beyond the earlier release-surface patch.
- Hardened the LoCoMo benchmark harness so staged benchmark conversations are written into canonical `memory/episodic/benchmark-locomo`, verified against the lexical index with a new stage-coverage gate, and documented accordingly.
- Added an expanded hardening benchmark dataset plus stage-coverage regression so benchmark failures now distinguish real retrieval weakness from corpus-staging mistakes.
- Hardened temporal / semantic rerank by passing the live query text into `temporal_relational_rerank()` and applying a small query-anchor bonus plus bootstrap-path penalty, improving top-1 ranking on the new hardening benchmark set without weakening lexical authority rules.
- Re-ran strict local release validation, full local regression tests, smoke benchmark, and expanded benchmark before publishing this new stable patch line.

## 4.0.2 - 2026-04-21
- Archived stale candidate-era maintenance and promotion references so the packaged artifact no longer mixes the active stable `4.0.1` line with pre-stable `4.0.0-candidate.23` guidance.
- Advanced the active artifact line to `4.0.2` instead of mutating the already-published `4.0.1` package in place after this post-publish documentation/release-surface fix.
- Reset local `_meta.json.publishedAt` to the unpublished sentinel before republish so package metadata does not imply that `4.0.2` was already live before the next real ClawHub publish.
- Added inherited-evidence bridge notes so `references/reference-test-log.md` and `references/verification-evidence.md` now identify the active packaged line as `4.0.2` while preserving the real equipped-host validation body captured for stable `4.0.1`.

## 4.0.1 - 2026-04-20
- Completed the equipped-host stable-readiness sequence with a clean `./validate-equipped-host.sh` exit and final stable verdict: `Host is fully equipped and v4.0.0 hybrid mode is operational.`
- Closed the last stable-gate validator seams instead of weakening the gate: tolerated only the exact transient step-1 `stale-vectors` rebuild path, read semantic freshness from the real `health-check.sh --json` schema, and hardened eval/release surfaces so heavy hybrid checks time out honestly instead of hanging the release path.
- Reconfirmed the stable host truth end-to-end: semantic retrieval active, vector state healthy, `health-check.sh --json` status `OK`, `audit-memory.sh --json` status `ok` with `vector_state=ok`, `skill_operational_memory.status=ok`, and `agent_change_memory.status=ok`.
- Intended stable promotion target was `4.0.0`, but ClawHub truth inspection showed that version was already occupied by an older historical stable artifact from 2026-04-09; published this validated stable state as `4.0.1` instead to preserve registry honesty.

## 4.0.0-candidate.27 - 2026-04-20
- Ran one more post-publish truth-sync pass and found a real metadata seam: local `_meta.json` still carried the older `candidate.25` `publishedAt` value even though ClawHub already reported `Latest: 4.0.0-candidate.26` and `Updated: 2026-04-20T14:14:23.919Z`.
- Synchronized `_meta.json` publish metadata to the real latest published state instead of leaving stale publish-truth in the package root.
- Advanced the active artifact line to `4.0.0-candidate.27` rather than silently mutating the already-published `candidate.26` line.
- Reconfirmed current host runtime cleanliness after the sync pass: health `ok`, audit `ok`, `skill_operational_memory.status=ok`, and `agent_change_memory.status=ok`.

## 4.0.0-candidate.26 - 2026-04-20
- Ran an additional hardening pass focused on the last real operational WARN tails rather than release-label polish.
- Fixed routine maintenance self-noise in `index-memory.sh` and `scripts/agent_change_memory.py`: successful low-risk reindex maintenance is now truthfully reconciled into one verified current durable change instead of accumulating endless `applied_but_unverified` duplicates.
- Added a dedicated reconciliation helper plus regression coverage so matched hot-buffer events are settled to verified/applied state and do not remain falsely interrupted or unverified after a successful maintenance pass.
- Refreshed live maintenance state after the patch; current host health now reports `skill_operational_memory.status=ok` and `agent_change_memory.status=ok` with `records=1`, `duplicates=[]`, `unverified=[]`, and `hot_interrupted=[]`.
- Re-ran targeted tests, strict release validation, regression suite, and an external DeepSeek sanity-check on the post-fix artifact; no new publish-blocking seam remained.
- Advanced the active artifact line to `4.0.0-candidate.26` for this validated post-publish hardening step instead of silently folding the fix into the already-published `candidate.25` tag.

## 4.0.0-candidate.25 - 2026-04-20
- Ran a fresh 6-round alternating Dual Thinking pass through ai-orchestrator (DeepSeek) and qwen-orchestrator (Qwen) starting from the already-published `4.0.0-candidate.24` baseline.
- Fixed a false semantic-health WARN in `health-check.sh`: the warning path now falls back from Qdrant `indexed_vectors_count` to `points_count` before claiming that no indexed vectors are present.
- Re-synchronized active support surfaces so current-line documentation no longer states that the current validation host is degraded/unbuilt when live validation shows semantic-ready execution; the earlier degraded claims are now explicitly historical snapshots.
- Advanced the active artifact line to `4.0.0-candidate.25` across `_meta.json`, `SKILL.md`, `references/release-status.md`, `references/verification-evidence.md`, and `references/reference-test-log.md` instead of silently reusing the already-published `candidate.24` tag for this post-publish fix.
- Candidate publication remains honest and host-truth-bound: stable `4.0.0` is still blocked pending the equipped-host readiness sequence, while current host state must still be taken from live health/audit output at use time.

## 4.0.0-candidate.24 - 2026-04-20
- Fixed `canonical_memory_files()` so ordinary daily notes in `memory/YYYY-MM-DD.md` are indexed as episodic memory instead of being silently skipped.
- Excluded non-canonical operational memory under `memory/semantic/skill-memory`, `memory/semantic/system-hygiene`, and `memory/semantic/agent-change-memory` from canonical indexing so maintenance refreshes do not make the canonical freshness checks immediately self-stale.
- Added the missing `.clawhubignore` file and excluded local review/runtime artifacts, bytecode caches, full `reports/`, and temporary validation leftovers from the published package.
- This release is still a candidate line; publish honesty remains host-scoped and live `health-check.sh --json` output remains the source of truth for freshness and semantic readiness.

## 4.0.0-candidate.23 - 2026-04-14
- Fresh 10-round alternating Dual Thinking rerun started from the already-published `4.0.0-candidate.21` baseline and accepted a real package-hygiene fix before continuing the confirmatory rounds.
- Tightened `.clawhubignore` so internal `reports/` review artifacts and the root temporary validator leftover `tmp_round2_strict.txt` no longer ship in the distributable ClawHub package payload.
- Synced the active artifact line to `4.0.0-candidate.23` across `_meta.json`, `SKILL.md`, `references/release-status.md`, `references/verification-evidence.md`, and `references/reference-test-log.md` instead of silently reusing the already-published `candidate.21` tag for this post-publish packaging fix.
- Updated `PACKAGING_CHECKLIST.md` so the exclusion contract explicitly covers full `reports/` review artifacts and root temporary validation leftovers.
- Strict local release validation still passes after the accepted rerun patch.

## 4.0.0-candidate.21 - 2026-04-14
- Fresh 10-round alternating Dual Thinking rerun started from the already-published `4.0.0-candidate.20` baseline and accepted a narrow support-surface truth fix before continuing the confirmatory rounds.
- Tightened `references/verification-evidence.md` so the current-host lexical-freshness line no longer hard-pins a stale `2026-04-12T14:24:01+0800` timestamp as if it were the active evidential anchor for the current line; it now points explicitly to the live `./health-check.sh --json` snapshot for the candidate line while preserving the true degraded state (`lexical_freshness.ok=false`).
- Advanced the active artifact line to `4.0.0-candidate.21` instead of silently reusing the already-published `candidate.20` tag for this post-publish support-surface fix.
- Synchronized current-line identity across `_meta.json`, `SKILL.md`, `references/release-status.md`, `references/verification-evidence.md`, and `references/reference-test-log.md` to `candidate.21` while leaving `.clawhub/origin.json` untouched as real prior-publication metadata for `candidate.20` until the next actual publish completes.
- Strict local release validation still passes after the accepted rerun patch.

## 4.0.0-candidate.20 - 2026-04-14
- Fresh 10-round alternating Dual Thinking rerun started from the already-published `4.0.0-candidate.19` baseline and accepted two additional publish-honesty fixes before republish.
- Fixed a live host-evidence drift in `references/verification-evidence.md`: the current host-observed block no longer falsely says `lexical freshness: working after refresh`; it now reports the real current host state that the lexical stack is operational but freshness is stale (`lexical_freshness.ok=false`, last indexed `2026-04-12T14:24:01+0800`).
- Corrected release-history semantics after that post-publish fix by advancing the active artifact line from `4.0.0-candidate.19` to `4.0.0-candidate.20` instead of silently reusing the already-published candidate tag.
- Synchronized current-line identity across `_meta.json`, `SKILL.md`, `references/release-status.md`, `references/verification-evidence.md`, and `references/reference-test-log.md` to the new `candidate.20` line while leaving `.clawhub/origin.json` untouched as real prior-publication metadata for `candidate.19`.
- Strict local release validation still passes after the accepted rerun patches.

## 4.0.0-candidate.19 - 2026-04-14
- Ran another fresh alternating Dual Thinking rerun with explicit current-date internet research pressure through ai-orchestrator (DeepSeek) and qwen-orchestrator (Qwen).
- Accepted one new runtime contract hardening from rounds 1-2:
  - added per-result `match_authority` plus top-level `authoritative_result_present` / `low_authority_only` signals so weak models can distinguish confirmed exact/hybrid memory from heuristic semantic/fallback matches without suppressing valid lexical truth
- Rejected a naive numeric confidence-floor proposal because this runtime's RRF/fusion scores are not globally calibrated and a hard cutoff would break the existing lexical-authority contract for exact/path matches.
- Added targeted regression coverage for the new authority surface and synced public command/skill contract wording to the new payload fields.
- Later rerun rounds 7-8 found one more real publish seam: active contract/reference surfaces still mixed `candidate.18` and `candidate.19` identity after the version bump. Fixed that release-truth drift by syncing `SKILL.md`, `release-status.md`, `verification-evidence.md`, and `reference-test-log.md` to `candidate.19` while preserving historical bridge notes and leaving `.clawhub/origin.json` untouched as real published `candidate.18` metadata.
- Removed one harmless duplicate `retrieval_stack_unavailable` assignment from `query-memory.sh` during the same sync pass.
- Candidate line remains `4.0.0-candidate.19` pending final convergence proof and publish.

## 4.0.0-candidate.18 - 2026-04-14
- Ran a brand-new full 10-round alternating Dual Thinking rerun from the published `4.0.0-candidate.17` baseline using ai-orchestrator (DeepSeek) and qwen-orchestrator (Qwen), with exact Qwen daemon-restart recovery applied when round 4 and round 6 hit `exit 2` / navigation-timeout continuity failures.
- Accepted two real runtime/test-alignment fixes from this rerun:
  - `audit_memory_integrity()` now classifies the zero-chunk / zero-vector degraded host state as `semantic-unbuilt` instead of `ok`, bringing runtime output back into line with the documented degraded-host contract and the strict semantic-unbuilt test
  - `build_hot_recovery_bundle()` now emits an explicit truth note that the hot buffer is not canonical truth and that direct live inspection plus durable change-memory remain stronger for exact current machine state, bringing runtime output back into line with the hot-buffer authority test and public contract
- After those two fixes, all remaining rounds were confirmatory only: DeepSeek rounds 3/5/7/9 and Qwen rounds 2/4/6/8/10 found no new material seam that justified another patch.
- Fresh strict validation now passes end-to-end on the post-fix baseline, and current health remains publish-compatible `WARN` for the already-documented host-scoped degraded reasons (`semantic-unbuilt`, stale lexical freshness) rather than any forbidden critical failure surface.
- Advanced the candidate line to `4.0.0-candidate.18` for this rerun-backed release.
- No public command expansion, no stable-release claim, no capability overstatement.

## 4.0.0-candidate.17 - 2026-04-14
- Ran another fresh 10-round alternating Dual Thinking rerun using ai-orchestrator (DeepSeek) and qwen-orchestrator (Qwen), including one lawful Qwen recovery chat after a polluted session repeated an already-fixed stale-version finding.
- Accepted four additional narrow, validated fixes during this rerun:
  - updated `ARCHIVE.md` from a stale `candidate.10` pointer to a frozen-history-only note that now defers generically to the current contract in `SKILL.md` and live release/reference surfaces
  - synchronized stale support-surface self-identification so `release-status.md`, `verification-evidence.md`, and `reference-test-log.md` now align to the live `candidate.17` line, while preserving a single explicit bridge note that the underlying evidence was captured at `candidate.12`
  - added an internal frozen-reference restatement inside the maintenance `Execution Notes` subsection so weak models cannot skim into the `<details>` block and misread it as active operating contract
  - removed the redundant secondary freshness-caution append path from the `query-memory.sh` exit-code `1` override when the exact combined degraded-state notice already governs, while still surfacing freshness notes from returned `warnings[]` outside that override
- DeepSeek confirmatory rounds 5, 7, and 9 found no new material seam after those accepted fixes.
- Qwen round 6 and round 10 both converged on confirmatory acceptance with no new material fix required; round 8 also found no new materially justified seam.
- Advanced the candidate line to `4.0.0-candidate.17` after the rerun-specific accepted fixes and fresh validation passed.
- No public command expansion, no stable-release claim, no capability overstatement.

## 4.0.0-candidate.16 - 2026-04-14
- Ran a fresh 10-round alternating Dual Thinking rerun with ai-orchestrator (DeepSeek) and qwen-orchestrator (Qwen), including honest recovery handling for Qwen daemon/session continuity failures and polluted repeat-finding chats.
- Accepted three real micro-fixes from this rerun:
  - synchronized stale lower-section `candidate.12` references so the live artifact no longer contradicts its own `candidate.15`/`candidate.16` release identity inside maintenance/reference sections
  - added explicit frozen-reference scoping for the maintenance `<details>` block and neutralized the highest-risk present-tense maintenance claims so weak models cannot misread them as live runtime truth
  - clarified in OpenClaw host setup that `qdrant-client` does not install or start the Qdrant database service, preventing weak operators from treating `pip install` as full semantic-stack readiness
- Rejected Qwen's later proposal to hard-restrict weak models to `--mode auto` only, because that would under-document real implemented semantic/hybrid capability and create a release-truth seam.
- Confirmatory DeepSeek/Qwen rounds converged with no further accepted material seam; remaining `Host profiles` weakness was judged optional fluff, not release-blocking.
- Advanced the candidate line to `4.0.0-candidate.16` after validation passed on the accepted artifact.
- No public command expansion, no stable-release claim, no capability under-reporting for convenience.

## 4.0.0-candidate.15 - 2026-04-13
- Fixed a real weak-model operator-risk seam in rule #4: forced semantic/hybrid fallback wording now explicitly yields to the combined degraded-state lexical-authority revocation rule when `index_fresh=false` (or `index_stale=true`) and semantic is unavailable together.
- Advanced the candidate line to `4.0.0-candidate.15` after this narrow contract fix.
- No public command expansion, no stable-release claim, no policy-gate overfitting.

## 4.0.0-candidate.13 - 2026-04-13
- Tightened release-truth wording so the packaged release line is explicitly separated from live host freshness, semantic readiness, and degraded authority state at use time.
- Reframed current-host degraded/stale wording as validation-host evidence instead of artifact-wide truth, reducing operator risk that a published version label is misread as a claim about every installed host.
- Tightened `validate-release.sh` so non-FAIL WARN publication is no longer an undifferentiated pass: release gating now explicitly blocks critical WARN surfaces such as unreadable canonical files or unavailable lexical FTS even if overall health is not `FAIL`.
- Synced `_meta.json` publish policy to the stronger host-scoped WARN interpretation and advanced the release line to `4.0.0-candidate.13`.
- No public command expansion, no stable-release claim, no forced freshness-window policy invented without stronger evidence.

## 4.0.0-candidate.12 - 2026-04-12
- Ran a fresh full 3-cycle / 18-round Dual Thinking rerun from the published `4.0.0-candidate.11` baseline using alternating AI Orchestrator and Qwen Orchestrator, including honest recovery handling for polluted Qwen sessions that repeated already-landed findings.
- Accepted three real micro-fixes from the new rerun:
  - in the combined stale-index + semantic-unavailable WARN state, degraded matches are now explicitly non-authoritative and lexical authority is revoked
  - removed the misleading `zero-findings` token from current-host `system_hygiene` wording so weak models cannot misread stale partial visibility as clean health
  - tightened the `query-memory.sh` exit code `1` no-results row so the combined stale-index + semantic-unavailable WARN state must reuse the exact degraded notice from the Health & Safety Gate rather than a weaker generic template
- Remaining Qwen suggestions about extra warning duplication or verbatim symmetry in other rows were reviewed and rejected as optional documentation polish, not material contract seams.
- Confirmatory rounds 10-18 produced clean convergence proof with no further accepted fixes.
- No public command expansion, no stable-release claim, no architecture rewrite.

## 4.0.0-candidate.11 - 2026-04-12
- Added an inline `OpenClaw quickstart for weak models` directly to `SKILL.md` so weak OpenClaw operators have a shortest safe path without cross-reading multiple files.
- Added an inline `OpenClaw host setup (weak-model executable)` section to `SKILL.md` with only real commands (`cd`, `python3 --version`, `pip3 install --user sentence-transformers numpy qdrant-client`, `./index-memory.sh --full --json`, `./health-check.sh --json`, `./query-memory.sh ...`).
- Added an explicit lowest-friction weak-model decision order: `health-check -> query(auto) -> read returned fields -> only then decide whether memorize or index is needed`.
- Retained the previously accepted weak-model honesty hardening: forced `semantic` / `hybrid` retrieval on unequipped hosts must be described through returned `mode_used`, `degraded`, and `semantic_ready` fields rather than overstated as semantic success.
- Retained the clarified hot-change-buffer durability wording (`RAM-resident`, `circular-buffer`, `non-durable`) and the synced WARN publish-qualification terminology.
- Final convergence result for the extended review scope: repeated DeepSeek/Qwen confirmatory rounds found no new material blocker after these weak-model/OpenClaw improvements.
- No runtime logic changes, no public command expansion, no stable-release claim.

## 4.0.0-candidate.10 - 2026-04-12
- Applied the accepted narrow SKILL.md wording cleanup for the hot-buffer truth line.
- Changed `very recent recovery-only recent changes` to `very recent recovery-only agent-made changes`.
- Narrowed the weak-model forced-mode contract so requested `semantic` / `hybrid` retrieval on an unequipped host must be reported via returned `mode_used`, `degraded`, and `semantic_ready` fields rather than being over-described as semantic success.
- Tightened the hot-change-buffer wording from `RAM-first, rotational` to `RAM-resident, circular-buffer, ... non-durable` to remove false durability implications.
- Synced WARN publish qualification terminology to the actual observed health-check shape (`lexical_freshness: ok=false`, `semantic_dependencies: ok=false`) instead of the older `: fail` shorthand.
- No runtime logic changes, no public command changes, no hot-buffer scope expansion.

## 4.0.0-candidate.9 - 2026-04-12
- Added a minimal safe-first Phase 1 internal hot-change-buffer for very recent agent-made changes.
- Buffer is RAM-first, rotational, recovery-only, non-canonical, aggressively noise-filtered, and bounded to a 32 MiB default target (64/128 MiB optional, 128 MiB max in this phase).
- Added only the minimal internal functions required for Phase 1: recent hot-event record/update/query, interrupted-sequence detection, recovery bundle assembly, compaction, and health reporting.
- Integrated the hot buffer into write/change logging, recent-change query routing, health reporting, minimal audit reporting, and maintenance compaction without adding any new public command.
- Added targeted Phase 1 eval coverage and passed strict release validation.

## 4.0.0-candidate.8 - 2026-04-12
- Completed the originally requested full review scope: 3 cycles total with 18 rounds of alternating Dual Thinking pressure-testing using AI Orchestrator and Qwen Orchestrator.
- Cycle 2 found and landed the last real post-`candidate.7` micro-fixes; cycle 3 then served as a clean no-new-issues convergence proof with 6 additional rounds and no new required changes.
- Moved `Change-memory truth` below `Change-memory authority boundary` to reduce weak-model reading-order risk.
- Changed weak-model rule #3 from `forced semantic/hybrid maintenance check` to `forced semantic/hybrid retrieval query` so normal forced retrieval does not get misclassified as maintenance.
- Normalized `system_hygiene` wording across `Current truth snapshot`, `Current host limitations`, and `Current blocker classification` to the clearer `zero-findings (stale state expected)` phrasing.
- Final campaign verdict after all 3 cycles: no remaining material seam in the skill artifact; release remains candidate, not stable.

## 4.0.0-candidate.7 - 2026-04-12
- Ran a strict 6-round Dual Thinking pressure test of the near-final candidate with alternating AI Orchestrator and Qwen Orchestrator, including one honest Qwen recovery round after session pollution repeated an already-fixed finding.
- Accepted only micro-fixes, with no public command expansion and no scope rewrite.
- Foregrounded current-host truth as `Current host execution mode: degraded lexical-only (semantic-unbuilt)` so weak models cannot miss that this host is still degraded.
- Disambiguated the maintenance note so it points directly to the Runtime Capability Matrix and Implemented-vs-Optional sections instead of the vague phrase `visible contract above`.
- Narrowed WARN continuation rules so read-only degraded queries do not require an invented rollback path, while write/maintenance continuations still require explicit rollback awareness.
- Anchored the stable-release checklist explicitly to equipped-host verification and clarified that unresolved `system_hygiene` status is separate from the non-blocking change-memory candidate classification.
- Replaced `file-derived fallback matches` with `degraded retrieval fallback matches` in the combined stale-index + semantic-unavailable WARN rule so fallback wording stays honest about the retrieval source.
- Final closure verdict for this candidate line: accept with micro-fixes landed; release remains candidate, not stable.

## 4.0.0-candidate.6 - 2026-04-12
- Prepared the next candidate release surface after the SKILL contract cleanup pass, without changing the public command surface or stable-release claim level.
- Release truth for this candidate is explicit: change-memory is implemented and live; change-audit integration is implemented and live; current host remains degraded / safe-first; `system_hygiene` remains stale / zero-findings on the current host; overall release remains candidate, not stable.
- Candidate-line documentation is now aligned around the cleaned current `SKILL.md` contract without introducing a new major refactor.

## 4.0.0-candidate.1 - 2026-04-12
- Published the current-generation local-only runtime as an explicit pre-release candidate so the stable `4.0.0` line remains reserved for the first equipped-host validation pass.
- This release contains the upgraded v4 runtime: local semantic spine, hybrid fusion, temporal-relational rerank, integrity audit, relation-aware writes, repair surface, telemetry, regression pack, release-prep, host-profile shaping, and stable-host readiness guidance.
- Host-state limitation remains explicit: this reference host is semantic-unbuilt, so the release is publish-honest as a candidate/pre-release, not as a stable full-hybrid tag.

## 4.0.0 - 2026-04-12
- Opened the new `4.0.0` candidate line because the runtime is no longer a lexical-first shell: local semantic indexing/search, hybrid fusion, temporal-relational rerank, integrity audit, and relation-aware learning writes now exist in code.
- Added a real local semantic spine: local embedding loading (`local_files_only=True`), semantic readiness/freshness, local Qdrant collection management, semantic rebuild, and semantic search.
- Added real hybrid quality logic: reciprocal-rank fusion, diversity control, temporal/recency shaping, source-confidence weighting, conflict-state handling, and relation-aware rerank pressure.
- Added integrity/audit surfaces: `audit-memory.sh`, `index-memory.sh --audit`, lexical/semantic drift detection, vector-state classification (`semantic-unbuilt`, `stale-vectors`, `orphan-vectors`), and stronger health visibility.
- Added relation-aware write/evolution paths: `memorize.sh` now records stable signatures, source-confidence, conflict status, canonical relation targets, and rejects new freeform relation labels.
- Reworked `mine-patterns.py` to cluster learning blocks instead of whole files and surface relation/conflict/review-status summaries for local memory evolution.
- Synced the skill contract to the new runtime truth: `semantic` and `hybrid` are real implemented modes, `auto` remains the default weak-model route, and release surfaces now distinguish implemented capability from host-state activation.
- Added host-profile shaping for `standard` vs `max` local operation without changing the weak-model public interface.
- Known candidate-line limitation: this host is still semantic-degraded because local embedding dependencies/model and built vectors are absent; the runtime reports that state honestly and does not overclaim semantic-ready operation.

## 3.4.9 - 2026-04-12
- Ran 6 additional full Dual Thinking cycles (36 planned rounds) on top of the published `3.4.8` baseline, using clean-room fresh consultant sessions from cycle 2 onward to reduce session-pollution repeats.
- Accepted only real post-`3.4.8` contract-clarity fixes that survived direct verification; rejected repeated, polluted, or code-false findings.
- Explicitly scoped direct `query-memory.sh --mode semantic` and `--mode hybrid` as compatibility/maintenance-only underlying CLI modes, keeping the active weak-model routing surface at `auto|exact|learning|recent`.
- Made `query-memory.sh` exit-code handling more self-contained and weak-model safe: exit `2` no longer borrows `health-check.sh` WARN semantics, and exit `1` now preserves freshness cautions when `warnings[]` still reports backlog/index-staleness conditions.
- Surfaced freshness-relevant warning categories directly in the visible contract so weak models do not need maintenance-fold context to apply the clean-miss caution rule.
- Tightened visible wording for literal accuracy on the historical lexical-first line before the later v4 candidate reclassification.
- Final closure outcome after the extra 6-cycle campaign: no remaining material blocker for the historical `v3.4.x` release line before the later v4 candidate reclassification.

## 3.4.8 - 2026-04-12
- Ran a fresh 6-round Dual Thinking review of `super-memori` with alternating AI Orchestrator and Qwen Orchestrator, including one honest Qwen recovery round after session pollution repeated an already-fixed finding.
- Added the missing public `memorize.sh` outcome contract and aligned it to real script behavior.
- Added explicit public `health-check.sh` and `index-memory.sh` exit-code handling for weak-model safety.
- Stabilized bad-arguments handling in `memorize.sh`, `health-check.sh`, and `index-memory.sh` so documented `4` paths are real rather than aspirational.
- Made `index-memory.sh` return exit code `2` when warnings are present, so degraded/partial maintenance runs are machine-visible.
- Tightened `query-memory.sh` exit-code `1` wording so weak models must inspect `degraded` first and frame degraded no-results honestly.
- Clarified that `index-memory.sh --rebuild-vectors` returning `2` on lexical-only hosts is an expected degraded outcome, not a hard failure.
- This release remains publish-compatible on a WARN host only because the skill explicitly documents lexical-first degraded operation and does not claim semantic-ready behavior on every host.

## 3.4.7 - 2026-04-11
- Applied the recovered Qwen round-4 documentation fix: replaced the stale `lexical_freshness=fail` phrase in `SKILL.md` with the actual query payload fields `index_stale=true` / `index_fresh=false`.
- Synced `references/verification-evidence.md` header to the accepted `3.4.7` state.

## 3.4.6 - 2026-04-11
- Tightened the new `query-memory.sh` exit-code contract after live validation exposed one more nuance: `exit 1` can occur on a degraded host when no results are returned.
- Clarified in both `SKILL.md` and `references/command-contracts.md` that weak models must inspect `degraded` and `warnings[]` alongside `exit 1` instead of assuming a fully healthy clean miss.

## 3.4.5 - 2026-04-11
- Continued the 6-round Dual Thinking rerun with a real consultant-backed fix from DeepSeek round 3.
- Added an explicit `query-memory.sh` exit-code interpretation table to the public `SKILL.md` contract so weak models can distinguish clean no-results (`1`) from a broken retrieval stack (`3`).
- Bound deterministic fallback handling to those exit-code rules instead of leaving post-command interpretation implicit.

## 3.4.4 - 2026-04-11
- Continued the 6-round Dual Thinking rerun with a real consultant-backed fix from Qwen round 2.
- Refactored `query-memory.sh` exit routing so documented codes are now honest: `4` bad arguments, `3` retrieval stack unavailable, `5` internal error, `2` only for degraded-but-usable results, `1` for clean no-results.
- Separated informational host-state warnings from real degraded execution, so `warnings[]` no longer automatically imply `degraded=true`.
- Version-locked verification evidence to `3.4.4` and replaced placeholder validation notes with concrete observed results.

## 3.4.3 - 2026-04-11
- Continued the 6-round Dual Thinking rerun with a real consultant-backed fix from DeepSeek round 1.
- Clarified that `--mode learning` is a lexical lookup over learning-memory entries in v3.x, not a separate semantic retrieval engine.
- Changed `query-memory.sh` so JSON output preserves `mode_used=learning` for learning-mode requests instead of collapsing them to `exact`.
- Synced the public skill contract and command-contract reference to that learning-mode reality.

## 3.4.2 - 2026-04-11
- Restarted Cycle 2 6-round Dual Thinking rerun from the published `v3.4.1` baseline under the corrected full-inline consultant method.
- Bound the worst-case double-degraded read path explicitly to degraded `query-memory.sh` surfaced fallback results instead of undefined direct file access.
- Aligned the mandatory double-degraded warning string across the Health & Safety Gate and command-contract surface.
- Added explicit structured-warning rule: mandatory degraded notices must live inside `warnings[]` in JSON mode rather than outside the payload.

## 3.4.1 - 2026-04-11
- Cycle 1 additional 6-round Dual Thinking rerun from the published `v3.4.0` baseline.
- Synced `references/command-contracts.md` to the actual `health-check.sh` implementation: real exit codes (`0/2/3/4/5`), required human-readable output contract, required JSON fields, and explicit weak-model interpretation rule.
- Rejected speculative escalations that relied on non-existent files or non-literal terms instead of the current artifact.

## 3.4.0 - 2026-04-11
- Ran a fresh Dual Thinking review cycle for `super-memori` with alternating AI Orchestrator and Qwen Orchestrator.
- Closed the runtime authority gap for the double-degraded WARN state: when lexical freshness is stale and semantic dependencies are unavailable at the same time, canonical markdown files are now the only authoritative source, and returned matches must be described as lexical / grep-derived file matches only.
- Clarified that `query-memory.sh --mode auto` remains valid on degraded hosts only as the script-selected degraded lexical path, not as an implicit guarantee of successful hybrid retrieval.
- Added the minimum honest ClawHub publish surface for this skill: `_meta.json`, `.clawhubignore`, `CHANGELOG.md`, `PACKAGING_CHECKLIST.md`, and release evidence files.
- Added explicit release-health policy: `FAIL` blocks publication, while `WARN` is publish-compatible only when it reflects documented optional/degraded host conditions and the release surface does not imply semantic-ready or fully healthy baseline. On this host, current `WARN` is due to stale lexical freshness plus unavailable semantic dependencies, which is documented degraded operation rather than a false healthy claim.
- Made the WARN publish exception deterministic in release evidence: qualification now records observed health-check state/fields (`WARN`, `lexical_freshness: fail`, `semantic_dependencies: fail`, no `FAIL`) instead of relying on free-text judgment alone.

## 3.3.3 - 2026-04-11
- Previous local release surface prepared during the same hardening pass; superseded by 3.4.0 after registry version collisions on 3.3.2 and 3.3.3, with no new semantic/runtime claim changes.

## 3.3.1 - 2026-04-09
- Added explicit degraded-mode prerequisite note for semantic / hybrid retrieval.
- Kept the public interface constrained to four commands for weak-model safety.
- Preserved lexical-first baseline with honest degraded-mode reporting when semantic retrieval is unavailable.
