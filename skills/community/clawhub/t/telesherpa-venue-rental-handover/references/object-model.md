# Object model — venue rental and handover

## 1. Scopes

| Scope name | Purpose | Holds | Who works here |
|---|---|---|---|
| `<company>_master` | master data | business, venues, people (basic fields) | managers write |
| `<company>_venue` | rental work | `serviceOrder` rows (bookings, protocols and defects), property definitions, manager views, functions and triggers, `result_scope_id` of the actions | managers |
| `<company>_team` | team door | start cards, team counterparts of the lists, the forms and the report-defect venue view | managers (daily UI) |

Rules:

- Names: `a-z0-9_`, max 30 characters. Check the longest one (`<company>_venue`).
- The scope is the lock. Never rely on a view filter to hide data.
- **Reuse.** If shift-planning already created `_master` and `_team` for this
  business, add only `_venue` and keep the existing people and sites.
- **Links cross scopes.** `concerns` / `ofAsset` runs from a `serviceOrder` in
  venue to a building (or, when confirmed, a `space`) in master.
- Placeholders such as `<venue_scope_id>` stay in the run log, not in public text.

## 2. Types to activate

On `_master`: `organisation`, `building`, `person`. If shift-planning already
activates `space` for this business, keep `space` on the reused master.
On `_venue`: `serviceOrder`.
On `_team`: no extra master types; views, start cards and the forms live here.

Read each type with `onto_type_show` before you activate it. A member does not
create types. If a required type is missing, stop and file
`ontouser_service_request`. Activate with `ontouser_scope_types_set` (that call
**replaces** the list; include every type the scope must keep).

The default venue type is `building`. A hall or room already modelled as a
`space` under a building (`bestehtAus`, as in shift-planning) may be used as
the booking's asset only after `onto_link_index` confirms that `concerns` /
`ofAsset` allows `serviceOrder` → `space`. If that pair is not allowed, store
the room name on the booking (`roomName`) and link `ofAsset` to the `building`.
Do not invent a linkvalue.

## 3. Properties on `building` (master)

Create these only for fields the intake actually uses.

| Key | Value type | Purpose |
|---|---|---|
| `inventoryNote` | string | standing inventory list the caretaker already uses |
| `keySetDefault` | string | usual key set or key-board hook for this venue |

Platform name and description fields already on the type may be used; do not
redefine them.

## 4. Properties on `serviceOrder` (venue scope)

| Key | Value type | Purpose |
|---|---|---|
| `startDate` | date | handover date (source of truth for upcoming-handover lists) |
| `dueDate` | date | return date (source of truth for overdue-return lists) |
| `lastDone` | date | date of the last recorded handover or return |
| `roomName` | string | room or hall name when the asset is the building |
| `hirerName` | string | hirer or club name as given at intake |
| `hirerContact` | string | contact as given at intake |
| `keySet` | string | keys handed over |
| `rentalAmount` | string | rental figure stored on the booking |
| `depositAmount` | string | deposit figure stored on the booking |
| `orderKind` | options | `venueBooking` / `handoverProtocol` / `returnProtocol` / `defect` |
| `result` | options | `pass` / `defect` |
| `inspectionNote` | string | inventory, meter or condition note written back to the booking |

Platform fields already on `serviceOrder` that this skill uses, not redefined:
`orderStatus` (`open` / `inProgress` / `done`), `description`, `task`,
`assignedTo`, `priority`, `startedAt`, `completedAt`.

A caretaker or chair is assigned with `assignedTo`. The hirer is stored as
text on the booking so this skill does not invent a second link to `person`.
People rows in master remain the address book the business already keeps.
Prices and deposits are stored fields; they are not a payment run.

One open `venueBooking` per hire. A key set is a text field on the booking and
on the handover protocol, not a separate key-cabinet product. Meter readings
are notes on the protocol (see [forms-actions.md](forms-actions.md)).

## 5. Link types

Confirm in `onto_link_index` before you depend on them. Invent none.

| Link | Direction | Linkvalue | Use |
|---|---|---|---|
| `concerns` | booking or defect → venue (`building`, or `space` only when confirmed) | `ofAsset` (set on the edge) | booking or defect to its venue |
| `concerns` | protocol → booking (both `serviceOrder`) | `ofOrder` (set on the edge) | handover or return protocol to its booking |
| `bestehtAus` | organisation → building (and building → `space` when that tree already exists) | — | site tree, same as shift-planning |

If `concerns` does not allow a pair you need, stop and file a service request.
