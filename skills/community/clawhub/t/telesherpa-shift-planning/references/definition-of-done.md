# Definition of Done — the audit before any status report

This file exists because a real build was reported as "everything is set up" while it held
six objects in one scope, no view, no action and no trigger. The report was not a lie in
the narrow sense — every UDID it listed existed. It was a status without a definition of
done, and there was nothing in the skill to measure it against.

Read this before you write a progress or completion message.

## The one sentence that replaces "done"

> The workspace is configured when a person who has never seen the build can plan a week,
> publish it, and have staff see their own shifts, file a request and clock in — without
> asking anyone.

Anything that cannot be traced to that sentence is not part of "done".

## The audit — one call per line, quote the value (twelve checks)

Run these in order. Keep the numbers; they go into the report verbatim.

| # | What it proves | Call | What you quote |
|---|---|---|---|
| 1 | the three scopes exist | `ontouser_scope_index` | the three names with their suffixes and `can_manage_scope` |
| 2 | the scopes are populated and who is in them | `onto_scope_index` | `obj_count`, `user_count`, `manager_count` per scope |
| 3 | the customer-specific values exist | `onto_property_def_index` | count of entries whose `scope_id` is your scope; the option values for station and contract type |
| 4 | something is visible to a human, and the start card is registered | `onto_settings_list` with `scope_id`, `onto_startcard_index` | number of views per scope; the start card row ("My shifts") |
| 5 | buttons exist and are gated | `onto_actiondef_list` | count; for each, `require_scope_write` and the scope list |
| 6 | automation exists | `onto_trigger_index` | count and the scope list |
| 7 | the intake was actually built | `onto_object_index` | objects per type |
| 8 | the staff path works | `onto_object_graph` on a published shift | the `worksShift` edge with person UDID |
| 9 | a human can work with it | the member view as that account | one own shift visible, one colleague's shift **not** visible |
| 10 | time tracking works | `ontouser_object_show` on the `serviceVisit` of a clock-in, the change-log view | start/end/break on the right day; a correction shows reason and old → new |
| 11 | the payroll export is usable | the CSV, opened and read | one row per person with planned and actual hours and the minijob warning |
| 12 | the money claim | `onto_credit_balance` | the balance, measured now |

`onto_object_show` answers **404 "object not found or no access"** for objects in a scope
you are not a member of. That is the platform working as designed (fail-closed), not an
error to work around: never grant yourself a right to make an audit possible.

## Phase gates

Do not enter phase N+1 while the proof of phase N is missing. In practice:

- **Phase 0 unfinished** → you have scopes but no property definitions and no 403 test.
- **Phase 1 unfinished** → you have objects but no view and no published shift.
- **Phase 2 unfinished** → you have forms but no request that ever reached an inbox.
- **Phase 3 unfinished** → staff accounts exist but no staff has seen a shift.
- **Phase 4 unfinished** → clock-in works in theory but no object was written.

## Status vocabulary

| Say this | Only when |
|---|---|
| "Stage 0 of 4 complete" | the three scopes, the property definitions and the 403 test are quoted |
| "Stage 1 of 4, 60 %" | object counts are quoted and the missing pieces are named |
| "Blocked: <reason>" | a stop rule fired; name the tool, the status code and the response |
| "Configured" | the acceptance scenario ran end to end and its steps are quoted |

Never: "done", "finished", "everything is set up", "ready to use" without the acceptance
result.

## The failure patterns this file is meant to catch

Each of these was observed in a real run, not invented:

1. **Six objects, one scope, "three-scope structure built".** If the report names a
   structure, the structure must appear in `ontouser_scope_index`. It did not.
2. **A link that cannot exist.** `assignedTo` is defined **room → person**; the shift is
   bound to its person by `worksShift`. A link named in a report without a read-back is a
   guess.
3. **Objects named by hand** (`shift_2026_11_15_marco`) instead of the agreed pattern —
   the naming pattern exists so a manager can read a list; it is a requirement, not taste.
4. **No view, no action, no trigger, and no mention of it.** The report listed what
   existed, never what was missing. Missing items belong in the report; they are the
   substance of a status.
5. **Credit arithmetic from memory** ("100 cost, 45 credited, 55 consumed") instead of the
   balance read from `onto_credit_balance`.

## For the platform operator

If this audit has to be run by hand for every build, most agents will skip it. A single
read-only tool — `workspace_audit(scope_id)` returning the twelve numbers above as one JSON
object — would make "are you finished?" a number the agent has to quote, instead of a
paragraph it can write. Until then this file is the substitute.
