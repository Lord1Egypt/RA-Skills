# Undo Plan Schema (JSON)

One plan per action. The gate (`undo_guard.py plan`) validates structure deterministically — plans are **data**, the engine never executes their contents.

## Template

```json
{
  "action": {
    "type": "file_write",
    "description": "Overwrite reports/summary.md with the new quarterly summary",
    "target": "reports/summary.md"
  },
  "risk": "medium",
  "undo": {
    "kind": "builtin_restore",
    "steps": ["python3 scripts/undo_guard.py restore <snapshot-id>"],
    "snapshot": "<snapshot-id>"
  },
  "verify": {
    "check": "sha256 of reports/summary.md equals the snapshot manifest entry"
  }
}
```

## Fields

### `action` (required)
| Field | Values | Notes |
|---|---|---|
| `type` | `file_write`, `file_delete`, `file_move`, `dir_change`, `config_change` (file class) · `git_push`, `external_message`, `deploy`, `api_call`, `payment`, `publish`, `delete_remote` (irreversible class) | Unknown values → REJECT |
| `description` | free text | Missing → warning (journal becomes unauditable) |
| `target` | path / endpoint | **required for `builtin_restore`** (coverage check); recommended otherwise |
| `targets` | array of paths | alternative to `target` when several paths are affected |

### `risk` (required)
`low` | `medium` | `high` | `critical` — how hard to recover if the action is wrong.

### `undo` (required)
| `kind` | When to use | Gate requirements |
|---|---|---|
| `builtin_restore` | Anything on disk — snapshot taken first | `snapshot` id **and** `target`/`targets` required; snapshot must exist, pass per-file backup sha256 integrity, and cover every target |
| `commands` | Documented rollback exists (git revert, deploy rollback) | `steps` non-empty **and** `verify.check` present |
| `compensation` | Irreversible in the real world (email, payment, publish, or any class) | `steps` non-empty (strings) — enforced for file actions too |
| `none` | Nothing recoverable available | REJECT for every action class, including `risk=low` — a plan cannot self-authorize |

`steps`: array of concrete rollback/mitigation instructions (for the agent/human — the engine does not run them).
`snapshot`: snapshot id when `kind=builtin_restore`; validated against `.undo-journal/snapshots/<id>/manifest.json`.

`builtin_restore` validation is fail-closed: missing id, unknown id, missing/corrupt backup, or a target outside the snapshot manifest all produce REJECT. `restore` requires `--yes` before overwriting changed files or removing ones created after the snapshot (`--keep-created` preserves new files; empty directories are left behind).

### `verify` (required for `commands`, warned for `critical`)
`check`: how to prove the rollback actually restored the desired state (hash comparison, API status, confirmed receipt…).

## Gate outcomes

| Verdict | Exit | Meaning |
|---|---|---|
| ACCEPT | 0 | Action may proceed |
| ACCEPT_WITH_WARNING | 1 | Proceed only after acknowledging the warning |
| REJECT | 2 | **Do not act.** Build an undo path or get explicit user acceptance of the risk |

Every gate decision is appended to `.undo-journal/journal.jsonl` with the full plan. Entries are hash-chained (`prev` + `hash`): `undo_guard.py journal --verify` detects edited or missing entries. This is tamper-evident, not immutable — a local file can still be replaced wholesale by anyone with filesystem write access, so export or relocate the journal when audit integrity matters. The journal is the evidence that the decision was made before the action, not after.
