# Checks (v0.4)

## PRJ001 — Project structure and engine association

Checks:

- `.uproject` is valid JSON and readable.
- `Content/` exists.
- `Config/` exists.
- `Config/DefaultEngine.ini` exists (warning if missing).
- `Config/DefaultGame.ini` exists (info only).
- `Source/` exists (info if absent; Blueprint-only projects are valid).
- `EngineAssociation` is non-empty.
- Plugins listed in the `.uproject` have a valid local `.uplugin` when present.

False positives:

- Engine/marketplace plugins are not in `Plugins/`; this is reported as info, not a failure.
- A intentionally minimal project may lack `DefaultGame.ini` or `Source/`.

## PRJ002 — Manifest and baseline diff

Builds a deterministic manifest of:

- `.uproject`
- `Content/`, `Config/`, `Source/`, `Plugins/`

Each file records size, mtime (ns), SHA256, and hash-skip reason. Excluded directories include `Saved/`, `Intermediate/`, `DerivedDataCache/`, `Binaries/`, `.git/`.

Diff buckets:

- `added`, `removed`, `changed` (content or size)
- `unknown` (file too large or unhashable)
- `metadata_changed` (same SHA256, different size/mtime/path case)

No baseline:

- `PRJ002` is `unknown`; it does not imply `pass` or `fail`.
- Create a baseline with `--save-baseline`.

False positives:

- mtime changes from a touch, checkout, or copy can produce `metadata_changed`.
- `--max-hash-mb` can turn large-file comparisons into `unknown`.

## PRJ003 — Abnormal file facts

Facts only:

- zero-byte files (warning for `.uasset`/`.umap`, info otherwise)
- files larger than `--max-file-mb` (default 100 MB) as info
- files that could not be hashed
- duplicate SHA256 groups (details only, not findings)

This check does not decide whether a large file is bad. It reports the fact.

## GIT001 — Git working-tree hygiene

Offline, optional. Runs only when the project is a Git working tree.

- HEAD / branch
- modified tracked paths
- untracked paths
- unresolved conflicts
- tracked files larger than `--git-large-mb` (default 50 MB)

Conflicts → error/fail. Modified/untracked → warning. Large files → info. Non-Git projects → skip. Disable with `--no-git`.

## PKG001 — Packaging readiness (offline)

Static check only; does not cook or package.

- reads `GameDefaultMap` / `EditorStartupMap` / `ServerDefaultMap` from `Config/DefaultEngine.ini`
- reads `MapsToCook` from `Config/DefaultGame.ini`
- checks `/Game/` map paths against the project manifest
- configured map missing → error/fail
- no `GameDefaultMap` → warning

## LOG001 — Log errors and crashes

Scans the newest `Saved/Logs/*.log` files (default 3).

- error/fatal/assert/exception/access-violation lines become findings;
- warning lines are counted but not turned into findings;
- known noisy categories (`LogHttp`, `LogStreaming`, `LogDerivedDataCache`, `LogPakFile`) are counted but do not become findings;
- no logs → `unknown` with `reason=no_logs`.

False positives:

- plugin/engine noise can still match error patterns;
- logs may be from a different editor session;
- log rotation can change line numbers.

## LIVE001 — Bridge and editor health

Optional. Requires a local HTTP editor bridge.

Checks:

- `bridge_loaded`
- editor project name vs audited project
- editor engine version vs `.uproject` association

Connection failure is `unknown`, not `pass` or `fail`.

## BP001 — Blueprint compile status

Optional. Requires `--blueprint /Game/...` (repeatable) and a bridge.

- calls `read_blueprint` with `level=L1`
- reads `l1.compile_status`
- does **not** call `compile_blueprint`
- binds `package_sha256` from the manifest when available

No selected blueprints → `skip` with `reason=no_blueprints_selected`.

False positives:

- bridge may point at a different project or an older editor instance;
- compile status may be stale or unavailable on older bridges.

## DT001 — DataTable structure

Optional. Requires `--datatable /Game/...` (repeatable) and a bridge.

- calls `datatable_read` with `include_csv=True`, `limit=50`
- reads `row_count`, `row_struct`, `csv_supported`, `truncated`
- binds `package_sha256` from the manifest when available

Findings:

- empty table → warning
- missing row struct → unknown
- CSV unavailable → info (UE 5.1 limitation)
- read failure → unknown

It does not write rows or validate game-specific column semantics.

## UMG001 — Widget tree

Optional. Requires `--widget /Game/...` (repeatable) and a bridge.

- calls `widget_read_tree`
- reads widget count, names, classes, parent links
- binds `package_sha256` from the manifest when available

Findings:

- empty tree → error/fail
- no parent-less root → warning
- multiple parent-less roots → warning
- read failure → unknown

It does not validate layout, text, bindings, or visual quality.

## MAT001 — Material structure

Optional. Requires `--material /Game/...` and a bridge.

- calls `material_read`
- reports expression count
- empty material → warning; read failure → unknown

No shader compilation, no material graph semantics.

## ANIM001 — AnimBlueprint structure

Optional. Requires `--animbp /Game/...` and a bridge.

- calls `animbp_probe` to confirm the asset is an AnimBlueprint
- calls `animbp_read` for graph/node counts
- not an AnimBP / read failure → unknown
- no graphs → warning

No animation logic validation.

## PIE001 — PIE smoke (opt-in, stateful)

Only with `--pie`. Requires `--live` and a bridge.

- refuses to start if PIE is already running
- starts PIE or Simulate (`--pie-mode`)
- polls `pie_state` for `--pie-seconds`
- reads only the new log lines after the start cursor
- stops PIE in a `finally` block
- does not save assets

If the bridge's PIE start API is unavailable, the check is `unknown`, not `fail`. New error log lines during the window → fail. Stop failure → warning.

## SAFE001 — Audit manifest evidence

Compares `manifest-before` and `manifest-after`:

- content equal?
- metadata equal?
- unknown files?
- diff summary

It does **not** prove absolute read-only behavior; it records what the tool observed.

## SAFE002 — During-write monitor

Windows `ReadDirectoryChangesW` over Content/Config/Source/Plugins while the audit runs.

- no events → pass
- events observed → warning, with `evidence/write-events.json`
- monitor unavailable (non-Windows/disabled) → unknown

It is best-effort, not kernel ETW/USN. Events outside the roots may be missed.

## VER001 — Task write-set verification

Only in `verify` mode.

- expected paths come from `expected_write_set` / `allowed_assets` / `allowed_write_set` / `write_set` / steps;
- matched expected changes → info/pass;
- missing expected changes → error/fail;
- unexpected changes outside the expected set → error/fail (toolchain paths downgraded to info);
- unhashable changes → unknown.

Requires a baseline manifest. Without one, `verify` refuses to run (exit 3).
