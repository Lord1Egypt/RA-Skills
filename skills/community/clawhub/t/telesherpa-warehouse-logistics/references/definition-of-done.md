# Definition of Done — the audit before any status report

Read this before you write a progress or completion message.

## The one sentence that replaces "done"

> The workspace is configured when a person who has never seen the build can print
> a sheet of labels, stick one on a package, bind it with a single scan, and see
> the quantity on that package, and a manager can put away, pick, relocate and
> count that package — without asking anyone.

Anything that cannot be traced to that sentence is not part of "done".

## The audit — one call per line, quote the value

Run these in order. Keep the numbers; they go into the report verbatim. The table
is the same as in [SKILL.md](../SKILL.md).

| # | What it proves | Call | What you quote |
|---|---|---|---|
| 1 | the three scopes exist | `ontouser_scope_index` | the three names with their suffixes and `can_manage_scope` |
| 2 | the scopes are populated and who is in them | `onto_scope_index` | `obj_count`, `user_count`, `manager_count` per scope |
| 3 | the label, package and movement fields are the live ones | `onto_type_show` | `code`, `charge`, `labelStatus` values, `menge`, `einheit`, `lot`, `bestBefore`, `stockMovement` fields |
| 4 | something is visible to a human, and the start card is registered | `onto_settings_list`, `onto_startcard_index` | number of views per scope; the start card row |
| 5 | bind, rebind and stock actions exist, functions match the package scope, manager actions are gated | `onto_actiondef_list`, `onto_function_index` | the six keys; function `scopes`; `require_scope_write` |
| 6 | the intake was actually built | `onto_object_index` | objects per type |
| 7 | the pointer path works | `onto_object_graph` on a bound label; `onto_object_show` on the package and the label | `identifies` to the package; `menge` on the package; no `menge` on the label |
| 8 | a human can bind with a scan | the scan as that account, then a read-back | one free label became `gebunden` |
| 9 | print and reprint behave | the PDF, plus counts for the charge | a sheet was opened; reprint created no new labels |
| 10 | a manager booking of putaway, pick, relocate, count and one rebind | `onto_object_execute_action` then `onto_object_show` | `menge`, movement links, new `identifies` |
| 11 | the money claim | `onto_credit_balance` | the balance, measured now |

`onto_object_show` answers **404 "object not found or no access"** for objects in
a scope you are not a member of. That is fail-closed, not an error to work around.

## Phase gates

Do not enter phase N+1 while the proof of phase N is missing.

- **Phase 0 unfinished** → you have scopes but no 403 test or no type quote.
- **Phase 1 unfinished** → you have objects but no free charge and no opened PDF.
- **Phase 2 unfinished** → you have labels but no quoted `identifies` edge.
- **Phase 3 unfinished** → staff accounts exist but no staff scan bind.
- **Phase 4 unfinished** → binds work but the log or the list was not quoted.
- **Phase 5 unfinished** → labels work but the four bookings or the rebind were not quoted.

## Status vocabulary

| Say this | Only when |
|---|---|
| "Stage 0 of 5 complete" | the three scopes, the type quote, the functions and the 403 test are quoted |
| "Stage 1 of 5, 60 %" | object counts are quoted and the missing pieces are named |
| "Blocked: <reason>" | a stop rule fired; name the tool, the status code and the response |
| "Configured" | the acceptance scenario ran end to end and its steps are quoted |

Never: "done", "finished", "everything is set up", "ready to use" without the
acceptance result.

The acceptance scenario has **38 steps** (0.1 … 5.8) and **14 negative tests**
(N1 … N14). Those counts are stated there; do not restate them from memory.

## The failure patterns this file is meant to catch

1. **Objects in one scope, "three-scope structure built".** The three suffixes
   must appear in `ontouser_scope_index`.
2. **A quantity on the label.** If the report says the package holds 10 kg, that
   number must be read from the package.
3. **A bind reported from the write response only.** Without a graph read-back
   the edge is a guess.
4. **A stock action that points at a function in another scope.** The first
   booking then returns 403 and no movement is written.
5. **Credit arithmetic from memory** instead of `onto_credit_balance`.
6. **`menge` edited by hand** instead of booking a movement.
