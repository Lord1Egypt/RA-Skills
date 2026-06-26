# Verification Evidence — super-memori 4.0.23

> **Evidence model:** `4.0.23` inherits the stable equipped-host validation evidence documented below from `4.0.1`, preserves the 2026-04-24 six-round hardening work, preserves the post-publish truth-sync captured in `4.0.9`, preserves the now-published `4.0.13` truth-sync line, preserves the published `4.0.14` release-surface sync-gate line, preserves the unpublished `4.0.15` release-gate completeness patch, preserves the unpublished `4.0.16` maintenance/evidence gate-completeness patch, preserves the unpublished `4.0.17` document-truth / stale-header guard patch, preserves the unpublished `4.0.18` maintenance-contract sync patch, preserves the unpublished `4.0.19` clean-failure / readability patch, preserves the unpublished `4.0.20` execution-anchor correction, preserves the published `4.0.21` release-status clarity correction, preserves the published `4.0.22` startup self-check/self-heal hardening line, and now adds the unpublished `4.0.23` enforceable per-session startup-hook line.

## Current line classification
- line: `4.0.23`
- evidence basis: inherited stable equipped-host validation from `4.0.1`, preserved `4.0.4` stable runtime evidence, preserved the `4.0.8` hardening work, preserved the `4.0.9` post-publish truth-sync release, preserved the now-published `4.0.13` line, preserved the published `4.0.14` line, preserved the unpublished `4.0.15` patch, preserved the unpublished `4.0.16` patch, preserved the unpublished `4.0.17` patch, preserved the unpublished `4.0.18` patch, preserved the unpublished `4.0.19` patch, preserved the unpublished `4.0.20` patch, preserved the published `4.0.21` patch, preserved the published `4.0.22` patch, and added the unpublished `4.0.23` enforceable per-session startup-hook line
- stable verdict: equipped host passed `./validate-equipped-host.sh` cleanly; stable promotion remains justified for the artifact family.
- reason: runtime architecture has crossed the lexical-first v3 boundary and now includes real local semantic indexing/search, hybrid fusion, temporal-relational rerank, integrity audit, and relation-aware learning writes
- frozen historical line: `3.4.9 release`
- current host state: host-dependent; read the live `./health-check.sh --json` snapshot for the active machine instead of inferring a degraded or semantic-ready state from this file alone
- publish state for this line: current published ClawHub line remains `4.0.22` as of `2026-04-27T04:23:28Z`; `4.0.23` is the current unpublished candidate line and `_meta.json.publishedAt=null` records that unpublished state.
- startup enforcement scope for this line: verified working startup self-check command, verified gateway-start execution path via `boot-md`, and now an actual per-session OpenClaw hook path via `agent:bootstrap` plus a `sessionId` ledger; this line does claim a real enforceable per-session startup hook on this host.

## Accepted structural upgrades in this line
1. Added a real local semantic runtime spine in code:
   - local embedding model loading with `local_files_only=True`
   - semantic readiness/freshness state
   - local Qdrant collection management
   - semantic index rebuild and semantic search
2. Added real hybrid quality logic:
   - reciprocal-rank fusion
   - diversity pass
   - temporal/recency shaping
   - source-confidence weighting
   - conflict-state handling
   - relation-aware rerank pressure
3. Added integrity/audit surfaces:
   - `audit-memory.sh`
   - `index-memory.sh --audit`
   - vector-state classification (`semantic-unbuilt`, `stale-vectors`, `orphan-vectors`)
   - stronger `health-check.sh` integrity visibility
4. Added relation-aware learning writes and evolution metadata:
   - stable signatures
   - `source_confidence`
   - `conflict_status`
   - canonical relation targets
   - rejection of new freeform relation labels
5. Reworked pattern mining from file-level noise toward block-level clustering with relation/conflict/review-status summaries.
6. Reclassified the skill contract and release surfaces onto an honest v4 candidate pre-release line.
7. Fresh 3-cycle / 18-round rerun from `4.0.0-candidate.11` accepted three additional micro-fixes:
   - explicit lexical-authority revocation in the combined stale-index + semantic-unavailable WARN state
   - full removal of the misleading `zero-findings` host-state token from current-host wording
   - explicit exit-code `1` override back to the exact Health & Safety Gate degraded notice for that same combined WARN state

## Historical validation snapshot (2026-04-12 / candidate.12)
- lexical index: working (`lexical_db` and `lexical_fts` were healthy on that validation host snapshot)
- lexical freshness: stale on that validation host snapshot (`lexical_freshness.ok=false`)
- semantic deps/model: missing on that validation host snapshot
- qdrant reachable: yes
- qdrant collection populated: no
- semantic vectors: absent
- semantic host state: degraded / unbuilt
- integrity audit: that validation snapshot reported `status=ok` with `vector_state=semantic-unbuilt`, no orphan chunk/vector drift, and no broken relations

Validation evidence was originally captured at `4.0.0-candidate.12`; the runtime contract later advanced through `4.0.1` without breaking capability regressions.

## Live validation snapshot (2026-04-20 / stable 4.0.1)
- lexical index: working (`lexical_db` and `lexical_fts` are healthy on the current validation host)
- lexical freshness: current (`lexical_freshness.ok=true`)
- semantic deps/model: ready on the current validation host
- qdrant reachable: yes
- qdrant collection populated: yes (`points_count=4`)
- semantic vectors: present (`semantic_vectors=4`)
- semantic host state: semantic-ready on the current validation host (`semantic_ready=true`)
- integrity audit: currently reports `status=ok` with `vector_state=ok`, no orphan chunk/vector drift, and no broken relations
- skill operational memory: currently reports `status=ok`, `stale_skills=[]`, `changed_skills=[]`
- agent change memory: currently reports `status=ok`, `records=1`, `duplicates=[]`, `unverified=[]`, `hot_interrupted=[]`

## Validation evidence recorded so far
### code syntax / runtime compile
Command:
- `python3 -m py_compile skills/super_memori/query-memory.sh skills/super_memori/index-memory.sh skills/super_memori/health-check.sh skills/super_memori/audit-memory.sh skills/super_memori/memorize.sh skills/super_memori/scripts/super_memori_common.py skills/super_memori/mine-patterns.py`
Observed result:
- no syntax failures

### temporal retrieval eval
Command:
- `python3 skills/super_memori/tests/test_temporal_retrieval.py`
Observed result:
- `[OK] temporal retrieval rerank cases passed`

### integrity audit surface
Command:
- `python3 skills/super_memori/audit-memory.sh --json`
Observed result:
- `status=warn`
- `vector_state=semantic-unbuilt`
- no orphan chunks
- no orphan FTS chunks
- missing vectors reported explicitly
- legacy non-canonical relation targets still flagged as broken relation residue

### host health surface
Command:
- `cd skills/super_memori && ./health-check.sh --json`
Observed result:
- `status=WARN`
- warnings reflect semantic host degradation and integrity drift visibility
- lexical DB / FTS healthy
- semantic-ready not claimed

### negative relation-target validation
Command:
- `cd skills/super_memori && ./memorize.sh --json --reviewed --refines semantic-spine "invalid relation target test" lesson`
Observed result:
- exit code `4`
- invalid freeform relation target rejected as intended

## 2026-04-21 hardening + latency validation snapshot (stable 4.0.4 inherited by 4.0.6)
- benchmark harness staging path: canonical `memory/episodic/benchmark-locomo`
- stage coverage gate: added earlier and still passing (`indexed_entries == stage_file_count` on the current benchmark runs)
- final current-workspace hardening benchmark: `benchmarks/locomo/results/20260421T093801.239655Z`
- current-workspace benchmark accuracy: `answer_hit_at_1=1.0`, `answer_hit_at_5=1.0` for `auto`, `exact`, `semantic`, and `hybrid`
- current-workspace benchmark latency: `exact=130.4 ms`, `semantic=212.6 ms`, `hybrid=217.2 ms`, `auto=219.2 ms` average
- direct timing probe on the current host: `exact [0.125, 0.124, 0.126]`, `semantic [10.612, 0.246, 0.205]`, `hybrid [0.207, 0.204, 0.234]`, `auto [0.209, 0.207, 0.205]`
- semantic daemon idle safety check: `/health` returned `200` and `{"pid": 40053, "idle_cpu_percent_of_total": 0.0}` during release verification
- current workspace release gate: `./validate-release.sh --strict` passes after a clean sequential lexical/vector refresh with `audit-memory.sh --json status=ok` and `vector_state=ok`

## Release honesty rule for this line
- The inherited stable validation basis for this line is the `4.0.1` equipped-host release, because an equipped host proved semantic-ready execution via `validate-equipped-host.sh` and the stable-host readiness sequence, and because `4.0.0` was already occupied in ClawHub by an older historical artifact.
- The `4.0.4` patch adds real benchmark/runtime latency hardening on top of the `4.0.3` benchmark harness work, so it is not described as a documentation-only republish; it carries fresh 2026-04-21 local validation plus the inherited equipped-host stable basis above.
- The `4.0.5` patch restored the missing `.clawhubignore` package surface that the packaging checklist already required, without changing runtime capability claims or pretending to add new semantic/runtime behavior.
- The `4.0.6` patch is also narrow: it hardens operator/support surfaces after the six-round 2026-04-22 review, without changing runtime capability claims or pretending to add new semantic/runtime behavior.
- The `4.0.8` line is narrow: it restores the missing `.clawhubignore`, advances version truth without mutating the already-published `4.0.7` line, resets `_meta.json.publishedAt` for the unpublished line, and re-synchronizes release/support surfaces without changing runtime capability claims.
- The `4.0.9` line is narrower still: it updates support surfaces and package metadata to match the real already-completed `4.0.8` publish, rather than leaving pre-publish wording in the post-publish artifact.
- `.clawhub/origin.json` remains local install/update metadata only; it is not publish evidence.
- Historical `3.x` remains historical only; it is no longer the current runtime truth.
- Stable publication remains host-truth-bound: current host readiness or degraded state on any future machine must still be taken from live command output, not inferred from historical evidence blocks in this file.
