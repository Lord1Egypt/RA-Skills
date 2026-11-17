# ue-audit

Read-only Unreal Engine project audit and reporting.

`ue-audit` answers five questions without writing to the project:

1. Is the project structure complete?
2. What changed relative to a baseline?
3. Are there abnormal files (zero-byte, too large, unhashable)?
4. Are there attributable log errors/crashes?
5. Did the audit observe any content or directory-write change?

Outputs: `report.json`, `report.md`, self-contained `report.html`, `junit.xml`, and an `evidence/` bundle.

> This is an assessment report, not a certification. It records what the tool observed under the configured roots and exclusions.

## Install

Requires Python 3.9+.

```bash
python -m pip install -e .
# or, without installing:
set PYTHONPATH=src
python -m ue_audit --help
```

## Quick start

```bash
ue-audit audit C:/Projects/MyGame

ue-audit audit C:/Projects/MyGame --out D:/audit/run1 --save-baseline D:/audit/baseline.json
ue-audit audit C:/Projects/MyGame --out D:/audit/run2 --baseline D:/audit/baseline.json

ue-audit verify C:/Projects/MyGame --task task.json --baseline D:/audit/baseline.json

ue-audit doctor C:/Projects/MyGame
```

The output directory must be outside the project.

## Checks

| ID | Check | Mode |
|---|---|---|
| PRJ001 | Project structure / EngineAssociation / plugin descriptors | offline |
| PRJ002 | Deterministic manifest + baseline diff | offline |
| PRJ003 | Zero-byte / large / unhashable files | offline |
| GIT001 | Git working-tree hygiene | offline optional |
| PKG001 | Packaging readiness (static) | offline |
| LOG001 | Log errors/crashes | offline |
| LIVE001 | Bridge/editor health | live optional |
| BP001 | Blueprint compile status + L2 graph stats | live optional |
| DT001 | DataTable structure | live optional |
| UMG001 | Widget tree structure | live optional |
| MAT001 | Material expression count | live optional |
| ANIM001 | AnimBlueprint graph/node stats | live optional |
| PIE001 | PIE smoke | live opt-in |
| SAFE001 | Manifest/metadata comparison | always |
| SAFE002 | Directory-write monitor | always/Windows |
| VER001 | Task write-set verification | verify |

## Live mode

Live checks are optional and require a local HTTP editor bridge at `127.0.0.1:8889` by default. The bridge is not bundled. Without it, live checks are `skip`/`unknown` and offline checks still complete.

Token precedence: `--token` → `UE_AUDIT_BRIDGE_TOKEN` → `UE_AUDIT_BRIDGE_TOKEN_FILE` → `%APPDATA%\ue-audit\bridge-token`.

## Read-only boundary

`SAFE001`/`SAFE002` are observations, not absolute proof. See `README.md` (Chinese) and `docs/CHECKS.md` for the exact limits.

## License

Apache-2.0. See `LICENSE`.
