# Minimal Governance Run Example

This example shows a minimal end-to-end run for `workspace-governance`.

## 1) Input Intent

User intent:

```text
Organize workspace and show plan first.
```

Runtime mode:

```text
Interactive
```

## 2) Effective Policy (excerpt)

Loaded from `SKILL_ADAPT.yaml`:

- `workspace_root: .`
- `immutable_dirs: [.git, .cursor, .claude, node_modules]`
- `destructive_guard.require_dry_run: true`
- `execution.batch_size: 20`

## 3) Dry-Run Plan (sample)

| Item | Current | Proposed Action | Target | Risk | Reason |
|------|---------|-----------------|--------|------|--------|
| `tmp/report.tmp` | root | delete | — | medium | temporary artifact |
| `notes-final.docx` | root | ask-user | `docs/` or `archive/` | low | ambiguous ownership |
| `build/cache.bin` | root | archive | `archive/cache/` | low | stale build residue |

## 4) Confirmation Gate

Prompt:

```text
Proceed with delete (1 item) and archive (1 item)?
Pending decision: notes-final.docx destination.
```

User response:

```text
Proceed. Move notes-final.docx to docs/.
```

## 5) Execution Result (sample)

- Batch 1: archived `build/cache.bin` -> success
- Batch 2: moved `notes-final.docx` to `docs/` -> success
- Batch 3: deleted `tmp/report.tmp` -> success

## 6) Log Snapshot (sample)

```json
{
  "timestamp": "2026-04-28 15:30:00",
  "intent": "organize",
  "batch_id": "batch_1",
  "action": "archive",
  "source_path": "build/cache.bin",
  "target_path": "archive/cache/cache.bin",
  "result": "success",
  "reversible": "yes",
  "rollback_ref": "checkpoint_batch_1"
}
```

## 7) Non-Interactive Variant (blocked sample)

If runtime has no confirmation capability and an `ask-user` item exists:

```text
status: blocked
pending_decisions:
  - item: notes-final.docx
    needed_input: choose destination (docs/ or archive/)
```
