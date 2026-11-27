# Acceptance scenario (end to end, phases 0–2)

One continuous test with fixed, fictional start data and expected values. A fresh
agent runs it once from an empty account (or from an existing ExampleWorks
shift-planning master, if the intake says to reuse it); the paid run is measured
with [measurement.md](measurement.md). Every step names the **role** that performs
it and the **expected result**; a step passes only when the result is read back
(tool read or browser), not when the write call returned "OK".

The scenario has **17 steps** (0.1 … 2.8) and **2 negative tests** (N1–N2).
Both counts are stated only here and in [SKILL.md](../SKILL.md) /
[definition-of-done.md](definition-of-done.md). Do not restate them from memory.

- Business: **ExampleWorks**, slug `exampleworks` → scopes
  `exampleworks_master`, `exampleworks_maintenance`, `exampleworks_team`
  (reuse `_master` / `_team` if they already exist).
- All test objects carry the prefix `TEST-A-`. All addresses are `@example.com`
  in this document. These are not activatable human mailboxes. The checks in
  this file run as the **manager**. Never use real staff data.
- Dates below are relative to **the calendar day of the run** in Europe/Berlin.
  Compute `dueDate` values from that day; do not copy a date from a previous run.

## 1. Start data

### 1.1 Site and people (master)

| # | Type | Name |
|---|---|---|
| 1 | `organisation` | TEST-A-ExampleWorks |
| 2 | `organisation` | TEST-A-Contractor (name only) |
| 3 | `building` | TEST-A-Site North |
| 4 | `person` | TEST-A-Inspector, login `inspector@example.com` |

### 1.2 Assets (master)

| # | Type | Name |
|---|---|---|
| 1 | `car` | TEST-A-Vehicle 1001 |
| 2 | `car` | TEST-A-Vehicle 1002 |
| 3 | `device` | TEST-A-Drill |
| 4 | `device` | TEST-A-Cable reel |
| 5 | `tool` | TEST-A-Ladder 3m |
| 6 | `tool` | TEST-A-Extinguisher Yard |
| 7 | `tool` | TEST-A-Extinguisher Office |
| 8 | `machine` | TEST-A-Heating Site North |

### 1.3 Service orders (maintenance)

All `orderStatus=open`. `orderKind=scheduledInspection` except the heating row
(`contractMaintenance`). Link each to the asset in the name with `concerns` /
`ofAsset`. Intervals: 365 days, except periodic vehicle inspection 730 days.
Oil change also has `intervalKm=15000`.

| # | Name | kind | dueDate relative to run day | Bucket |
|---|---|---|---|---|
| 1 | TEST-A-occupationalSafetyCheck 1001 | `occupationalSafetyCheck` | today + 19 days | within 30 |
| 2 | TEST-A-periodicVehicleInspection 1001 | `periodicVehicleInspection` | today + 150 days | later |
| 3 | TEST-A-oilChange 1001 | `oilChange` | today − 27 days | overdue |
| 4 | TEST-A-occupationalSafetyCheck 1002 | `occupationalSafetyCheck` | today + 77 days | later |
| 5 | TEST-A-periodicVehicleInspection 1002 | `periodicVehicleInspection` | today + 24 days | within 30 |
| 6 | TEST-A-oilChange 1002 | `oilChange` | today + 105 days | later |
| 7 | TEST-A-electricalTest Drill | `electricalTest` | today + 15 days | within 30 |
| 8 | TEST-A-electricalTest Cable reel | `electricalTest` | today + 197 days | later |
| 9 | TEST-A-ladder Ladder 3m | `ladder` | today + 60 days | later |
| 10 | TEST-A-fireExtinguisher Yard | `fireExtinguisher` | today + 14 days | within 30 |
| 11 | TEST-A-fireExtinguisher Office | `fireExtinguisher` | today + 258 days | later |
| 12 | TEST-A-contractMaintenance Heating | `contractMaintenance` | today + 166 days | later |

Expected buckets **after phase 1, before any phase 2 execute:** overdue **1**
(oil change 1001), due in the 30-day window (`{today}` through `{today+30}`)
**4** (extinguisher yard, electrical test drill, occupational safety 1001,
periodic inspection 1002), later **7**, all open **12**, defects **0**.

## 2. Steps

### Phase 0

| # | Role | Step | Expected |
|---|---|---|---|
| 0.1 | Manager | Create or reuse the three scopes | `ontouser_scope_index` lists `exampleworks_master`, `exampleworks_maintenance`, `exampleworks_team`; the account is manager of all three |
| 0.2 | Manager | Activate the types in [phase0.md](phase0.md) | `ontouser_scope_types` quotes the active types on master and on maintenance |
| 0.3 | Manager | Create the property definitions | `onto_type_show` on `serviceOrder` in the maintenance scope quotes `dueDate` (date), `intervalDays`, `lastDone`, `kind`, `orderKind` (including `inspectionProtocol`), `result`, `inspectionNote`; each definition's `scope_id` is the maintenance scope |
| 0.4 | Manager | Confirm option values | `kind`, `orderKind` and `result` contain the English values from phase 0 |

### Phase 1

| # | Role | Step | Expected |
|---|---|---|---|
| 1.1 | Manager | Create the master objects in 1.1–1.2 | counts: organisation 2, building 1, person 1, car 2, device 2, tool 3, machine 1 |
| 1.2 | Manager | Read one asset of each class | `onto_object_show` quotes name, type and master scope |
| 1.3 | Manager | Create the twelve orders in 1.3 | each reads back `orderStatus=open`, the planned `dueDate`, `intervalDays`, `kind` and `orderKind` |
| 1.4 | Manager | Link each order `concerns` / `ofAsset` | `onto_object_graph` shows exactly one such edge per order, to the intended asset |
| 1.5 | Manager | Count the due-date buckets | overdue 1, within 30 days 4, later 7 |

### Phase 2

| # | Role | Step | Expected |
|---|---|---|---|
| 2.1 | Manager | Create the four work views and the five team views | filters, hidden `udid` column, row actions, sort and `access.require` match [phase2.md](phase2.md); `team_assets` has no `access.require` |
| 2.2 | Manager | Create the form, function, triggers and action for `record_inspection`, plus the five start cards in the team scope | form widget keys and required flags match phase 2; `apply_inspection` guards `nextduedate` as `YYYY-MM-DD`; both triggers target `{linked:concerns:ofOrder:udid}`; `onto_startcard_index` lists the cards in the order overdue, due in 30 days, all open inspections, defects, report defect; each `iface` is a team view |
| 2.3 | Manager | Open the start page in the browser | five cards in that order; each card opens the team view, not a work-scope URL |
| 2.4 | Manager | Open the four lists in the browser | overdue 1, due in 30 days 4 (from today through today + 30 days), all open 12, defects 0; every row shows its asset name; the defect filter keeps the open list at 12; the row button opens the record-inspection **form** |
| 2.5 | Manager | Run `report_defect` on TEST-A-Drill with a short description | one new `serviceOrder` in the maintenance scope, `orderKind=defect`, `orderStatus=open`, `concerns` / `ofAsset` to the drill; defects view **1**; all open inspections still **12** |
| 2.6 | Manager (browser) | Run `record_inspection` from the list button on TEST-A-fireExtinguisher Yard: `result=pass`, at least one photo, a signature, inspection date = run day, **next due date left empty** | the same duty stays `orderStatus=open`; `result=pass`; `lastDone` = run day; `dueDate` = run day + 365; `description` unchanged; a protocol (`orderKind=inspectionProtocol`, `orderStatus=done`) is linked `concerns` / `ofOrder` and holds the photo and signature; the duty remains in all open inspections and has left overdue and the current 30-day window; due in 30 days is now **3**; all open still **12** |
| 2.7 | Manager (browser) | Run `record_inspection` on TEST-A-electricalTest Drill: `result=pass`, photo, signature, inspection date = run day, **next due date = run day + 400 days** | the same duty stays `open`; `result=pass`; `lastDone` = run day; `dueDate` = run day + 400 (the typed date, not the 365-day interval); a protocol is linked `ofOrder`; due in 30 days is now **2**; all open still **12** |
| 2.8 | Manager (browser) | Run `record_inspection` on TEST-A-ladder Ladder 3m: `result=defect`, photo, signature, inspection date = run day, next due date left empty | the same duty stays `open`; `result=defect`; `lastDone` = run day; `dueDate` = run day + 365; `inspectionNote` holds any note you typed; **no** second defect order is created; defects is still **1** (the order from 2.5); all open still **12**; due in 30 days is still **2** |

After 2.6 and 2.7 the 30-day window still contains occupational safety 1001
and periodic inspection 1002. Extinguisher yard and the drill have moved
out. Oil change 1001 remains the single overdue row.

## 3. Negative tests (N1–N2)

| # | Role | Test | Expected |
|---|---|---|---|
| N1 | Manager (browser) | Open `record_inspection` on an open scheduled order **without** a result (dates may be filled) | the server refuses the save; `onto_object_show` shows the duty unchanged (`dueDate`, `lastDone`, `result`, `orderStatus`) |
| N2 | Manager (browser) | Open `record_inspection` on an open scheduled order **without** an inspection date (a result may be filled) | the server refuses the save; the duty is unchanged |

Run N1 and N2 **before** 2.6 on an order you will later record (for example
TEST-A-fireExtinguisher Yard), so the refused saves are proven on a
still-untouched row.

## 4. Clean-up

Leave `TEST-A-` objects in place unless the intake asks to delete them. If you
delete, delete **one id at a time**, never by prefix, and budget the live
`delete_*` price. Do not move test objects into a customer's live lists without
being asked. Quote the four list counts after clean-up, or quote that the
ExampleWorks rows were kept.
