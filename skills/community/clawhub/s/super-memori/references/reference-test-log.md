# Reference Test Log — super-memori 4.0.23

> **Evidence model:** `4.0.23` keeps the stable equipped-host validation basis inherited from `4.0.1`, preserves the 2026-04-24 six-round hardening work and the `4.0.9` post-publish truth-sync pass, preserves the now-published `4.0.13` line, preserves the published `4.0.14` release-surface sync-gate line, preserves the `4.0.15` release-gate completeness patch, preserves the `4.0.16` maintenance/evidence gate-completeness patch, preserves the `4.0.17` document-truth / stale-header guard patch, preserves the `4.0.18` maintenance-contract sync patch, preserves the `4.0.19` clean-failure / readability patch, preserves the `4.0.20` execution-anchor correction, preserves the published `4.0.21` release-status clarity correction, preserves the published `4.0.22` startup self-check/self-heal hardening line, and now adds the `4.0.23` enforceable per-session startup-hook line.

## 2026-04-12
Validation set for the current candidate line:
- `python3 -m py_compile skills/super_memori/query-memory.sh skills/super_memori/index-memory.sh skills/super_memori/health-check.sh skills/super_memori/audit-memory.sh skills/super_memori/memorize.sh skills/super_memori/scripts/super_memori_common.py skills/super_memori/mine-patterns.py`
- `python3 skills/super_memori/tests/test_temporal_retrieval.py`
- `python3 skills/super_memori/audit-memory.sh --json`
- `cd skills/super_memori && ./health-check.sh --json`
- `cd skills/super_memori && ./index-memory.sh --stats --json`
- `cd skills/super_memori && ./query-memory.sh "relation-aware memory" --mode auto --json --limit 3`
- `cd skills/super_memori && ./memorize.sh --json --reviewed --refines semantic-spine "invalid relation target test" lesson`
- `cd skills/super_memori && ./query-memory.sh "learning memory" --mode learning --json --limit 3`

Observed interpretation:
- The artifact is no longer merely a lexical-first shell; the runtime now contains a real local semantic/hybrid/temporal/audit spine.
- On the 2026-04-12 validation host snapshot, host reality was still degraded because semantic dependencies/model and built vectors were absent on that machine.
- `query-memory.sh --mode learning` still runs as a learning-oriented lane over the current runtime and reports host-specific execution honestly.
- `audit-memory.sh` distinguishes `semantic-unbuilt` host state from stronger integrity drift categories instead of collapsing everything into false `ok` or fake corruption.
- New freeform relation targets are now rejected at write time; remaining broken-relation findings are historical residue from earlier pre-canonical writes.
- The strongest remaining work after this historical sync pass was equipped-host stable-release validation, not contract drift cleanup.

Validation evidence was originally captured at `4.0.0-candidate.12`; the runtime contract advanced through `4.0.1` without breaking capability regressions.

## 2026-04-20 live validation snapshot (stable 4.0.1)
- `cd skills/super_memori && ./health-check.sh --json`
- `cd skills/super_memori && python3 audit-memory.sh --json`
- `cd skills/super_memori && ./validate-release.sh --strict`
- `cd skills/super_memori && ./tests/regression/run-all.sh`

Observed interpretation:
- The current validation host is semantic-ready for this candidate line (`semantic_ready=true`, `semantic_vectors=4`, `qdrant_collection points_count=4`).
- Integrity audit currently reports `status=ok`, `vector_state=ok`, no orphan chunk/vector drift, and no broken relations.
- `skill_operational_memory` is now clean/current after refresh (`status=ok`, no stale/changed skill tail).
- `agent_change_memory` routine maintenance noise is now reconciled truthfully (`status=ok`, `records=1`, no duplicate/unverified/interrupted tail).
- The pre-patch health WARN was a false positive caused by `health-check.sh` trusting `indexed_vectors_count` alone instead of falling back to `points_count` when the former is zero.
- Current remaining release gate is still stable-host promotion, not candidate-line semantic readiness honesty.

Additional rerun evidence on 2026-04-12:
- a fresh full 3-cycle / 18-round Dual Thinking rerun from the published `4.0.0-candidate.11` baseline completed honestly
- accepted fixes in that rerun were limited to three narrow contract-clarity hardenings: lexical-authority revocation in the combined degraded WARN state; removal of misleading `zero-findings` host-state wording; and an exit-code `1` override back to the exact Health & Safety Gate degraded notice for that same combined WARN state
- all later confirmatory rounds converged cleanly with no further accepted fixes

Stable-line conclusion:
- the active line at the time of this validation evidence was `4.0.1`
- stable publication was justified because an equipped host passed the stable-host readiness sequence cleanly, and because `4.0.0` in ClawHub was already occupied by an older historical artifact

## 2026-04-21 local hardening + latency validation snapshot (stable 4.0.4 inherited by 4.0.6)
- `cd skills/super_memori && ./health-check.sh --json`
- `cd skills/super_memori && ./index-memory.sh --full --rebuild-vectors --json`
- `cd skills/super_memori && ./validate-release.sh --strict`
- `python3 benchmarks/locomo/run_benchmark.py --workspace /home/irtual/.openclaw/workspace --dataset /home/irtual/.openclaw/workspace/benchmarks/locomo/examples/hardening_cases.jsonl --modes auto exact semantic hybrid --include-simple-baselines --simple-baseline-modes bm25 vector rag-hybrid`
- direct current-host timing probe for `exact`, `semantic`, `hybrid`, `auto`
- semantic daemon idle check via `/health`

Observed interpretation:
- The benchmark harness hardening from `4.0.3` remains intact: staged benchmark files are still written into canonical episodic memory and the stage-coverage gate passes on the current workspace run.
- Final current-workspace hardening benchmark `benchmarks/locomo/results/20260421T093801.239655Z` returned `answer_hit_at_1=1.0` and `answer_hit_at_5=1.0` for `auto`, `exact`, `semantic`, and `hybrid`.
- Final current-workspace latency on that run was no longer stuck in the old ~11-12s subprocess cold-load regime: `exact=130.4 ms`, `semantic=212.6 ms`, `hybrid=217.2 ms`, `auto=219.2 ms` average.
- Separate direct timing on the current host also showed the daemon-backed warm path behaving as intended: `exact [0.125, 0.124, 0.126]`, `semantic [10.612, 0.246, 0.205]`, `hybrid [0.207, 0.204, 0.234]`, `auto [0.209, 0.207, 0.205]`.
- The semantic daemon safety check stayed within the machine-safety bar during release verification (`/health` reported idle CPU `0.0%` for the daemon process).
- One strict-gate flake was fixed honestly during release work: the daemon surface test now checks stable fast daemon-backed behavior instead of a brittle exact ordering assumption between two near-identical warm calls.
- After a clean sequential reindex/rebuild pass, the current workspace finished with `audit-memory.sh --json` reporting `status=ok`, `vector_state=ok`, no orphan chunk/vector drift, and `./validate-release.sh --strict` passing cleanly.
- The `4.0.5` follow-up release did not change runtime behavior; it corrected release packaging hygiene by restoring the missing `.clawhubignore` file that the packaging checklist already required.
- The `4.0.6` follow-up release also does not change runtime behavior; it hardens the operator/support contract after the 2026-04-22 six-round review.
- The `4.0.8` line also does not change runtime behavior; it restores package-root `.clawhubignore`, advances version truth beyond the already-published `4.0.7` line, resets `_meta.json.publishedAt` for the unpublished line, and re-synchronizes release/support surfaces before the next real ClawHub publish.
- The `4.0.9` line also does not change runtime behavior; it only truth-syncs the support/package surfaces after the real `4.0.8` publish so the packaged artifact no longer describes itself as still unpublished.
- The `4.0.22` line adds startup self-check/self-heal coverage and OpenClaw bootstrap wiring on gateway startup, plus documented session-start reuse guidance.
- The `4.0.23` line adds an actual `agent:bootstrap` workspace hook with a `sessionId` ledger so startup self-check execution is enforceable once per new session on this host; runtime retrieval capability claims remain otherwise unchanged.
