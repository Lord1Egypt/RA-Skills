# Phase 2 — views, start cards, record inspection, report defect

**Goal:** the four lists (work scope and team counterparts), five start cards on
the team door, `record_inspection` as a form with function and triggers, and
`report_defect` on an asset. A manager can complete the sentence in
[definition-of-done.md](definition-of-done.md).

**Input:** closed phase 1; bucket counts from that phase; intake 13 (label
language) and 18 (who logs in as manager).

**Budget:** definition writes (views, forms, actions, function, triggers) plus
the browser form saves in the acceptance run. Read each definition back before
you rely on it. Save the current JSON before you change an action, a form, a
function, a trigger or a view.

Placeholders: `<master_scope_id>`, `<maintenance_scope_id>`, `<team_scope_id>`,
`<master_scope_name>`, `<maintenance_scope_name>`.

---

## 1. Definitions

### 1.1 Shared columns, sorting and row actions

Inspection lists (`inspections_open`, `inspections_overdue`,
`inspections_due_30` and their team counterparts):

| Column | Source |
|---|---|
| `udid` (first, **hidden**) | system `udid`, `hidden: true` |
| Asset | link `concerns`, forward, linkvalue `ofAsset`, system name |
| Kind | `kind` |
| Due date | `dueDate` |
| Interval (days) | `intervalDays` |

Sort by `dueDate` ascending. Object type `serviceOrder`. Do not set
`data_scope_id`.

The hidden `udid` column is required so row actions know which order they
belong to. `row_actions` on the six inspection and defect lists:

- a detail link, label in the intake language, icon `eye-open`, URL
  `ontouser/object/show/{udid}`
- `record_inspection` (intake-language label, icon `edit`) on the four
  inspection lists (not on the defects lists)

The defects list uses the same hidden `udid` column and the same asset
column, then short description (`description`), kind and due date, plus the
detail link only.

### 1.2 Manager views (maintenance scope)

All four set `view_config.access.require` to `write`. Scope of the data:
`<maintenance_scope_name>`.

| Key | Label (intake language) | Extra filter |
|---|---|---|
| `inspections_open` | All open inspections | `orderStatus != done` **and** `orderKind != defect` |
| `inspections_overdue` | Overdue | `orderStatus != done` and `dueDate < {today}` |
| `inspections_due_30` | Due in 30 days | `orderStatus != done`, `dueDate >= {today}` and `dueDate <= {today+30}` |
| `defects` | Defects | `orderKind = defect` and `orderStatus != done` |

View filter operators are `!=`, `<`, `>=`, `<=`. `{today}` and `{today+30}`
are stored as placeholders; do not replace them with a fixed date. The
30-day list is a fixed window, not a navigable period.

### 1.3 Team counterparts (team scope)

Same filters, columns, sort and row actions as the manager views they pair
with. Data still comes from the maintenance scope (name it in the view; do
not set `data_scope_id`). Set `access.require` to `<maintenance_scope_id>`
on the four list counterparts. Create these **before** the start cards.

| Key | Counterpart of |
|---|---|
| `team_inspections_open` | `inspections_open` (include `orderKind != defect`) |
| `team_inspections_overdue` | `inspections_overdue` |
| `team_inspections_due_30` | `inspections_due_30` (same `{today}` … `{today+30}` window) |
| `team_defects` | `defects` |
| `team_assets` | — asset list for `report_defect` (below) |

`team_assets` is a block view of `car`, `device`, `tool`, `machine` and
`building` in the master scope. It has **no** `access.require`. Its label is
the same as the report-defect action (intake language).

### 1.4 Start cards (team scope only)

Create with `onto_startcard_save` in `<team_scope_id>`. Each `iface` / URL must
be a **team** view. A card that points at a maintenance-scope view is rejected
(HTTP 400).

| sort | Title (intake language) | `iface` | URL |
|---|---|---|---|
| 1 | Overdue | `team_inspections_overdue` | `/ontouser/interface/show/team_inspections_overdue` |
| 2 | Due in 30 days | `team_inspections_due_30` | `/ontouser/interface/show/team_inspections_due_30` |
| 3 | All open inspections | `team_inspections_open` | `/ontouser/interface/show/team_inspections_open` |
| 4 | Defects | `team_defects` | `/ontouser/interface/show/team_defects` |
| 5 | Report defect | `team_assets` | `/ontouser/interface/show/team_assets` |

Read `onto_startcard_index` and quote the five cards in this order.

### 1.5 Form, action, function and triggers for `record_inspection`

This is one path: the form collects the values, the action creates a
protocol, the triggers run `apply_inspection`, and the function updates the
duty.

#### Form (team scope)

`answer_type` `serviceOrder`. Widget keys are stored as written; keep them
lowercase.

| Key | Widget | Required | Notes |
|---|---|---|---|
| `result` | select `pass` / `defect` | yes | |
| `note` | textarea | no | |
| `images` | `images` | yes | `max` 5; validation `min_count:1` |
| `signature` | `signature` | — | signature canvas; stored as a PNG on the protocol |
| `lastdone` | `datepicker`, `mode: date` | yes | inspection date, `YYYY-MM-DD` |
| `nextduedate` | `datepicker`, `mode: date` | no | next due date, `YYYY-MM-DD`; leave empty to use the interval |
| `orderKind` | select, only `inspectionProtocol` | yes | classifies the protocol |
| `orderStatus` | select, only `done` | yes | keeps the protocol off the open lists |

Do not put photos or a signature on action prompts. Those prompt types are
not accepted; they belong in this formdef.

#### Action `record_inspection`

Type `form_answer` on `serviceOrder`, bound to the form above. Create with
**exactly one** scope in `body.scopes` (the maintenance scope), then add the
team scope in a second save. `result_scope_id` is `<maintenance_scope_id>`.

Condition (operator `ne`, not `neq`): `orderStatus` is `open` or `inProgress`,
and `orderKind` `ne` `inspectionProtocol`.

Action props:

```json
{
  "orderKind": "inspectionProtocol",
  "orderStatus": "done",
  "assignedTo": "{current_user_email}"
}
```

Link: `concerns` with `linkvalue` `ofOrder` to `{object_udid}` (the duty the
button was run on). Protocol name, for example `Inspection {now}`. A comment
effect may record that an inspection was saved (do not put form field
placeholders in the comment; they are not action prompts).

`assignedTo={current_user_email}` is required when `result_scope_id` is set.

The protocol lands in the maintenance scope. It must not appear in the open,
overdue or 30-day lists (`orderStatus=done`).

#### Function `apply_inspection`

Create in the maintenance scope. Inputs:

| Key | Type | Required | Meaning |
|---|---|---|---|
| `objekt` | object | yes | the **duty**, not the protocol |
| `inspResult` | string | yes | inspection result (`pass` / `defect`) |
| `note` | string | no | becomes `inspectionNote` |
| `lastdone` | datetime | yes | inspection date |
| `nextduedate` | datetime | no | typed next due date, if any |

The input is named `inspResult` because `{result}` in the effects is the
**function result** (the computed due date), not the inspection result.

Body: if `nextduedate` is not empty **and** matches `^[0-9]{4}-[0-9]{2}-[0-9]{2}`,
use that value; otherwise `date_add(lastdone, intervalDays)`, where
`intervalDays` is read from the duty (`objekt`).

Effects, `set_property` on `objekt` (the duty):

```json
{
  "result": "{inspResult}",
  "inspectionNote": "{note}",
  "lastDone": "{lastdone}",
  "dueDate": "{result}"
}
```

Do **not** set `orderStatus`, `completedAt` or `description` on the duty.
After a successful run the duty is still `open` (or still `inProgress`),
`result` and `lastDone` are set, and `dueDate` is either the typed date or
the inspection date plus the interval. `result=defect` does not create a
second order.

#### Triggers

Both in the maintenance scope, object type `serviceOrder`, enabled.

| Key | Event | Condition | Effect |
|---|---|---|---|
| `on_inspection_recorded` | insert | `orderKind` `eq` `inspectionProtocol` | `run_function` `apply_inspection` |
| `on_inspection_recorded_update` | update | same, plus `changed`: `result`, `lastdone`, `nextduedate` | same function and inputs |

Function inputs on both triggers (placeholders = exact form widget keys):

```json
{
  "objekt": "{linked:concerns:ofOrder:udid}",
  "inspResult": "{result}",
  "note": "{note}",
  "lastdone": "{lastdone}",
  "nextduedate": "{nextduedate}"
}
```

`{linked:concerns:ofOrder:udid}` resolves the duty. `{result}` here is the
protocol's `result` field, not the function result.

### 1.6 Form and action `report_defect`

Form in the team scope, `answer_type` `serviceOrder`. Fields:

| Key | Required | Notes |
|---|---|---|
| `task` | yes | short title |
| `description` | yes | description of the defect |
| `orderKind` | — | fixed to `defect` |
| `orderStatus` | — | fixed to `open` |

Action type `form_answer`, object types `car`, `machine`, `tool`, `device`,
`building`. Create with `body.scopes` = `[<master_scope_id>]` and
`result_scope_id` = `<maintenance_scope_id>`, then add the team scope in a
second save. Bind the form. Props: `orderKind=defect`, `orderStatus=open`,
`assignedTo={current_user_email}`. Link: `concerns` with `linkvalue` `ofAsset`
to the asset the action was run on.

The new order lands in the maintenance scope, appears in `defects` /
`team_defects`, and must not appear in `inspections_open` /
`team_inspections_open`.

## 2. Recipe

1. Confirm no views, forms, actions, functions or triggers with these keys
   already exist (interface, form, action, function and trigger indexes).
2. Create `result` and `inspectionNote` if phase 0 did not (read back). Add
   `inspectionProtocol` to `orderKind` if it is missing.
3. Create the four manager views, one at a time. Read each back (filters,
   hidden `udid` column, `row_actions`, `access.require`, `{today}` /
   `{today+30}` on the 30-day view).
4. Create the form `record_inspection`; read it back (widget keys, required
   flags, `images` min/max, date mode).
5. Create the function `apply_inspection`; read it back (the `YYYY-MM-DD`
   guard, `date_add` fallback, effects do not touch `orderStatus`).
6. Create the two triggers; read them back (condition, `ofOrder` target,
   placeholders equal to the form keys).
7. Create the action `record_inspection` with one scope; read back; add the
   team scope; confirm type `form_answer`, the form binding, `assignedTo`,
   the `ofOrder` link, and condition operator `ne`.
8. Create the form `report_defect`; read it back; create the action with one
   scope; add the team scope; confirm the `ofAsset` link.
9. Create the five team views. Read each back (`access.require` on the four
   lists, none on `team_assets`, hidden `udid` and row actions on the lists).
10. Create the five start cards in the team scope. Read `onto_startcard_index`.
11. Smoke-test `record_inspection` in the browser on a `TEST-` order only
    after the form, function and triggers have been read back.

## 3. Checks via MCP

- Four manager views in the maintenance scope; four list counterparts plus
  `team_assets` in the team scope; filters, hidden `udid`, row actions and
  `access.require` as in 1.1–1.3.
- Five start cards in the team scope, in the order in 1.4, each `iface` a team
  view.
- `record_inspection`: type `form_answer`, form bound, scopes include
  maintenance and team, `result_scope_id` is maintenance, condition uses
  `ne`, props include `orderKind=inspectionProtocol`, `orderStatus=done` and
  `assignedTo`, link `concerns` / `ofOrder`.
- `apply_inspection` and both triggers present; trigger inputs use the form
  widget keys; the function accepts a next due date only as `YYYY-MM-DD`.
- `report_defect`: form in the team scope, action `result_scope_id` is
  maintenance, link `concerns` / `ofAsset`.

## 4. Checks in the browser (manager)

- On the start page: five cards in the order in 1.4. Each card opens the
  **team** view, not the work-scope URL.
- Counts: overdue, due in 30 days (from today through today + 30 days), all
  open inspections, defects — match the phase 1 buckets (adjusted for any
  inspection or defect you already recorded).
- Every row in the four lists shows the asset name.
- The row button `record_inspection` opens the **form** (result, note, photos,
  signature, inspection date, optional next due date), from the list and from
  the order page.
- Saving without a result or without an inspection date is refused; the duty
  is unchanged.
- Saving with a result, at least one photo, a signature, an inspection date
  and an **empty** next due date succeeds. The duty stays open, `lastDone` is
  the inspection date, `dueDate` is that date plus `intervalDays`, and a
  protocol (`orderKind=inspectionProtocol`) is linked `ofOrder` with the photo
  and signature on it. The duty leaves Overdue or Due in 30 days once the new
  due date is outside that list.
- Saving with a **typed** next due date uses that date as `dueDate`, not the
  interval.
- `record_inspection` with `result=defect` does not add a second defect order.
- `report_defect` on an asset creates one open defect, visible under Defects,
  not under All open inspections.

## 5. Phase gate

Quote: the start-card list, the four counts from the browser, one recorded
inspection with an empty next due date (`orderStatus`, `result`, `lastDone`,
computed `dueDate`, protocol `ofOrder`), one recorded inspection with a typed
next due date, one defect that is absent from all open inspections, and the
refused saves without a result and without an inspection date. Until those
lines are quoted, phase 2 is not closed.

## 6. Typical errors

- Action prompts used for photos or a signature → those types are not
  accepted; put them in the formdef and set `action.type=form_answer`.
- Action condition operator `neq` instead of `ne` → the button does not
  show.
- Missing hidden `udid` column → a list row action has no object and does
  not open the form.
- Empty `nextduedate` written through as the literal `{nextduedate}` because
  the function treated a placeholder as a date. Guard with the `YYYY-MM-DD`
  pattern; otherwise use `date_add`.
- Trigger placeholders in camelCase (`{lastDone}`, `{nextDueDate}`) → they
  do not match the stored widget keys and the values are not passed.
- `{result}` used as a function input name → it collides with the function
  result; the inspection result input is `inspResult`.
- `orderStatus=done` written onto the **duty** → the recurring row
  disappears from every list. Only the protocol is `done`.
- `ofOrder` missing on the protocol → the function cannot find the duty.
- `assignedTo` omitted on a `form_answer` with `result_scope_id` → HTTP 400.
- `ofAsset` missing on some edges → blank asset column on those rows.
- All open inspections missing `orderKind != defect` → the defect count leaks
  into that list.
- Start cards created before the team views, or pointed at work-scope keys →
  HTTP 400.
- Action create with several scopes → HTTP 400, nothing stored.
- 30-day window stored as a navigable period (`period_start` / `period_end`)
  instead of `{today}` / `{today+30}`.
