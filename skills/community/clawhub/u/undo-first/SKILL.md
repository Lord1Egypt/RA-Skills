---
name: undo-first
description: Reversible-action infrastructure for AI agents. Use before any side-effecting action (writing/deleting/moving files, config changes, git pushes, sending messages, deploys, API calls) when the user asks "can we roll this back?", "make this safe to try", or when executing risky multi-step work. Provides hash-verified snapshots, a risk gate that demands an undo or compensation plan before acting, byte-identical restore, and a tamper-evident audit journal. Philosophy - no undo path, no action.
allowed-tools: Read, Write, Edit, Bash(python3 scripts/undo_guard.py:*)
---

# Undo-First Guard

**No undo path, no action.** Every side effect gets a verified way back — or it does not happen. There is no in-plan opt-out.

## The workflow (always in this order)

1. **Classify** the action: `file_write | file_delete | file_move | dir_change | config_change | git_push | external_message | deploy | api_call | payment | publish`
2. **Snapshot** file-level state before acting:
   ```bash
   python3 scripts/undo_guard.py snapshot <paths...>
   ```
   Stores sha256 manifest + backup copies under `.undo-journal/`. For non-file actions, skip snapshot.
3. **Write the undo plan** (JSON, schema: [references/plan-schema.md](references/plan-schema.md)) and pass the gate:
   ```bash
   python3 scripts/undo_guard.py plan my-plan.json
   ```
   Exit `0` ACCEPT · `1` ACCEPT_WITH_WARNING · `2` REJECT. **A REJECT means do not perform the action** — either build the undo path or ask the user to accept the risk explicitly.
4. **Act** (the agent performs the action).
5. **Verify / restore** if anything goes wrong:
   ```bash
   python3 scripts/undo_guard.py verify <snapshot-id>   # what changed since snapshot?
   python3 scripts/undo_guard.py restore <snapshot-id> --yes  # byte-identical rollback
   ```
   Restore is sha256-verified both ways: backups are checked against the manifest before restoring (tamper → REFUSED) and after (restored file must be byte-identical). It also removes files created after the snapshot inside the snapshot roots, so moves and directory changes roll back too. Because that overwrites/removes files, restore refuses to act without `--yes`; use `--keep-created` to preserve new work. Destinations that traverse a symlink are refused.
6. **Journal** — every decision is already recorded in a hash-chained audit trail; show or verify it when asked:
   ```bash
   python3 scripts/undo_guard.py journal
   python3 scripts/undo_guard.py journal --verify   # detect edits/deletions
   ```

## Risk-gate rules (deterministic)

- **Irreversible actions** (`external_message`, `deploy`, `api_call`, `payment`, `publish`, `delete_remote`) require `undo.kind = "compensation"` with concrete mitigation steps — the gate REJECTS "none" or bare "commands". An email cannot be unsent; the plan must say what makes it right.
- **File actions at risk ≥ medium** require `builtin_restore` (snapshot taken) or rollback `commands` with a `verify.check`.
- **`builtin_restore`** requires `undo.snapshot` (a real snapshot id) **and** `action.target` (or `action.targets`). The gate loads the snapshot, re-hashes every backup, and rejects missing, tampered, or non-covering snapshots.
- **`undo.kind = "compensation"`** requires non-empty, concrete steps for every action class (file actions included).
- **`undo.kind = "commands"`** requires non-empty steps AND `verify.check` proving restoration.
- **`undo.kind = "none"` → REJECT** for every action type, including low risk. There is no in-plan opt-out: take a snapshot or provide rollback/compensation.
- **Unknown action type → REJECT.** Classify first.

## Static source self-check (limited)

Plans and files are treated as **data, not code**. A limited heuristic checks this file's source text for a fixed list of execution primitives:

```bash
python3 scripts/undo_guard.py selfcheck
```

It looks for literals such as `os.system`, `subprocess`, `eval(` and reports each as absent. This is a source-text heuristic, not a proof: it cannot rule out dynamic or imported behavior. The behavioral guarantees are covered by the harness (backup tamper refusal, byte-identical restore, filesystem boundary handling), not by this check.

## Choosing undo.kind

| Situation | kind |
|---|---|
| Files/dirs/config on disk | `builtin_restore` (snapshot first, then cite `snapshot` + `target`) |
| Git/deploy where a documented rollback command exists | `commands` + `verify.check` |
| Email, messages, payments, publishes (cannot be unsent) | `compensation` (mitigation steps) |
| Trivially reproducible, low risk | `none` is never accepted — snapshot or provide rollback steps |

## Verification

```bash
python3 tests/test_undo_guard.py
```

23 cases: modify/delete/multi-file restore proven **byte-identical by sha256**, created-file cleanup, explicit `--yes` confirmation gate (and `--keep-created`), tampered-backup refusal, snapshot coverage/integrity rejections, 13 risk-gate decisions (including the no-undo and operator-override paths), source-text selfcheck heuristic, journal audit trail, and hash-chain tamper detection. Evidence JSON is written to `../evidence/undo_test_results.json`.

## Limitations

- Restore covers file-level state only; remote-world actions rely on `compensation` plans executed by the agent.
- Restore removes files created after the snapshot but leaves any newly created empty directories in place.
- Snapshots consume disk proportional to target size; snapshot specific paths, not whole disks.
- The gate re-hashes snapshot backups on every `builtin_restore` plan, so very large snapshots make gating slower — snapshot the affected paths, not whole disks.
- The journal is a local file. It is hash-chained and `journal --verify` is strict: edited, deleted, or hash-stripped entries are rejected. The file is still not immutable — anyone with filesystem write access can replace it wholesale. Store it outside the agent's write scope when audit integrity matters.
- `selfcheck` is a literal-string heuristic over this one source file; it does not prove the absence of execution paths. Treat it as a smoke signal, not a security guarantee.
- The risk gate validates plan *structure*, not the quality of compensation steps — write them concretely (who, what, by when).
