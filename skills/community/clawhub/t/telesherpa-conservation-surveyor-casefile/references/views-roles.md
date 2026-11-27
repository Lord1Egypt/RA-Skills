# Views, start cards and roles — conservation and surveyor case file

## 1. Rights

This skill describes the **manager path**.

| Account | `<company>_master` | `<company>_cases` | `<company>_team` |
|---|---|---|---|
| Manager / owner (builds the workspace) | R W M | R W M | R W M |

Notes:

- Cases and protocols are stored in the cases scope. The team door holds views,
  start cards and the form; writes go through the scope bridge
  (`result_scope_id` = cases).
- Do not grant extra rights "so a view works".
- The scope is the lock. A client who should see only their own cases needs
  their own scope, agreed at intake — not a list filter.
- Studio colleagues added later receive the rights the intake names. Do not
  widen rights as a workaround.

## 2. Shared columns, sorting and row actions

Lists of cases (`cases_open`, `cases_overdue`, `cases_due_window` and their
team counterparts):

| Column | Source |
|---|---|
| `udid` (first, **hidden**) | system `udid`, `hidden: true` |
| Object | link `concerns`, forward, linkvalue `ofAsset`, system name |
| Kind | `caseKind` |
| Due date | `dueDate` |
| Interval (days) | `intervalDays` |

Sort by `dueDate` ascending. Object type `serviceOrder`. Do not set
`data_scope_id` (person-binding hides unassigned cases).

The hidden `udid` column is required so row actions know which case they belong
to. `row_actions` on the case lists:

- a detail link, label in the intake language, icon `eye-open`, URL
  `ontouser/object/show/{udid}`
- `record_survey` (intake-language label, icon `edit`)

## 3. Manager views (cases scope)

All set `view_config.access.require` to `write`. Scope of the data:
`<cases_scope_name>`. View filter operators are `!=`, `<`, `>=`, `<=`.
`{today}` and `{today+14}` or `{today+30}` (the number agreed at intake) are stored as placeholders; do not replace them with
a fixed date, and do not store the letter N. The due-window list
is a fixed window, not a navigable calendar.

| Key | Extra filter |
|---|---|
| `cases_open` | `orderStatus != done` **and** `orderKind = caseFile` |
| `cases_overdue` | `orderStatus != done` and `orderKind = caseFile` and `dueDate < {today}` |
| `cases_due_window` | `orderStatus != done`, `orderKind = caseFile`, `dueDate >= {today}` and `dueDate <= {today+14}` (or `{today+30}` as agreed) |

Open-case lists must restrict `orderKind` to `caseFile` so survey protocols do
not appear as cases.

## 4. Team counterparts and start cards

Same filters, columns, sort and row actions as the manager views they pair
with. Data still comes from the cases scope (name it in the view; do not set
`data_scope_id`). Set `access.require` to `<cases_scope_id>` on the list
counterparts. Create these **before** the start cards.

| Key | Counterpart of |
|---|---|
| `team_cases_open` | `cases_open` |
| `team_cases_overdue` | `cases_overdue` |
| `team_cases_due_window` | `cases_due_window` (same `{today}` … `{today+14}` or `{today+30}` window) |

Create start cards with `onto_startcard_save` in `<team_scope_id>`. Each
`iface` / URL must be a **team** view. A card that points at a cases-scope
view is rejected (HTTP 400).

| sort | `iface` | URL |
|---|---|---|
| 1 | `team_cases_overdue` | `/ontouser/interface/show/team_cases_overdue` |
| 2 | `team_cases_due_window` | `/ontouser/interface/show/team_cases_due_window` |
| 3 | `team_cases_open` | `/ontouser/interface/show/team_cases_open` |

Titles are in the intake language (see [country-de.md](country-de.md) when that
language is German). Read `onto_startcard_index` and quote the cards in this
order.

## 5. Browser checks (manager)

- On the start page: the three cards in the order above, each opening the
  **team** view.
- Every row shows the object name (`ofAsset`).
- The row button `record_survey` opens the **form** (result, findings, photos,
  signature, optional client confirmation, survey date, optional next due date), from the list and from the
  case page.
- Saving without a result, findings, a photo or a survey date is refused; the
  case is unchanged.
- Saving with those fields and an **empty** next due date succeeds. The case
  stays open, `lastDone` is the survey date, `dueDate` is that date plus
  `intervalDays` when the interval is set (otherwise the existing due date is
  unchanged), and a protocol (`orderKind=surveyProtocol`) is linked `ofOrder`
  with the photo, the surveyor signature and, when used, the client confirmation on it.
- Saving with a **typed** next due date uses that date as `dueDate`, not the
  interval.
