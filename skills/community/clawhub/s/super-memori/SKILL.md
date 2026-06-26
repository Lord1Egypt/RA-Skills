---
name: super-memori
description: >
  Local-first hybrid memory skill for OpenClaw agents. Use when the agent needs to find, recall, search, or reuse past knowledge across
  episodic, semantic, procedural, and learning memory; when the user asks things like "what did we do about X", "remember", "find in memory",
  "что мы делали", or "найди в памяти"; when exact match and meaning-based recall both matter; or when designing, operating, or improving
  long-term agent memory on a local Ubuntu host. Includes manual-review learning improvement surfaces and memory-health guidance for degraded-mode detection,
  backup awareness before major operations, and risk-aware memory changes. Optimized for weak models by exposing a small command surface and clear degraded-mode rules.
---

# Super Memori — v4.0.23 Project Skill

**Release line:** `v4.0.23` unpublished current candidate line for the current-generation local-only memory runtime, advanced from the previously-published `v4.0.22` baseline with an enforceable per-session startup self-check hook for OpenClaw session start.

**Release-line truth boundary:** the release line identifies the packaged skill artifact, not the live freshness state of whatever host runs it later. Current host freshness, semantic readiness, degraded state, and authority limits must be read from live command outputs such as `./health-check.sh --json` and `./query-memory.sh ... --json` at use time, not inferred from the release label alone.

**Runtime prerequisites:** Semantic / hybrid retrieval is now implemented in the runtime, but it only becomes active on hosts where local semantic prerequisites are actually present: `sentence-transformers`, `numpy`, a locally available embedding model, local Qdrant, and vectors built from canonical files. Without them, the skill remains operational in lexical/degraded mode and surfaces that state explicitly.

**Status:** v4 local-only memory runtime with real lexical, semantic, hybrid, temporal-relational, audit, and change-memory machinery in code, plus maintenance-only learning improvement / pattern-mining surfaces. Host state still matters: a host can run this release in lexical-only/degraded mode if semantic prerequisites or vector build state are missing.

## Current Release & Host State

### Artifact invariants (v4.0.23)
- Lexical retrieval: active.
- Change-memory: implemented and live.
- Change-audit integration: implemented and live.
- Minimal hot-change-buffer: implemented, internal, recovery-only, non-canonical, non-durable.
- Semantic / hybrid / temporal-relational runtime: implemented in code, host-dependent activation.
- Destructive auto-actions: disabled by default.
- Overall release state: unpublished `4.0.23` built on top of the previously published baseline `4.0.22`.

### Host-state guidance
- Do not infer live host state from this document. Read `./health-check.sh --json` and `./query-memory.sh ... --json` at use time.
- Known host-scoped caveat: `system_hygiene` may surface as stale or partial-visibility on some hosts; treat that as host-scoped degraded evidence, not a clean-health signal and not an artifact-wide invariant.
- Blocking issues for the active `4.0.23` line: none currently known after the enforceable per-session startup-hook hardening pass on this host.
- Publish-readiness qualification: a host reporting `WARN` is still within the qualified `v4.0.23` baseline and does not by itself indicate artifact instability, setup failure, or a publication blocker; it only activates the degraded-mode routing contract defined below.

## Host profiles
- `current-degraded-host` — safe-first, degraded-aware, no destructive auto-actions by default.
- `equipped-stable-host` — stronger semantic / audit / index verification allowed, but still truth-tracked and rollback-aware.

## OpenClaw quickstart for weak models
If you need the shortest safe operating path under OpenClaw, use this order and do not improvise extra steps:
1. `cd ~/.openclaw/workspace/skills/super_memori`
2. `./health-check.sh --json`
3. Read the JSON `status` field first. If status is `FAIL` → stop (emit `D-FAIL`).
4. If status is `WARN` → continue only in degraded mode, applying the matching `D-WARN-*` catalog row from the JSON-qualified state rather than from exit code alone.
5. Treat the bash exit code from `health-check.sh` only as a hard-stop gate: exit `3`, `4`, or `5` = immediate stop/escalate; otherwise continue to JSON parsing.
6. For first query: `./query-memory.sh "<your query>" --mode auto --json`
7. Trust the exact field set defined in Operating Rule 2 below. Do not infer stronger capability than the payload states.
8. Use `./memorize.sh` only for reusable lessons.
9. Use `./index-memory.sh` only when the contract below tells you to refresh or repair freshness.

This quickstart does not guarantee semantic-ready operation on every host. It gives the strongest safe first path on OpenClaw while keeping degraded truth explicit.

## Weak-Model Decision Matrix
Use this matrix when a weak model needs one-pass routing instead of hopping between quickstart prose, degraded-state catalog rows, and multiple exit-code tables.

| Situation | Read first | Exact next action | Exact user-visible outcome |
|---|---|---|---|
| `health-check.sh --json` says `FAIL`, or bash exit is `3`/`4`/`5` | `status`, then exit code | Stop immediately. Do not query, memorize, or index. | Emit `D-FAIL` or the explicit argument/internal-error stop string. |
| `health-check.sh --json` says `WARN` | `status`, `warnings[]`, freshness fields | Continue only in degraded mode. Select the matching `D-WARN-*` row from the catalog before any query/write/index step. | Emit the matching degraded string. Add `D-WARN-WRITE-ROLLBACK` for writes/maintenance. |
| `health-check.sh --json` says `OK` | `status` | Normal path: run `./query-memory.sh --mode auto --json` for reads, or enter the pre-action gate for writes/maintenance. | No degraded warning required unless the later command payload says otherwise. |
| `query-memory.sh` exit `0` and `degraded=false` | exit code, `degraded`, `mode_used`, result fields | Use the returned results normally. | Normal success. |
| `query-memory.sh` exit `0` and `degraded=true` | exit code, `degraded`, `warnings[]`, freshness/authority fields | Use the returned results, but route through the matching `D-WARN-*` row first. | Degraded success, never normal success. |
| `query-memory.sh` exit `1` and `degraded=false` | exit code, `degraded` | Report a clean miss. Do not escalate. | `No memory entries found for this query.` |
| `query-memory.sh` exit `1` and `degraded=true` | exit code, `degraded`, `warnings[]` | Report a degraded miss, then apply the matching `D-WARN-*` row. | `No memory entries found for this query (degraded retrieval; results may be incomplete).` plus the matching degraded warning. |
| `query-memory.sh` exit `2` | exit code, `degraded`, `warnings[]`, authority fields | Present returned results only as degraded/partial, then apply the matching `D-WARN-*` row. | Degraded partial-result response, never clean success. |
| `query-memory.sh` exit `3`/`4`/`5` | exit code | Stop and escalate. | Emit the explicit unavailable / argument / internal-error stop string. |
| Need `memorize.sh` or `index-memory.sh` | latest health state + rollback state | Run the pre-action gate first. If rollback is unclear, stop. | For WARN writes/maintenance, append `D-WARN-WRITE-ROLLBACK`. |
| Request does not map to the four public commands | command mapping | Stop and ask for an in-scope command or human maintenance. | Emit the deterministic fallback line. |

Priority rules:
1. `health-check.sh --json` `status` is the primary gate; bash exit code is only a hard-stop override.
2. For degraded routing, `D-WARN-COMBINED` beats `D-WARN-INDEX-STALE-ONLY`, which beats `D-WARN-GENERIC`.
3. `D-LOW-AUTHORITY` can apply on top of `OK` or `WARN` whenever the returned authority fields require it.
4. Never describe a degraded lexical fallback as semantic or hybrid retrieval.

## Execution

### OpenClaw host setup (weak-model executable)
Use this only when preparing `super-memori` on an OpenClaw host for first use or when rebuilding local prerequisites. Execute the steps in order.

### 1. Enter the skill directory
```bash
cd ~/.openclaw/workspace/skills/super_memori
```

### 2. Confirm Python is available
```bash
python3 --version
```
Expected: Python is installed and callable as `python3`.

### 3. Optional: install semantic prerequisites for fuller local capability
```bash
pip3 install --user sentence-transformers numpy qdrant-client
```
Note: this installs only the Python client library; it does not install or start the Qdrant database service. Vector search will remain inactive until a reachable local Qdrant service is running and accessible.
If this step fails, the skill can still run in degraded lexical-only mode and will report that state honestly.

### 4. Build or refresh local indexes
```bash
./index-memory.sh --full --json
```
If semantic prerequisites are still unavailable, this may complete in degraded mode. Report that honestly; do not pretend semantic readiness.

### 5. Verify host health
```bash
./health-check.sh --json
```
Expected result:
- `OK` = normal operation
- `WARN` = degraded but usable operation
- `FAIL` = stop and escalate to maintenance

### 6. Run a first real query
```bash
./query-memory.sh "test query" --mode auto --json --limit 3
```
Confirm that the output includes at least `mode_used`, `degraded`, `warnings`, and `results`.

### 7. Return to the normal operating contract
After setup, follow only the four public commands and the `FOR ALL MODELS — REQUIRED OPERATING CONTRACT` below.

## Change-Memory Authority & Scope
- Change-memory records are operational truth about agent-made changes. Structured records distinguish `applied`, `failed`, `reverted`, and `unverified` states, and support current-known-state + recall-bundle retrieval. `reverted` or `unverified` records must not be presented as active current state.
- A minimal internal hot-change-buffer may hold very recent recovery-only state for recent agent-made changes. It is internal-only (no public command), RAM-resident, circular, non-canonical, non-durable, and aggressively noise-filtered.
- Neither durable change-memory nor the hot-change-buffer replaces direct live filesystem / service / package inspection when exact current machine state is required.
- Destructive auto-actions remain disabled by default.

## Change-Memory Noise Policy
- Do not log harmless reads as change-memory.
- Log only state-changing actions, failed writes, risky cleanup, package/service/config/runtime changes, and rollback events.

## Truth precedence
### For current machine state
1. Canonical files and direct live inspection
2. Lexical index
3. Semantic / vector index when healthy
4. Learning memory
5. Inferred recall last

### For agent-made change history
1. Change-memory records
2. Change-audit integration
3. Canonical files that directly confirm the current result
4. Inferred recall last

### Decision rule for live inspection
Live filesystem / service / package inspection is **mandatory** before writes, config changes, service restarts, or any action that depends on exact current machine state, and whenever `./health-check.sh` returns `WARN` or `FAIL`. Memory-tool outputs are sufficient on their own only for read-only queries when `status=OK` and the returned payload has `degraded=false`.

Never let inferred, stale, degraded, or retrieval-only surfaces override canonical truth.

## RUNTIME CAPABILITY MATRIX

| Capability | Implementation status | Host requirement |
|---|---|---|
| Lexical search (SQLite FTS5) | **Implemented** | Always available |
| Learning-memory retrieval | **Implemented** | Always available |
| Semantic embeddings | **Implemented** | `sentence-transformers` + `numpy` + local model files |
| Vector search (Qdrant local) | **Implemented** | Local Qdrant reachable + vectors built |
| Hybrid fusion (RRF) | **Implemented** | Semantic stack ready |
| Temporal / relation-aware rerank | **Implemented** | Semantic or temporal rerank path selected |
| Integrity audit | **Implemented** | Local lexical DB available |
| Pattern mining (block-level) | **Implemented** | `.learnings` populated |
| Change-memory records | **Implemented** | Always available |
| Change-audit integration | **Implemented** | Always available |
| Optional semantic-ready host state | **Optional host capability** | Semantic deps + local model + vectors built |

## IMPLEMENTED VS OPTIONAL VS HOST-STATE TRUTH
- **Implemented now in code:** lexical search, semantic search, hybrid fusion, temporal-relational rerank, integrity audit, relation-aware write metadata, block-level pattern mining, change-memory capture, change-audit integration, and a minimal internal recovery-only non-canonical non-durable hot-change-buffer.
- **Optional host state:** semantic embeddings, vector search, and hybrid selection only activate when local semantic dependencies/model/vector state are actually ready.
- **Not implemented / not claimed:** cloud backends, remote embeddings endpoints, remote vector DB, auto-promotion into durable memory, internet-dependent memory runtime, destructive auto-actions by default.

## Design Boundaries / Intentional Exclusions
This skill is intentionally strong-by-constraint rather than feature-maximal.
- It keeps a four-command public surface because weak OpenClaw models are more reliable when command choice, degraded routing, and rollback expectations fit in one short loop.
- It rejects background auto-indexing and always-on memory daemons as public operating requirements because they hide freshness state, blur operator intent, and make degraded/rollback truth harder to surface cleanly on local hosts.
- It rejects LLM-driven auto-consolidation or automatic promotion into durable memory because reusable lessons must remain operator-auditable and reversible.
- It rejects cloud sync, hosted embeddings, and remote vector backends because this artifact is optimized for local-first OpenClaw deployment, local privacy, and host-truthful failure handling.
- It prefers explicit host-state checks over ambient automation: current freshness, semantic readiness, and authority must come from live payloads, not from assumptions that a background subsystem stayed healthy.

## FOR ALL MODELS — REQUIRED OPERATING CONTRACT

### Public commands
- `./query-memory.sh`
- `./memorize.sh`
- `./index-memory.sh`
- `./health-check.sh`

### Maintenance-only entrypoints
These are maintenance-only surfaces. Do not add them to the normal weak-model command loop unless maintenance is explicitly requested.
- `./audit-memory.sh` — human/maintenance integrity audit surface.
- `./repair-memory.sh` — human/maintenance repair planner/executor surface for controlled memory repair work.
- `./list-promotion-candidates.sh` — human/maintenance review surface for candidate promotion workflow.
- `./validate-release.sh` — human/maintenance release-surface verification gate; not a normal runtime memory command.
- `./startup-self-check.sh` — startup-only health gate and safe self-heal surface for OpenClaw bootstrap/BOOT.md flows.
- `hooks/super-memori-session-start/` — enforceable per-session startup hook surface for OpenClaw `agent:bootstrap` runs.

### Weak-model operating rules
1. Default to `./query-memory.sh --mode auto`. The script will choose the strongest available local path and will report what actually ran via `mode_used`.
2. Trust the returned `mode_used`, `degraded`, `warnings[]`, `semantic_ready`, `semantic_fresh`, `index_fresh`, `authoritative_result_present`, `low_authority_only`, and each result's `match_authority` fields when they are present. Do not infer stronger capability than the payload states.
3. `--mode semantic` and `--mode hybrid` are now real implemented runtime modes. They are no longer compatibility stubs. Weak models still should prefer `auto` unless the task clearly requires a forced semantic/hybrid retrieval query.
4. If `--mode semantic` or `--mode hybrid` is requested on a host where the runtime reports `semantic_ready=false` or otherwise returns `degraded=true`, do not pretend semantic execution succeeded. Trust the returned `mode_used` and warnings: the request may honestly degrade to the strongest available local lexical path on this host. In that case, report the degraded lexical outcome as such and do not describe the result as semantic or hybrid retrieval. Precedence: if the payload also reports `index_fresh=false` (or `index_stale=true`) together with semantic unavailability, `D-WARN-COMBINED` applies and lexical fallback authority is revoked; otherwise apply `D-WARN-GENERIC` and present the degraded lexical result honestly.
5. For the lowest-friction safe path, weak models should think in this order: `health-check -> query(auto) -> read returned fields -> only then decide whether memorize or index is needed`.
6. `--mode learning` remains a learning-memory-oriented retrieval lane, but it now sits on top of the stronger v4 retrieval stack and still reports its true `mode_used` honestly.
7. Use `memorize.sh` only for reusable lessons that should influence future behavior. Positive test: memorize only if the lesson encodes a reusable decision rule, parameter set, or failure pattern that will predictably recur across ≥2 sessions or contexts. Do not log expected misses, one-off noise, duplicate lessons, or `checked, nothing relevant`.
8. Relation targets in `memorize.sh` are canonical, not freeform. Use only `learn:<signature>`, `chunk:<chunk_id>`, or `path:<canonical_path>` relation targets.
9. Do not execute internal helper scripts or reason about backend selection manually during normal use. The runtime owns retrieval choice; you consume the structured output.

### Canonical action routing
Use this compact routing map first when choosing what to do next; the detailed gates and exit-code tables below remain authoritative for script-specific interpretation.

| Trigger | First gate | Normal path | Maintenance / write path | Primary authority |
|---|---|---|---|---|
| Read/query request | `./health-check.sh` | If `OK` or degradable `WARN`, run `./query-memory.sh --mode auto --json` and trust returned fields | n/a | Health & Safety Gate + `query-memory.sh` payload |
| No-results query outcome | `query-memory.sh` exit + payload | If exit `1` and `degraded=false`, report clean miss; if degraded, apply matching `D-WARN-*` row | n/a | `query-memory.sh` exit table + payload |
| Durable lesson write | Pre-action gate | n/a | Run `./health-check.sh`, apply Health & Safety Gate, verify rollback, then run `./memorize.sh` only for reusable lessons | Pre-action gate + `memorize.sh` exit table |
| Index / repair freshness work | Pre-action gate | n/a | Run `./health-check.sh`, apply Health & Safety Gate, verify rollback, then run `./index-memory.sh` | Pre-action gate + `index-memory.sh` exit table |
| Any `FAIL` health state | `./health-check.sh` | Stop | Stop | `D-FAIL` |
| Ambiguous / out-of-scope request | command mapping check | Stop and ask for one of the public commands or escalate to maintenance | Stop and ask for one of the public commands or escalate to maintenance | Deterministic fallback |

### Degraded-State Response Catalog (single source of truth)
All mandatory user-visible degraded strings live here. Some rows are exact output strings; behavioral-rule rows are marked as such. Other sections reference this catalog by ID; do not restate inline elsewhere.

| ID | Trigger (payload signals) | Mandatory exact output |
|----|---------------------------|------------------------|
| `D-WARN-GENERIC` | `status=WARN` and no more specific trigger below | `⚠️ MEMORY DEGRADED: <reason>. Results are partial.` |
| `D-WARN-WRITE-ROLLBACK` | Any WARN continuation that performs writes or maintenance | Append: `⚠️ Continuing in degraded mode. Rollback path: <git/backup>.` |
| `D-WARN-INDEX-STALE-ONLY` | WARN caused by stale lexical index, semantic still OK | `⚠️ Memory index may be stale. Results may miss recent changes. Consider running ./index-memory.sh.` |
| `D-WARN-COMBINED` | `index_fresh=false` (or `index_stale=true`) **and** `semantic_ready=false` in the same WARN state | `⚠️ MEMORY DEGRADED: index stale, semantic unavailable. Results from query-memory fallback only. Missing recent changes and meaning-based matches. Run ./index-memory.sh and restore semantic prerequisites to resolve.` |
| `D-LOW-AUTHORITY` | `authoritative_result_present=false` and `low_authority_only=true` | *(behavioral rule, not an exact emit string)* Treat returned matches as heuristic/fallback assistance only; do not present as confirmed memory truth. |
| `D-FAIL` | `status=FAIL` | `❌ MEMORY UNAVAILABLE: health check FAIL.` Do not query, memorize, or edit memory files. |

JSON-capable outputs: mandatory degraded notices must live inside structured warning fields rather than outside the payload.

### Health & Safety Gate
For one-pass weak-model routing, prefer the **Weak-Model Decision Matrix** above first; this section remains the detailed degraded-state authority.
See **Canonical action routing** above for the shortest precedence map; this section remains the detailed degraded-state authority.
- **OK** → proceed normally.
- **WARN** → emit the matching catalog row (`D-WARN-COMBINED` takes precedence over `D-WARN-INDEX-STALE-ONLY`, which takes precedence over `D-WARN-GENERIC`). For writes/maintenance also append `D-WARN-WRITE-ROLLBACK`. For read-only degraded queries, state the degradation and fallback scope without requiring a rollback path.
- In the `D-WARN-COMBINED` state, lexical authority is revoked: do not present results as lexical truth or as `the best available answer`; do not invent manual retrieval steps outside the four public commands.
- Under `D-WARN-INDEX-STALE-ONLY`, indexed results remain usable but freshness-limited; do not present them as fully current. Under semantic-only unavailability (lexical freshness OK), lexical/index-backed results remain authoritative for exact/path/time-style matches, but do not describe them as semantic or meaning-based retrieval.
- `D-LOW-AUTHORITY` applies regardless of warn/ok surface whenever those fields are set.
- Do not treat every `warnings[]` note as a degraded retrieval result. Informational notes may appear even when the current request was satisfied exactly as designed; rely on the script's `degraded` field and exit code, not on the mere presence of warning text.
- Queue/backlog WARN states do not by themselves disable read/query authority, but they do require reporting that recent learnings or pending index work may not yet be reflected. Negative results under that WARN should be treated as potentially incomplete, not definitive absence.
- **FAIL** → emit `D-FAIL`.

### Interpreting `query-memory.sh` exit codes
After running `./query-memory.sh`, you MUST check the exit code and act accordingly:

| Exit Code | Meaning | Permitted Action |
|-----------|---------|------------------|
| `0` | Results found. Inspect `degraded` to determine stack health. | If `degraded=false`: use results normally. If `degraded=true`: results were returned but the stack is degraded — apply the matching `D-WARN-*` catalog row via the Health & Safety Gate while still using the returned payload. |
| `1` | No results found. Check `degraded` and `warnings[]` to tell whether this was a clean miss or a degraded no-results outcome. | If `degraded=false`, state: `No memory entries found for this query.` If `degraded=true`, state: `No memory entries found for this query (degraded retrieval; results may be incomplete).` Then apply the matching `D-WARN-*` row from the Degraded-State Response Catalog per the Health & Safety Gate precedence. Use returned `warnings[]` to surface any freshness-relevant notes. Do **not** treat exit code `1` as an automatic stack failure. |
| `2` | Degraded but usable results returned. | Apply the matching `D-WARN-*` catalog row via the Health & Safety Gate; inspect `degraded`, `warnings[]`, `authoritative_result_present`, and `low_authority_only`. Present any returned results explicitly as degraded/partial results, not as a normal or fully authoritative success. Do **not** treat this as a clean success. |
| `3` | Retrieval stack unavailable. | **STOP.** State: `❌ MEMORY UNAVAILABLE: Cannot search memory at all.` Do **not** continue as if this were a clean no-results case. Escalate to human maintenance. |
| `4` | Bad arguments provided to script. | **STOP.** State the argument error and re-evaluate the command. |
| `5` | Internal script error. | **STOP.** State: `❌ MEMORY INTERNAL ERROR.` Escalate to human maintenance. |

**CRITICAL:** Do not confuse exit code `1` (clean miss) with exit code `3` (broken retrieval stack). The former is normal operation; the latter requires immediate escalation.

### Interpreting `memorize.sh` exit codes
After running `./memorize.sh`, you MUST check the exit code and act accordingly:

| Exit Code | Meaning | Permitted Action |
|-----------|---------|------------------|
| `0` | Learning was written successfully, or an exact duplicate was safely skipped. | State success honestly. Do **not** retry a duplicate write as if persistence failed. |
| `4` | Bad arguments provided to script. | **STOP.** State the argument error and re-evaluate the command. |
| `5` | Internal script error. | **STOP.** State: `❌ MEMORY INTERNAL ERROR.` Escalate to human maintenance. |

If you need machine-readable confirmation, prefer `./memorize.sh --json ...` and inspect its `status` field (`written` vs `duplicate`) instead of inventing extra exit-code meanings.

### Interpreting `health-check.sh` exit codes
After running `./health-check.sh`, you MUST check the exit code and act accordingly:

**Precedence rule:** for normal degraded-mode routing, always execute `./health-check.sh --json` and decide `OK` vs `WARN` vs `FAIL` from the parsed JSON `status` field plus payload details. Treat the bash exit code only as a hard-stop gate: exit `3`, `4`, or `5` means immediate stop/escalate; other non-fatal paths still require JSON parsing before selecting a `D-WARN-*` row.

| Exit Code | Meaning | Permitted Action |
|-----------|---------|------------------|
| `0` | Overall status is `OK`. | Proceed normally. |
| `2` | Overall status is `WARN`. | Apply the matching `D-WARN-*` catalog row via the Health & Safety Gate. |
| `3` | Overall status is `FAIL`. | Emit `D-FAIL` and STOP. Do not continue with memory edits or retrieval-dependent work. |
| `4` | Bad arguments provided to script. | **STOP.** State the argument error and re-evaluate the command. |
| `5` | Internal script error. | **STOP.** State: `❌ MEMORY INTERNAL ERROR.` Escalate to human maintenance. |

If you need machine-readable status decisions, prefer `./health-check.sh --json` and inspect structured `status`, `warnings`, and `checks[]` fields rather than guessing from free text.

### Interpreting `index-memory.sh` exit codes
After running `./index-memory.sh`, you MUST check the exit code and act accordingly:

| Exit Code | Meaning | Permitted Action |
|-----------|---------|------------------|
| `0` | Requested indexing/maintenance action completed without warnings. | Continue normally. |
| `2` | Action completed with warnings or expected degraded conditions. | Report the warning state explicitly. Treat indexing as usable-but-degraded until the warning cause is resolved. On lexical-only hosts, `--rebuild-vectors` returning `2` because semantic dependencies are unavailable is an expected degraded outcome, not an unexpected hard failure. |
| `3` | Index maintenance failed at the storage/runtime layer. | **STOP.** State: `❌ MEMORY UNAVAILABLE: index maintenance failed.` Escalate to human maintenance. |
| `4` | Bad arguments provided to script. | **STOP.** State the argument error and re-evaluate the command. |
| `5` | Internal script error. | **STOP.** State: `❌ MEMORY INTERNAL ERROR.` Escalate to human maintenance. |

If you need machine-readable details, prefer `./index-memory.sh --json` and inspect `actions[]`, `warnings[]`, and any mode-specific fields returned by the script.

### Pre-action gate
**Applies when:** the next action is a script/policy/index edit that modifies files, OR a `./memorize.sh` call meant to durably record a high-value lesson. For the short routing form, see **Canonical action routing** above.

Execute in order, do not skip:
1. Run `./health-check.sh` directly (not via `bash <script>`).
2. Apply the Health & Safety Gate result:
   - `OK` → continue to step 3.
   - `WARN` → emit the matching catalog row (plus `D-WARN-WRITE-ROLLBACK`) and continue to step 3 only if the rollback path is concrete.
   - `FAIL` → emit `D-FAIL` and STOP.
3. Verify rollback exists: `git status`, a backup directory, or untouched canonical files. If rollback is unclear, abort and escalate to human maintenance.
4. If live inspection contradicts a change-memory record marked `applied`, trust live inspection, abort the write/maintenance action, and treat the host as degraded until reconciled.
5. Do not ingest `references/maintenance.md` during normal operation; open it only for human-led maintenance or when this skill explicitly tells you to.

### Deterministic fallback
- If a request does not clearly map to the four public commands or the explicit maintenance path, reply: `Out of scope for super-memori v4 local-only runtime. Please specify which command to run or escalate to human maintenance.` After running a public command, follow the exit-code interpretation rules above exactly.
- If you are unsure whether information qualifies for `memorize.sh`, default to not memorizing.

## Maintenance Reference
For retrieval pipeline contracts, write/learning contracts, promotion rules, maintenance entrypoints, release gates, and anti-patterns, see [`references/maintenance.md`](references/maintenance.md).
