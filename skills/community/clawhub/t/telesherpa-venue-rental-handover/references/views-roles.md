# Views, start cards and roles — venue rental and handover

## 1. Rights

This skill describes the **manager path**.

| Account | `<company>_master` | `<company>_venue` | `<company>_team` |
|---|---|---|---|
| Manager / owner (builds the workspace) | R W M | R W M | R W M |

Notes:

- Bookings, protocols and defects are stored in the venue scope. The team door
  holds views, start cards and the forms; writes go through the scope bridge
  (`result_scope_id` = venue).
- Do not grant extra rights "so a view works".
- The scope is the lock. A hirer who should see only their own booking needs
  their own scope, agreed at intake — not a list filter.
- A caretaker or further board members added later receive the rights the
  intake names. Do not widen rights as a workaround.

## 2. Shared columns, sorting and row actions

Booking lists (`bookings_open`, `handovers_upcoming`, `returns_overdue` and
their team counterparts):

| Column | Source |
|---|---|
| `udid` (first, **hidden**) | system `udid`, `hidden: true` |
| Venue | link `concerns`, forward, linkvalue `ofAsset`, system name |
| Room | `roomName` |
| Hirer | `hirerName` |
| Handover | `startDate` |
| Return | `dueDate` |
| Status | `orderStatus` |

Sort upcoming handovers by `startDate` ascending, and open bookings and
overdue returns by `dueDate` ascending. Object type `serviceOrder`. Do not set
`data_scope_id` (person-binding hides unassigned bookings).

The hidden `udid` column is required so row actions know which booking they
belong to. `row_actions` on the booking lists:

- a detail link, label in the intake language, icon `eye-open`, URL
  `ontouser/object/show/{udid}`
- `record_handover` (intake-language label, icon `edit`)
- `record_return` (intake-language label, icon `edit`)

The defects list uses the same hidden `udid` column and the same venue column,
then short description (`description`) and due date, plus the detail link only.

## 3. Manager views (venue scope)

All set `view_config.access.require` to `write`. Scope of the data:
`<venue_scope_name>`. View filter operators are `!=`, `<`, `>=`, `<=`.
`{today}` and `{today+14}` or `{today+30}` (the number agreed at intake) are stored as placeholders; do not replace them with
a fixed date, and do not store the letter N. The upcoming
handover list is a fixed window, not a navigable calendar.

| Key | Extra filter |
|---|---|
| `bookings_open` | `orderStatus != done` **and** `orderKind = venueBooking` |
| `handovers_upcoming` | `orderStatus = open`, `orderKind = venueBooking`, `startDate >= {today}` and `startDate <= {today+14}` (or `{today+30}` as agreed) |
| `returns_overdue` | `orderStatus != done`, `orderKind = venueBooking` and `dueDate < {today}` |
| `defects` | `orderKind = defect` and `orderStatus != done` |

Open-booking lists must restrict `orderKind` to `venueBooking` so protocols and
defects do not appear as bookings.

## 4. Team counterparts and start cards

Same filters, columns, sort and row actions as the manager views they pair
with. Data still comes from the venue scope (name it in the view; do not set
`data_scope_id`). Set `access.require` to `<venue_scope_id>` on the four list
counterparts. Create these **before** the start cards.

| Key | Counterpart of |
|---|---|
| `team_bookings_open` | `bookings_open` |
| `team_handovers_upcoming` | `handovers_upcoming` (same `{today}` … `{today+14}` or `{today+30}` window) |
| `team_returns_overdue` | `returns_overdue` |
| `team_defects` | `defects` |
| `team_venues` | — venue list for `report_defect` (below) |

`team_venues` is a block view of `building` in the master scope (and `space`
only when that type is in use and confirmed). It has **no** `access.require`.
Its label is the same as the report-defect action (intake language).

Create start cards with `onto_startcard_save` in `<team_scope_id>`. Each
`iface` / URL must be a **team** view. A card that points at a venue-scope
view is rejected (HTTP 400).

| sort | `iface` | URL |
|---|---|---|
| 1 | `team_handovers_upcoming` | `/ontouser/interface/show/team_handovers_upcoming` |
| 2 | `team_returns_overdue` | `/ontouser/interface/show/team_returns_overdue` |
| 3 | `team_bookings_open` | `/ontouser/interface/show/team_bookings_open` |
| 4 | `team_defects` | `/ontouser/interface/show/team_defects` |
| 5 | `team_venues` | `/ontouser/interface/show/team_venues` |

Titles are in the intake language (see [country-de.md](country-de.md) when that
language is German). Read `onto_startcard_index` and quote the cards in this
order.

## 5. Browser checks (manager)

- On the start page: the five cards in the order above, each opening the
  **team** view.
- Every booking row shows the venue name (`ofAsset`).
- `record_handover` and `record_return` open their **forms** from the list and
  from the booking page.
- Saving a handover without a result, a photo, a key note or a date is refused;
  the booking is unchanged.
- A successful handover save creates a `handoverProtocol` protocol linked
  `ofOrder`, with the photo and both signatures (`handedoverby`, `receivedby`) on the protocol, and leaves the
  booking `inProgress`.
- A successful return save creates a `returnProtocol` protocol linked `ofOrder`,
  with the photo and both signatures on the protocol, and the booking's
  `orderStatus` is the value you read back from the function (expected: `done`,
  so the booking leaves the open lists).
- `report_defect` on a venue creates one open defect, visible under Defects,
  not under All open bookings.
