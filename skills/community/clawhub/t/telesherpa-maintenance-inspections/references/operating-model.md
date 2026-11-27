# Operating model — how an agent oversees inspection deadlines

This file is the control picture for a workspace built with this skill. It does
not add features. Flows and limits are those measured on the manager path.

## 1. The maintenance picture

- Every asset that must be inspected has one open `serviceOrder` per kind.
- The due date on that order is what the lists use.
- **Overdue** is `dueDate` before today, still open, not a defect.
- **Due in 30 days** is the open orders whose due date falls from `{today}`
  through `{today+30}` (a fixed window).
- **All open inspections** is every open scheduled or contract duty; defects
  are excluded.
- **Defects** is every open order with `orderKind=defect`.
- Recording an inspection creates a protocol (photos and signature live
  there) and updates the same duty: result, last done, and the next due date
  — either the date the manager typed, or the inspection date plus the
  interval when that field was left empty. The duty stays open and will show
  again when the new due date enters a list.
- A defect is a separate order, created on the asset with `report_defect`.

## 2. The agent's role

The agent sets up the scopes, types, views, forms, function, triggers and
actions, and then *measures* the workspace: counts, one recorded inspection,
one reported defect, a read-back of the links. Day-to-day recording of
inspections is the manager's work from the start cards. The agent does not
become the inspector of record after acceptance, unless the intake says the
agent will keep running the manager path.

## 3. The control loop

1. Quote the four list counts (overdue, due in 30 days, all open, defects).
2. Open a sample overdue or due row and quote asset, kind and `dueDate`.
3. If a count disagrees with the orders you read, check `orderStatus`,
   `orderKind`, `dueDate` and the `ofAsset` edge before you change a view.
4. After `record_inspection` or `report_defect`, read the duty, the protocol
   and the lists again. Do not trust the save "OK" alone.
5. Report in the shape from [SKILL.md](../SKILL.md). Name the stage. Never
   write "done" or "everything is set up".

## 4. Indicators a member can quote

| Indicator | Where it comes from |
|---|---|
| Overdue count | the overdue view, plus a read of those orders' `dueDate` |
| Due-in-window count | the 30-day view (`{today}` through `{today+30}`) |
| Open duties | all open inspections (defects excluded) |
| Open defects | the defects view |
| Last recorded inspection | `result`, `lastDone`, `dueDate`, `orderStatus` on the duty, plus the protocol linked `ofOrder` |

These are list counts and field values, not a report or a chart.

## 5. What the agent never does alone

- Message real people, or turn on e-mail or push, without a human asking.
- Delete by name, prefix or pattern.
- Widen rights so a view "starts working".
- Close a recurring duty to make a list shorter.
- Override a typed next due date, or invent an interval the intake did not give.
- Treat asset comfort fields as the deadline.
- Publish live identifiers, balances or personal e-mail addresses.
