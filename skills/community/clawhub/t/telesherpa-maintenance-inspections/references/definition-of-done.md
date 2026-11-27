# Definition of Done — the audit before any status report

Read this before you write a progress or completion message.

## The one sentence that replaces "done"

> The workspace is configured when a person who has never seen the build can open
> the start cards, see overdue and upcoming inspections with their asset names,
> record an inspection (result, photo, signature, date, and either a typed next
> due date or none) so the same order stays open with the new due date, and
> report a defect on an asset — without asking anyone.

Anything that cannot be traced to that sentence is not part of "done".

## The audit — one call per line, quote the value

Run these in order. Keep the numbers; they go into the report verbatim. The table
is the same as in [SKILL.md](../SKILL.md).

| # | What it proves | Call | What you quote |
|---|---|---|---|
| 1 | Three scopes, you are manager | `ontouser_scope_index` | the three names with the agreed suffixes |
| 2 | Size of each scope | `onto_scope_index` | `obj_count`, `user_count`, `manager_count` |
| 3 | Fields on `serviceOrder` | `onto_type_show` in the maintenance scope | `dueDate`, `intervalDays`, `lastDone`, `kind`, `orderKind` (including `inspectionProtocol`), `result`, `inspectionNote` |
| 4 | Views and start cards | `onto_interface_index`, `onto_startcard_index` | four work lists, five team views, five cards pointing at team views |
| 5 | Actions, form, function, triggers | `onto_actiondef_list`, `show_formdef`, function and trigger index/show | `record_inspection` (`form_answer`, no `orderStatus` write on the duty), `apply_inspection`, both triggers, `report_defect` |
| 6 | Object counts | `onto_object_index` | counts per type vs the intake |
| 7 | A duty points at its asset | `onto_object_graph`, `onto_object_show` | one `concerns` / `ofAsset` edge; `dueDate` on the order |
| 8 | A recorded inspection stays open | form in the browser, then `onto_object_show` / graph | `result`, `lastDone`, new `dueDate` (typed or computed), `orderStatus` still `open`, protocol `ofOrder` |
| 9 | A defect is a separate order | the form action, then the views | one defect on the asset; not in all open inspections |
| 10 | The balance you mention | `onto_credit_balance` | the figure you just read |

If a line cannot be filled, the status is the missing line, not a summary.

## Phase gates

A phase is closed only when its gate in the phase file is quoted. Do not start
phase 1 while phase 0 is open, or phase 2 while phase 1 is open.

The workspace is configured only when
[acceptance-scenario.md](acceptance-scenario.md) has run end to end once: **17
steps** (0.1 … 2.8) and **2 negative tests** (N1–N2). Those counts live in that file
and in [SKILL.md](../SKILL.md); do not restate them from memory.

## Language of the report

Use the report shape in [SKILL.md](../SKILL.md). Forbidden lines: "everything is
set up" and "done". Name the stage as "stage X of 2 (0–2)".
