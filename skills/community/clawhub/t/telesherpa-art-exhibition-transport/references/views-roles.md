# Views, start cards and roles — art and exhibition transport

## 1. Rights

This skill describes the **manager path**.

| Account | `<company>_master` | `<company>_transport` | `<company>_team` |
|---|---|---|---|
| Manager / owner (builds the workspace) | R W M | R W M | R W M |

Notes:

- Jobs and protocols are stored in the transport scope. The team door holds
  views, start cards and the forms; writes go through the scope bridge
  (`result_scope_id` = transport).
- Do not grant extra rights "so a view works".
- The scope is the lock. A client who should see only their own jobs needs
  their own scope, agreed at intake — not a list filter.
- Drivers and office staff added later receive the rights the intake names.
  Do not widen rights as a workaround.

## 2. Shared columns, sorting and row actions

Lists of jobs (`jobs_open`, `jobs_overdue`, `jobs_due_window`, `jobs_in_progress`
and their team counterparts):

| Column | Source |
|---|---|
| `udid` (first, **hidden**) | system `udid`, `hidden: true` |
| Item | link `concerns`, forward, linkvalue `ofAsset`, system name |
| Tour code | `tourCode` |
| Crate | `crateCode` |
| Delivery date | `dueDate` |
| Status | `orderStatus` |

Sort by `dueDate` ascending. Object type `serviceOrder`. Do not set
`data_scope_id` (person-binding hides unassigned jobs).

The hidden `udid` column is required so row actions know which job they belong
to. `row_actions` on the job lists:

- a detail link, label in the intake language, icon `eye-open`, URL
  `ontouser/object/show/{udid}`
- `record_collection` (intake-language label, icon `edit`)
- `record_delivery` (intake-language label, icon `edit`)

## 3. Manager views (transport scope)

All set `view_config.access.require` to `write`. Scope of the data:
`<transport_scope_name>`. View filter operators are `!=`, `<`, `>=`, `<=`.
`{today}` and `{today+14}` or `{today+30}` (the number agreed at intake) are stored as placeholders; do not replace them with
a fixed date, and do not store the letter N. The due-window list
is a fixed window, not a navigable calendar.

| Key | Extra filter |
|---|---|
| `jobs_open` | `orderStatus != done` **and** `orderKind = transportJob` |
| `jobs_overdue` | `orderStatus != done` and `orderKind = transportJob` and `dueDate < {today}` |
| `jobs_due_window` | `orderStatus != done`, `orderKind = transportJob`, `dueDate >= {today}` and `dueDate <= {today+14}` (or `{today+30}` as agreed) |
| `jobs_in_progress` | `orderStatus = inProgress` and `orderKind = transportJob` |

Open-job lists must restrict `orderKind` to `transportJob` so protocols do not
appear as jobs.

## 4. Team counterparts and start cards

Same filters, columns, sort and row actions as the manager views they pair
with. Data still comes from the transport scope (name it in the view; do not
set `data_scope_id`). Set `access.require` to `<transport_scope_id>` on the
list counterparts. Create these **before** the start cards.

| Key | Counterpart of |
|---|---|
| `team_jobs_open` | `jobs_open` |
| `team_jobs_overdue` | `jobs_overdue` |
| `team_jobs_due_window` | `jobs_due_window` (same `{today}` … `{today+14}` or `{today+30}` window) |
| `team_jobs_in_progress` | `jobs_in_progress` |

Create start cards with `onto_startcard_save` in `<team_scope_id>`. Each
`iface` / URL must be a **team** view. A card that points at a transport-scope
view is rejected (HTTP 400).

| sort | `iface` | URL |
|---|---|---|
| 1 | `team_jobs_overdue` | `/ontouser/interface/show/team_jobs_overdue` |
| 2 | `team_jobs_due_window` | `/ontouser/interface/show/team_jobs_due_window` |
| 3 | `team_jobs_in_progress` | `/ontouser/interface/show/team_jobs_in_progress` |
| 4 | `team_jobs_open` | `/ontouser/interface/show/team_jobs_open` |

Titles are in the intake language (see [country-de.md](country-de.md) when that
language is German). Read `onto_startcard_index` and quote the cards in this
order.

## 5. Browser checks (manager)

- On the start page: the four cards in the order above, each opening the
  **team** view.
- Every row shows the item name (`ofAsset`).
- `record_collection` and `record_delivery` open their **forms** from the list
  and from the job page.
- Saving a collection report without a result, a photo or a date is refused;
  the job is unchanged.
- A successful collection save creates a `collectionReport` protocol linked
  `ofOrder`, with the photo and both signatures (`handedoverby`, `receivedby`) on the protocol, and leaves the job
  `inProgress`.
- A successful delivery save creates a `deliveryReport` protocol linked
  `ofOrder`, with the photo and both signatures on the protocol, and the job's
  `orderStatus` is the value you read back from the function (expected: `done`,
  so the job leaves the open lists).
