# Output and exit codes

- **Add `--json` and read stdout.** It carries one JSON value and nothing else; warnings go to stderr. An error that
  ends the command goes to stderr as `{"error": {"code", "reason", "message", …}}`, and stdout stays empty.
- **Branch on the exit code and `reason`, never on the text.** `amo commands info --json` lists every `reason` with
  its `code`.
- **`--json=id,ref,title`** keeps those fields of each item. `--jsonl` prints one object per line. `--compact` prints
  one line per item with the ref first, for reading. `--no-input` never prompts.
- **Lists answer an object, not an array:** `{ "items": [...], "page": {...}, "meta": {...} }`; one record is
  `{ "item": {...}, "meta": {...} }`. A list shows the newest first: `--limit` and `--page` move through it.
  `changes list` moves on with `--cursor`, from the last answer's `page.next`.
- **`--dry-run` before a write** parses the arguments and names every permission key the command checks, with its
  level. It sends nothing to the account.
- One command has 30 seconds by default (`--timeout 2m` changes it). A `sync` stops before its deadline and the next
  one goes on from there.
- `amo help options` lists the options every command takes.

| Exit | Code | What to do |
|---:|---|---|
| 0 | — | Done. Still read `complete` and `issues` in a sync answer. |
| 1 | — | Anything else. Read the message and tell the owner. |
| 2 | `validation_error` | Bad input: fix it. Also "name a profile", with `details.profiles`. |
| 3 | `configuration_error` | The settings are wrong: `amo doctor` says how to fix them. |
| 4 | `authentication_error` | Not signed in, or the token expired (`session.expired`). Only the owner signs in. |
| 5 | `permission_error` | Permissions, `AMO_READ_ONLY` or the user's amoCRM rights refuse it. Tell the owner. |
| 6 | `not_found` | No such record, stage, pipeline or operation. |
| 7 | `confirmation_required` | The write asks first and nobody answered. Stop and ask the owner. |
| 8 | `rate_limited` | amoCRM's limit: wait as the error says, then run it once more. |
| 9 | `timeout` | The command ran out of time. A `sync` goes on from where it stopped. |
| 10 | `network_error` | The account could not be reached. Try once more later. |
| 11 | `provider_error` | amoCRM answered with an error. |
| 12 | `provider_unavailable` | amoCRM is down or under maintenance. Try later. |
| 13 | `invalid_response` | amoCRM's answer was not what its reference describes. Report it. |
| 14 | `outcome_unknown` | The write may have happened. Never repeat it blindly: see [writing.md](writing.md). |
| 15 | `conflict` | The request clashes with what the account or the journal holds: read the record before you write. |
| 130 | `cancelled` | Stopped by the owner. |

Reasons worth knowing: `employee.delete`, `employee.clear` and `employee.unbind` (only an administrator may do that),
`amo.access-denied` (amoCRM refused the user), `amo.subscription-ended` (writes stop at once, reads 30 days later),
`amo.blocked` (stop every `amo` command on the account), `amo.filters-off` (no API filter add-on: search by name),
`crm.record-field` (amoCRM cannot filter that list by that field), `crm.record-ambiguous`, `pipeline.ambiguous` and
`field.ambiguous` (several records have that name: take an id), and `crm.foreign-contacts-spent`.
