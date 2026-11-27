# Acceptance scenario (end to end, phases 0–5)

One continuous test with fixed, fictional start data and expected values. A fresh
agent runs it once from an empty account (or from an existing DemoRestaurant
shift-planning master, if the intake says to reuse it); the paid run is measured
with [measurement.md](measurement.md). Every step names the **role** that performs
it and the **expected result**; a step passes only when the result is read back
(tool read or browser), not when the write call returned "OK".

The scenario has **38 steps** (0.1 … 5.8) and **14 negative tests** (N1 … N14).
Both counts are stated only here and in [SKILL.md](../SKILL.md) /
[definition-of-done.md](definition-of-done.md). Do not restate them from memory.

- Business: **DemoRestaurant**, slug `demorestaurant` → scopes
  `demorestaurant_master`, `demorestaurant_warehouse`, `demorestaurant_team`
  (reuse `_master` / `_team` if they already exist).
- All test objects carry the prefix `TEST-A-`. All addresses are `@example.com`
  in this document. These are not activatable human mailboxes. Before login tests,
  obtain explicit permission for dedicated controlled test mailboxes or another
  supported active test-account route, and align their master person e-mails with
  those logins. If only `example.com` data is permitted, keep the synthetic
  fixtures and mark staff-login tests blocked. Never use real staff data.
- Roles: **L** = manager / warehouse lead (owner of the scopes,
  `warehouse.lead@example.com`); **M1** = warehouse staff
  (`warehouse.staff@example.com`).
- Times are entered in Europe/Berlin; tool reads return UTC — compare after
  conversion.
- Budget: see [measurement.md](measurement.md); read the balance before and after
  each phase.

## 1. Start data

### 1.1 Site and storage (master)

| Object | Name | Values |
|---|---|---|
| organisation | `TEST-A-DemoRestaurant` | reuse if present |
| building | `TEST-A-DemoRestaurant Main Street` | one site |
| storage | `TEST-A-LOC-Kitchen-01`, `TEST-A-LOC-Cellar-01` | `description` set |

### 1.2 People (master: basic data only)

| # | Person | Login e-mail | Role | Account |
|---|---|---|---|---|
| L | `TEST-A-Warehouse Lead` | `warehouse.lead@example.com` | manager | L |
| M1 | `TEST-A-Warehouse Staff` | `warehouse.staff@example.com` | staff | M1 |

### 1.3 Packages (master)

| Package | `menge` | `einheit` | `lot` | `bestBefore` |
|---|---|---|---|---|
| `TEST-A-PKG-Flour-10kg` | 10 | `kg` | `TEST-A-LOT-FLOUR` | `2027-06-30` |
| `TEST-A-PKG-Oil-6` | 6 | `piece` | `TEST-A-LOT-OIL` | `2027-03-31` |

### 1.4 Labels

One charge `TEST-A-CHARGE-01` of free labels (a full 24-up Avery 3475 sheet, or a
smaller quoted test charge if that is what the platform issued). Codes are assigned
by the platform.

## 2. Steps

A step passes only with a read-back. Mark "(confirm)" where the live path (print
key, short-URL target, staff 404) must be quoted from this workspace.

### Phase 0

| Step | Role | Action | Expected |
|---|---|---|---|
| 0.1 | L | `GET /health` or skip; `auth_status`; tool list for phase 0 | `member`; every named tool present |
| 0.2 | L | `onto_credit_pricing` and `onto_credit_balance` | full table saved with timestamp; balance covers phase 0 |
| 0.3 | L | `onto_type_show` on `label`, `package`, `storage`, `stockMovement`, `person`, `organisation`, `building`, `file` | fields of SKILL.md check 3 quoted |
| 0.4 | L | `onto_link_index` | `identifies` is label → package and unique; `moves` and `movesTo` are present |
| 0.5 | L | create or reuse the three scopes | `ontouser_scope_index` lists the three suffixes; you can manage all three |
| 0.6 | L | activate types; install `stock_move_apply` and `stock_count_apply` with the package scope in `scopes`; install the six actions | `ontouser_scope_types` quotes the lists in phase 0; `onto_function_index` and `onto_actiondef_list` quote the keys; `label_rebind` has `require_scope_write` |
| 0.7 | L | confirm `labelStatus` options | values are `frei`, `gebunden`, `gesperrt` — not replaced |
| 0.8 | L | set the rights matrix | `ontouser_team_show` matches phase 0 |
| 0.9 | M1 or a staff test | open the warehouse scope | **403** / no access; master read is allowed |

### Phase 1

| Step | Role | Action | Expected |
|---|---|---|---|
| 1.1 | L | reuse or create organisation and building | objects read back; `bestehtAus` present |
| 1.2 | L | reuse or create persons L and M1 | emails read back, lower case |
| 1.3 | L | create the two storage locations | both read back with `description` |
| 1.4 | L | create the two packages | `menge` / `einheit` / `lot` / `bestBefore` as in §1.3 |
| 1.5 | L | create charge `TEST-A-CHARGE-01` | count quoted; at least five codes match Crockford 12+check; every sampled label has `labelStatus=frei` and no `menge` |
| 1.6 | L | print the charge, open the PDF | Avery 3475 layout (70 × 36 mm, 3 × 8, QR 26 mm, ECC M, code in groups of four, charge on the sheet) — or the quoted test count with the same typography |
| 1.7 | L | manager views | label, package, storage and movement lists exist; `access.require` set |

### Phase 2

| Step | Role | Action | Expected |
|---|---|---|---|
| 2.1 | L | `label_bind` one free label to `TEST-A-PKG-Flour-10kg` | `labelStatus=gebunden`; `identifies` → that package; `menge` still 10 |
| 2.2 | L | bind three further labels to the same package | four labels identify it |
| 2.3 | L | `label_bind` again on a bound label | HTTP 400, precondition not met; still one `identifies` edge; status still `gebunden` |
| 2.4 | L | lock one label (`gesperrt`) | status `gesperrt`; resolve no longer opens the package (may be finished in 3.7 if the browser is only then available) |
| 2.5 | L | reprint `TEST-A-CHARGE-01` | label count for the charge unchanged; PDF still shows the same codes (spot-check three) |

### Phase 3

| Step | Role | Action | Expected |
|---|---|---|---|
| 3.1 | L | activate M1, set rights, transfer credits | `ontouser_team_show` quoted; M1 has a balance |
| 3.2 | L | save the team start card | `onto_startcard_index` shows the scan entry |
| 3.3 | M1 | single-scan a free label, run `label_bind`, pick `TEST-A-PKG-Oil-6` | status `gebunden`; `identifies` → that package; `menge` still 6 |
| 3.4 | anyone logged out | open `/q/<code>` of a bound label | **no object name** is shown |
| 3.5 | M1 | open the same `/q/<code>` after sign-in | the linked package is reachable (quote what opened) |
| 3.6 | M1 | `onto_object_show` on the warehouse label UDID | 404 / no access **(confirm)**; the bind in 3.3 remains |

### Phase 4

| Step | Role | Action | Expected |
|---|---|---|---|
| 4.1 | L | read `onto_action_logs` for `label_bind` | a success row for 2.1 and for 3.3; no success row for 2.3 |
| 4.2 | L | open the manager list or CSV | one row per test package; bound labels show `gebunden` and the package name; the locked label shows `gesperrt` |
| 4.3 | L | `onto_credit_balance` for L and M1 | balances quoted now |

### Phase 5

Starting book quantities before 5.2: Flour 10, Oil 6. Keep a written running
quantity in the run log.

| Step | Role | Action | Expected |
|---|---|---|---|
| 5.1 | L | read `lot` and `bestBefore` on both packages; fill them if empty | values as in §1.3 |
| 5.2 | L | `stock_putaway` 5 kg of Flour to `TEST-A-LOC-Kitchen-01` | package `menge` is 15; one movement type `putaway`, `menge` 5, `moves` to Flour, `movesTo` to Kitchen-01, `bookedBy` and `bookingTime` set |
| 5.3 | L | `stock_pick` 3 kg from Flour (place Kitchen-01 optional) | package `menge` is 12; one movement type `pick`, `menge` 3 |
| 5.4 | L | `stock_relocate` Flour to `TEST-A-LOC-Cellar-01`, pass `zugang` 12 | package `menge` still 12; one movement type `relocate`, `movesTo` to Cellar-01 |
| 5.5 | L | `stock_count` Flour, `ist` 11, `grund` "TEST-A count", place Cellar-01 | package `menge` is 11; one movement type `count`, `menge` 11, `grund` set; no second correction row |
| 5.6 | L | `label_rebind` one Flour-bound label onto `TEST-A-PKG-Oil-6` | label stays `gebunden`; `identifies` → Oil; Flour no longer has that edge; execute result lists `links_entfernt` |
| 5.7 | L | confirm the four stock actions and both functions: each function's `scopes` include the package scope | `onto_actiondef_list` and `onto_function_index` quoted; a mismatch would have failed 5.2 with HTTP 403 |
| 5.8 | L | `onto_credit_pricing` and `onto_credit_balance` | live keys and balances quoted now |

## 3. Negative tests (N1 … N14)

Run these as named tests and log them even when a numbered step already covered
the same fact.

| # | Role | Test | Expected |
|---|---|---|---|
| N1 | L | second `label_bind` on a bound label | 400, no change (same as 2.3) |
| N2 | L or M1 | resolve or scan a `gesperrt` label | does not open the package |
| N3 | M1 | scan a code that is not a platform label code | no action offered |
| N4 | M1 | membership or direct read on the warehouse scope | 403 / 404; no grant is added |
| N5 | M1 | manager-only print or lock action | button invisible; direct execute denied |
| N6 | L | reprint the same charge | no new label objects |
| N7 | L | read a label for `menge` / `einheit` | those properties are absent on the label; they are present on the package |
| N8 | logged out | `/q/<code>` of a bound label | no object name (same as 3.4) |
| N9 | L | run a stock action whose function is registered only in another scope (or quote the 403 from a first mis-install, then fix and continue) | HTTP 403, platform message that the function is not allowed in this scope; `menge` unchanged; no new movement |
| N10 | M1 | bind with a 0-credit staff account | HTTP 402, no bind; top up only after the test is logged |
| N11 | L | `label_rebind` definition | `require_scope_write` is set; the action is not on the staff start card |
| N12 | M1 | start card | it does not open a warehouse-scope manager view |
| N13 | L | after relocate (5.4) | package `menge` equals the quantity before the relocate |
| N14 | L | after count (5.5) | only one new movement, type `count`; no extra correction row |

## 4. Clean-up

Keep `TEST-A-` objects by default and list them in the run log. If the intake
asks you to delete them, delete **one id at a time**, budget the `delete_*`
price, and never delete by prefix. Do not move test objects into a live customer
scope that already serves real staff.
