# Phase 1 — sites, people, assets, recurring service orders

**Goal:** the master data and one open `serviceOrder` per agreed inspection duty,
each linked to its asset with `concerns` / `ofAsset`. No views or actions yet
(that is phase 2).

**Input:** closed phase 0; intake sections A, C and D answered (kinds, intervals,
naming, sites).

**Budget:** live `create_object` and `create_link` prices for every row you
actually create. Test objects carry `TEST-1-` in name and `external_id`. One
write at a time; read back after each create.

Placeholders: `<master_scope_id>`, `<maintenance_scope_id>`, asset and order
UDIDs as returned (always lower case; never publish them).

---

## 1. Definitions

### 1.1 Master objects

Reuse from shift-planning where the intake says so. Otherwise create in
`_master`:

| Type | What to create | Notes |
|---|---|---|
| `organisation` | the business; optionally a contractor (name only) | no commercial terms on master |
| `building` | one object per site | link `bestehtAus` from the business if you use the site tree |
| `person` | people named in the intake | basic fields only (name, login e-mail) |
| `car`, `device`, `tool`, `machine` | the assets in intake 3 | use the catalogue type that fits; do not store a device as a `tool` |

Comfort date fields that a catalogue type may already have on an asset are not
the duty. Leave them alone unless the intake asks to fill them as a mirror.

### 1.2 Recurring service orders

Create in `_maintenance`. One open order per asset and kind.

| Field | Value |
|---|---|
| `name` | from the naming pattern (intake 14) |
| `orderKind` | `scheduledInspection` (or `contractMaintenance` for a contractor duty) |
| `orderStatus` | `open` |
| `kind` | one of the phase 0 values |
| `dueDate` | the next due date (`YYYY-MM-DD`) |
| `intervalDays` | calendar interval from the intake |
| `intervalKm` | only when the intake gives a kilometre interval |

Link each order to its asset:

```json
{
  "linktype": "concerns",
  "linkvalue": "ofAsset",
  "source": "<serviceOrder_udid>",
  "target": "<asset_udid>"
}
```

Set `linkvalue` to `ofAsset` **when you create the edge**. If a read-back shows
an empty value, update that same edge (`onto_object_update_link`); do not add a
second `concerns` link. After each link, `onto_object_graph` (or
`onto_object_show`) must show exactly one `concerns` edge, value `ofAsset`, to
the intended asset.

## 2. Recipe

1. Create or reuse the business, site and people. Read each back.
2. Create the assets, one at a time. Read each back (name, type, scope).
3. Create the service orders, one at a time, with the fields in 1.2. Read
   `dueDate`, `intervalDays`, `kind`, `orderKind`, `orderStatus` from
   `onto_object_show` — the create response is not enough.
4. Create the `concerns` / `ofAsset` edge, one at a time. After a timeout, read
   the graph and only create edges that are still missing.
5. Build three buckets from the due dates and today's date (Europe/Berlin):
   overdue (`dueDate` before today), due within 30 days, later. Write the
   counts into the run log; phase 2 will compare the views to these numbers.

## 3. Checks via MCP

- Object counts per type match the intake (and the run log).
- Every service order reads back with `orderStatus=open`, a `dueDate`,
  `intervalDays`, `kind` and `orderKind`.
- Every service order has exactly one `concerns` edge with `linkvalue=ofAsset`
  to the intended asset in master.
- The overdue / within-30-days / later counts are written down.

## 4. Checks in the browser (manager)

Open a sample asset and a sample order. Confirm the name, the due date and that
the order shows its asset. Lists are built in phase 2, so do not expect start
cards yet.

## 5. Phase gate

Quote: counts per type; one order with `dueDate`, `kind`, `orderKind` and a
single `ofAsset` edge; the three due-date bucket counts. If a duty has no
`ofAsset` edge, phase 1 is not closed.

## 6. Typical errors

- Links created in parallel; a timeout leaves some edges missing or duplicated.
  Always read the graph before you retry.
- `concerns` created without `ofAsset`; the object header shows the asset, the
  list column later does not.
- `dueDate` written as a date-time. Use `YYYY-MM-DD`.
- Two open scheduled orders of the same kind on one asset, or a duty created
  in the master scope.
- An existing due date overwritten because `onto_object_show` was skipped and
  the create payload was sent again.
