# super_memori v4 — Command Contracts

## Public commands
The active v4 weak-model public interface remains exactly four commands:

1. `query-memory.sh`
2. `memorize.sh`
3. `index-memory.sh`
4. `health-check.sh`

## `query-memory.sh`
### Purpose
Retrieve memory by exact, semantic, hybrid, recent, or learning-oriented query.

### Target flags
- `--mode auto|exact|semantic|hybrid|recent|learning`
- `--type episodic|semantic|procedural|learning|buffer|all`
- `--json`
- `--limit N`
- `--from DATE`
- `--to DATE`
- `--tags a,b,c`
- `--reviewed-only`

### Active-contract scope note
- `--mode semantic` and `--mode hybrid` are now real implemented runtime modes.
- For normal weak-model/runtime use, still prefer `auto`, `exact`, `learning`, or `recent`; use direct `semantic` / `hybrid` mainly when the task explicitly requires that maintenance/runtime check.
- `mode_used` remains authoritative over `mode_requested` for what actually executed on the current host.

### Target exit codes
- `0` results found without degraded execution for the current request
- `1` no results found; check `degraded` and `warnings[]` to distinguish a clean miss from a degraded no-results outcome
- `2` degraded mode with usable results returned
- `3` retrieval stack unavailable
- `4` bad arguments
- `5` internal error

### Required output fields
- `mode_requested`
- `mode_used`
- `degraded`
- `warnings`
- `index_fresh`
- `authoritative_result_present`
- `low_authority_only`
- `results`

### `mode_used` honesty rule
- If `--mode learning` was requested, `mode_used` must remain `learning` so downstream automation can tell intent from the underlying lexical engine.
- `mode_used=exact` is reserved for the normal exact/lexical retrieval path and for degraded `semantic` / `hybrid` requests that fall back to lexical search.

### Degraded vs informational warnings
- `warnings[]` may include informational host-state notes that do not by themselves force `degraded=true`.
- `degraded=true` is reserved for cases where the requested retrieval path became partial, stale, or fallback-backed for the current query.
- `authoritative_result_present` indicates whether at least one returned result still counts as confirmed exact/hybrid memory under the current runtime contract.
- `low_authority_only` indicates that every returned result is only semantic/fallback heuristic support rather than confirmed exact/hybrid memory.
- Informational notes such as "learning mode ran on lexical search on this host" may appear in `warnings[]` while `degraded=false` if the request was satisfied exactly as designed.
- `exit 2` must be interpreted from the query response itself (`degraded=true` plus returned `warnings[]`/results), without delegating to any separate health-state branch.
- `exit 1` does not by itself mean the host was fully healthy; it means no results were returned. Weak models must inspect `degraded` and `warnings[]` first, then frame the result as either a clean miss (`degraded=false`) or a degraded no-results outcome (`degraded=true`).
- A clean miss (`degraded=false`) does not cancel freshness-relevant warning notes. If `warnings[]` still reports queue/backlog delay, stale lexical index, or similar recent-changes-may-be-missing conditions, the response should keep the clean-miss wording but append a short caution that recent changes may not yet be reflected.

### Degraded authority rule
- `--mode learning` remains the learning-memory-oriented retrieval lane. It may still execute on a degraded lexical path on weaker/degraded hosts, but it no longer implies that the whole skill is only a lexical-first baseline.
- If `mode_requested=auto` on a degraded host, `auto` remains valid because the script may degrade internally to the lexical path.
- If semantic dependencies are unavailable but lexical freshness remains OK, lexical/index-backed results remain authoritative for exact/path/time-style retrieval only; they must not be described as semantic or meaning-based retrieval.
- If `authoritative_result_present=false` and `low_authority_only=true`, returned matches must be framed as heuristic/fallback support only, not as confirmed memory truth.
- If lexical freshness is stale but semantic dependencies are otherwise available, indexed results remain usable but freshness-limited; they must not be described as fully current until `./index-memory.sh` is run.
- If lexical freshness is stale and semantic dependencies are unavailable at the same time, rely only on the degraded results surfaced by `query-memory.sh` itself.
- In that double-degraded state, returned matches must be interpreted as file-derived fallback matches only, not fresh indexed truth and not semantic matches.
- Do not invent direct manual file-reading steps outside the four public commands; the public degraded path remains `query-memory.sh` plus its explicit warnings.
- Queue/backlog WARN states require explicit freshness caution but do not by themselves remove read/query authority.
- The operator warning for the double-degraded state must explicitly say: `Missing recent changes and meaning-based matches. Run ./index-memory.sh and restore semantic prerequisites to resolve.`

## `memorize.sh`
### Purpose
Write a useful learning record that can improve future behavior.

### Target types
- `error`
- `correction`
- `lesson`
- `insight`

### Actual exit codes
- `0` learning written successfully, or exact duplicate safely skipped
- `4` bad arguments
- `5` internal error

### Output contract
- Human-readable mode may print either `written: ...` / `queued: ...` or `duplicate skipped: ...`
- JSON mode must include at least `status` plus the target `file`
- `status=written` and `status=duplicate` are both successful non-error outcomes and share exit code `0`
- Weak models must not invent separate failure meanings for duplicates; inspect JSON `status` when the distinction matters

### Rule
Do not auto-log every failure. Only write when the event teaches future behavior.

## `index-memory.sh`
### Purpose
Manage lexical and semantic index maintenance.

### Target modes
- `--incremental`
- `--full`
- `--rebuild-fts`
- `--rebuild-vectors`
- `--stats`
- `--vacuum`
- `--audit`

### Actual exit codes
- `0` requested action completed without warnings
- `2` completed with warnings or expected degraded conditions
- `3` storage/runtime failure during index maintenance
- `4` bad arguments
- `5` internal error

### Required output fields
- `actions`
- `warnings`
- mode-specific fields such as `lexical_entries`, `lexical_chunks`, `db_path`, `state`, `semantic`, and `audit` when `--stats` is used

### Interpretation rule
- `warnings[]` is authoritative for whether the maintenance run completed only partially or with degraded follow-up obligations.
- `--rebuild-vectors` may legitimately return `2` when semantic rebuild was requested but not executed because Qdrant or semantic dependencies are unavailable.
- Weak models must not treat `2` as a clean success; they must report the warning state explicitly.

## `health-check.sh`
### Purpose
Verify the health of canonical files, indexes, freshness, backlog, semantic host state, and integrity drift.

### Actual exit codes
- `0` overall status `OK`
- `2` overall status `WARN`
- `3` overall status `FAIL`
- `4` bad arguments
- `5` internal error

### Exit-code mapping rule
- `0` maps to the public `OK` branch
- `2` maps to the public `WARN` branch
- `3` maps to the public `FAIL` branch
- `4` and `5` are execution errors, not health states

### Required output contract
Human-readable mode must emit:
- leading `status: <OK|WARN|FAIL>` line
- one `- <check_name>: <ok|fail> (<detail>)` line per check
- `warnings:` block only when warnings exist

JSON mode must emit:
- `status`
- `warnings`
- `checks[]`

### Structured warning rule
- Mandatory degraded-mode notices must be represented inside the structured `warnings[]` payload in JSON mode rather than breaking JSON with extra free text.
- Human-readable mode may render the same notices as plain warning lines in stdout.

### Check/interpretation rule
- `health-check.sh` summarizes degraded state through explicit status plus named checks/warnings; weak models must not infer freshness or semantic readiness from unrelated raw logs.
- Different degraded causes share the same `WARN` exit code; automation should use the named checks/warnings payload to distinguish stale lexical index, semantic dependency loss, semantic-unbuilt host state, queue backlog, broken relations, or other degraded-but-usable states.

## `audit-memory.sh` (maintenance-only)
### Purpose
Audit lexical/semantic integrity drift without expanding the weak-model public command surface.

### Actual exit codes
- `0` audit clean
- `2` drift/warn state found
- `4` bad arguments
- `5` internal error

### Expected semantics
- `vector_state=semantic-unbuilt` means semantic vectors are simply not built on this host yet; this is a host-state warning, not corruption by itself
- `vector_state=stale-vectors` means lexical truth has outrun vector rebuild and hybrid quality is degraded until rebuild
- `orphan_vectors` and `orphan_chunks` are true integrity drift signals
- `broken_relations` means relation-target discipline was violated or references point at missing canonical targets

### Status model
- `OK`
- `WARN`
- `FAIL`
