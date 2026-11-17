# Report schema (v1, ue-audit 0.1)

`report.json` is the machine-readable report. `report.md`, `report.html`, and `junit.xml` are derived views.

## Top level

```json
{
  "schema_version": 1,
  "tool": "ue-audit",
  "tool_version": "0.1.0",
  "run_id": "20261104T033349Z-e0f566",
  "generated_at": "2026-11-04T03:33:49+00:00",
  "mode": "audit",
  "fail_on": "warning",
  "project": {},
  "engine": {},
  "baseline": null,
  "summary": {},
  "checks": [],
  "findings": [],
  "readonly_proof": {},
  "limitations": [],
  "evidence": {}
}
```

## Status

Checks and findings use one of:

```
pass | fail | warn | skip | unknown | error
```

`unknown` is not a failure and is not a pass. It means the tool could not evaluate the item (for example, no baseline, no logs, bridge unavailable, or a file too large to hash).

## Severity

```
blocker | error | warning | info
```

Exit code mapping:

- `0`: no error/blocker
- `1`: warning only
- `2`: error/blocker
- `3`: usage/config error
- `4`: audit could not complete

## Finding

```json
{
  "id": "UEA-0001",
  "check_id": "LOG001",
  "severity": "error",
  "status": "fail",
  "title": "Log error",
  "message": "Game.log:120: ...",
  "asset": "C:/Project/Saved/Logs/Game.log",
  "evidence": [],
  "recommendation": "Open the log around this line.",
  "provenance": "unknown",
  "confidence": "fact"
}
```

`provenance`:

```
ai | manual | unknown | toolchain
```

`confidence`:

```
fact | rule | ai
```

v0.1 uses `fact` and `rule`; it does not use an LLM to produce findings.

## Check

```json
{
  "check_id": "PRJ002",
  "title": "Baseline diff",
  "status": "warn",
  "severity": "warning",
  "summary": "added=0, removed=0, changed=1, unknown=0, metadata=0",
  "details": {},
  "findings": [],
  "started_at": "2026-11-04T03:33:49+00:00",
  "duration_ms": 0
}
```

## readonly_proof

```json
{
  "before_manifest_sha256": "...",
  "after_manifest_sha256": "...",
  "content_equal": true,
  "metadata_equal": true,
  "unknown_count": 0,
  "no_observed_difference": true,
  "during_write_monitor": "available",
  "during_write_clean": true,
  "during_write_event_count": 0,
  "during_write_events": [],
  "during_write_overflow": false,
  "during_write_reason": "",
  "during_write_limitation": "Best-effort ReadDirectoryChangesW...",
  "diff": {},
  "statement": "No content or metadata difference and no directory write events were observed...",
  "limitations": []
}
```

This is an observation, not a certification. See README "只读证据的边界".

## evidence

Relative paths inside the output directory:

```json
{
  "manifest_before": "evidence/manifest-before.json",
  "manifest_after": "evidence/manifest-after.json",
  "manifest_diff": "evidence/manifest-diff.json",
  "readonly_proof": "evidence/readonly-proof.json",
  "checks": "evidence/checks.json",
  "write_events": "evidence/write-events.json",
  "index": "evidence/index.json"
}
```

`evidence/index.json` lists each evidence file with size and SHA256.

## Manifest

`evidence/manifest-before.json` / `manifest-after.json`:

```json
{
  "schema_version": 1,
  "tool": "ue-audit",
  "tool_version": "0.1.0",
  "root": "C:/Project",
  "generated_at": "...",
  "algorithm": "sha256",
  "roots": ["Content", "Config", "Source", "Plugins"],
  "excludes": [],
  "max_hash_bytes": 536870912,
  "file_count": 123,
  "total_bytes": 456789,
  "manifest_sha256": "...",
  "files": {
    "Content/A.uasset": {
      "size": 123,
      "mtime_ns": 123456789,
      "sha256": "..."
    }
  }
}
```

`manifest_sha256` covers the file map, size, mtime, hashes, hash-skip reasons, symlink flags, errors, roots, exclusions, and max hash size. It deliberately excludes `generated_at` and `root`, so the same content produces the same manifest hash.

## Determinism

- File walk is sorted.
- Paths use POSIX separators.
- Diff comparisons are case-insensitive for matching; the after path is reported.
- JSON uses sorted keys.
- `generated_at` and `run_id` are the only intentionally variable fields.
