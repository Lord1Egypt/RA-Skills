# Glossary

Terms as this skill uses them. Keys stay verbatim in calls.

## Key concepts

### Team door

The team scope (`_<slug>_team`). Start cards, the manager-facing lists used in
daily work, and both forms (record inspection, report defect) live here.
Inspection, protocol and defect *objects* live in the maintenance scope and
are reached through the views and through the scope bridge
(`action.result_scope_id`).

### Maintenance scope

The work scope (`_<slug>_maintenance`). It holds `serviceOrder` rows (duties,
protocols and defects), the property definitions, the manager views, the
function `apply_inspection` and its triggers, and is the `result_scope_id` of
both actions.

### Inspection duty (type `serviceOrder`)

An open order is the source of truth for a recurring deadline: `dueDate`,
`intervalDays`, optional `intervalKm`, `kind`, `orderKind=scheduledInspection`
(or `contractMaintenance`), `lastDone`, `result`. There is no second
requirement type. Recording an inspection updates this same row and leaves it
open.

### Inspection protocol (same type, `orderKind=inspectionProtocol`)

The form answer created by `record_inspection`. It is a `serviceOrder` with
`orderStatus=done`, linked to the duty with `concerns` / `ofOrder`. The result,
note, photos and signature are stored on this protocol. It does not appear in
the open, overdue or 30-day lists.

### Defect (same type, `orderKind=defect`)

A defect is also a `serviceOrder`, created by `report_defect` on an asset. It
appears in the defects view, not in all open inspections.

### Asset

A master object the duty or defect concerns: `car`, `device`, `tool`, `machine`
or `building`. The order points at it with `concerns` and linkvalue `ofAsset`.

### `concerns` / `ofAsset`

The link from a duty or defect to its asset. The value `ofAsset` must be set on
the edge, or the asset column in the lists stays blank.

### `concerns` / `ofOrder`

The link from a protocol to the open duty it belongs to. The function
`apply_inspection` follows this edge to update the duty.

### `record_inspection`

A `form_answer` action on `serviceOrder`, bound to a formdef (result, optional
note, photos, signature, inspection date, optional next due date). Saving
creates a protocol and, through `apply_inspection`, sets `result`, `lastDone`,
`dueDate` and optionally `inspectionNote` on the duty. Leaves the duty's
`orderStatus` unchanged (open or in progress).

### `apply_inspection`

The function that writes the recorded values back to the duty. If
`nextduedate` is a `YYYY-MM-DD` date, that value becomes `dueDate`; otherwise
`dueDate` is `lastdone` plus the duty's `intervalDays`. Insert and update
triggers on the protocol run it.

### `report_defect`

A form action on an asset. The answer is a new `serviceOrder` in the maintenance
scope with `orderKind=defect`, linked `concerns` / `ofAsset`.

### 30-day window

The "due in 30 days" view is a fixed filter: `dueDate >= {today}` and
`dueDate <= {today+30}`. The placeholders are stored as written and evaluated
when the view runs. The window is not a navigable period.

### Overdue

A list of open orders whose `dueDate` is before `{today}`. The placeholder is
stored as `{today}` and is evaluated when the view runs.

## Keys (verbatim)

| Key | Meaning |
|---|---|
| `dueDate` | next due date on the duty (date) |
| `intervalDays` | calendar interval in days (int) |
| `intervalKm` | optional kilometre interval (int) |
| `lastDone` | date the inspection was last recorded, on the duty (date) |
| `kind` | inspection kind (option value, English) |
| `orderKind` | `scheduledInspection` \| `defect` \| `contractMaintenance` \| `inspectionProtocol` |
| `result` | `pass` \| `defect` |
| `inspectionNote` | optional note written to the duty |
| `orderStatus` | platform status; duties stay `open` or `inProgress`; protocols are `done` |
| `assignedTo` | text; the action may set the executing user's e-mail |
| `lastdone` | form widget key for the inspection date (lowercase) |
| `nextduedate` | form widget key for the next due date (lowercase) |
| `inspResult` | function input for the inspection result (avoids colliding with `{result}`) |
| `ofAsset` | linkvalue on `concerns` from a duty or defect to its asset |
| `ofOrder` | linkvalue on `concerns` from a protocol to its duty |
| `result_scope_id` | scope bridge: where the written object lands |
