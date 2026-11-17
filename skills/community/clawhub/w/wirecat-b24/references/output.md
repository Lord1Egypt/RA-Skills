# Output and exit codes

- **Add `--json` and read stdout.** It carries one JSON value and nothing else; warnings go to stderr. An error that
  ends the command goes to stderr as `{"error": {"code", "reason", "message", "details"}}`, and stdout stays empty.
- **Branch on the exit code and `reason`, never on the text.** `b24 commands info --json` lists every `reason` with
  its `code`.
- **`--json=id,ref,title`** keeps those fields of each item. `--jsonl` prints one object per line. `--compact` prints
  one line per item with the ref first, for reading. `--no-input` never prompts.
- **Lists answer an object, not an array:** `{ "items": [...], "page": {...}, "meta": {...} }`; one record is
  `{ "item": {...}, "meta": {...} }`. A list shows the newest first: `--limit` and `--page` move through it.
- **`--dry-run` before a write** parses the arguments and names every permission key the command checks, with its
  level. It sends nothing to the portal.
- One command has 30 seconds by default (`--timeout 2m` changes it). A `sync` stops before its deadline and the next
  one goes on from there.
- `effects.remote: "write"` in `commands info` marks a write to the portal; `effects.local: "write"` alone, a write to
  this computer.
- `b24 guide` lists scenarios for common tasks, each as commands in order with why; `b24 guide <name> --json` gives
  one as data.

| Exit | Code | What to do |
|---:|---|---|
| 0 | — | Done. Still read `complete` and `issues` in a sync answer. |
| 1 | — | The profile's sign-in names no portal user, so no stored deal or lead is read: the owner runs `session start` again. |
| 2 | `validation_error` | Bad input: fix it. Also "name a profile", with `details.profiles`. |
| 3 | `configuration_error` | The settings file is wrong: `b24 doctor` says how to fix it. |
| 4 | `authentication_error` | Not signed in, or the portal refused the webhook. Only the owner signs in. |
| 5 | `permission_error` | Permissions, `B24_READ_ONLY` or the webhook user's rights refuse it. Final: tell the owner. |
| 6 | `not_found` | No such record, stage, pipeline or method. |
| 7 | `confirmation_required` | The write asks first and nobody answered. Stop and ask the owner. |
| 8 | `rate_limited` | The portal's limit: wait as the error says, then run it once more. |
| 14 | `outcome_unknown` | The write may have happened. Never repeat it blindly: see [writing.md](writing.md). |
| 15 | `conflict` | The request clashes with what the portal or the journal holds: read the record before you write. |

Reasons worth knowing: `employee.delete`, `employee.clear`, `employee.batch`, `employee.unbind` and `employee.merge`
(only an administrator's webhook may do that), `webhook.refused`, `webhook.scope-missing`, `bitrix.access-denied`
(the webhook's user may not do that in Bitrix24), `deal.ambiguous` and the other `*.ambiguous`, and
`crm.record-ambiguous` (several records have that name: take an id), `field.unknown` and `field.unknown-option`.
