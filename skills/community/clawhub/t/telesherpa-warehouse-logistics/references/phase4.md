# Phase 4 — action log, manager list or CSV

**Goal:** the manager can prove who bound which label, and can export or open a
list of labels, packages and movements.

**Input:** phase 3 gate passed.

---

## 1. Definitions

### 1.1 Action log

The source is `onto_action_logs` (confirm the tool name in your catalogue). Every
`label_bind` execution must leave a row with the action key, the label, the
account and the scope. Quote at least:

- the manager bind from phase 2
- the staff bind from phase 3

A rejected second bind must **not** add a successful bind row.

Reports that interpret this log are ordered through the service channel. Offer them
([reports.md](../../../telesherpa-ontology-platform/references/features/reports.md));
do not try to save a report yourself (403).

### 1.2 Manager list or CSV

A member can build a block view. If the view allows a download, enable it and
open the file. Minimum columns:

- Labels: `code`, `labelStatus`, `charge`, identified package (name), printed at
- Packages: name, `menge`, `einheit`, `lot`, `bestBefore`, count of identifying
  labels if the view can show it
- Movements: time, `movementType`, `menge`, package, place (`movesTo`), `bookedBy`,
  `grund` when present

The package list shows the book quantity `menge` that the bookings maintain.
Movement rows are the history of those bookings.

After this phase, run [phase 5](phase5.md) and come back to quote the booking
rows in the same list or CSV.

---

## 2. Recipe

1. Read the action log for `label_bind`. Quote the two successful rows and the
   absence of a success row for the rejected second bind.
2. Open the manager label, package and movement views. If a CSV is available,
   download it, open it, and quote one row per test package and the bound test
   labels. After phase 5, quote the test movements as well.
3. Read `onto_credit_balance` for the manager and for M1.

---

## 3. Checks via MCP

- Action-log rows quoted.
- Views still carry `access.require`.
- Balance quoted now, not from memory.

## 4. Checks in the browser (manager)

- The list or CSV opens and matches the read-backs of phases 1–3
  (statuses, charges, quantities).

## 5. Phase gate

Log rows and the list or CSV are quoted. The workspace is still not "configured"
until [acceptance-scenario.md](acceptance-scenario.md) has been run end to end.

## 6. Typical errors

- Building a privileged report yourself instead of filing a service request.
- Cleaning up test labels before the log has been quoted.
