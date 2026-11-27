# Operating model — how an agent oversees a warehouse

This file describes the warehouse this skill sets up: how goods are identified,
how quantity is booked, how an agent measures and acts, and what the agent never
does alone. Build the blocks in phases 0–5.

---

## 1. The warehouse picture

Goods sit in **packages**. Each package has a book quantity (`menge`), a unit
(`einheit`), and, when the business uses them, a lot (`lot`) and a best-before
date (`bestBefore`). A printed **label** is only a pointer: its code binds to at
most one package. Staff identify a package by scanning the sticker. Managers book
quantity with a single scan of that package (or of a bound label that resolves to
it). The action then prompts for the quantity and, where required, the storage
location.

| Flow | What happens |
|---|---|
| Identify the package | Print a charge of labels, stick them on, bind a free label to a package with a single scan. Quantity and unit sit on the package. Several labels may point at the same package. |
| Lock a lost or replaced sticker | Set `labelStatus` to `gesperrt`. The code must no longer resolve. |
| Put-away | Book inbound quantity onto the package. `menge` increases by the booked amount. A `stockMovement` of type `putaway` is written, with `moves` to the package and `movesTo` to the place. |
| Pick / issue | Book outbound quantity. `menge` decreases by the booked amount. A movement of type `pick` is written. |
| Relocate | Name the new storage location. `menge` stays the same. A movement of type `relocate` is written, with `movesTo` on the new place. |
| Count / inventory | Enter the counted quantity and a reason. `menge` is set to that quantity. A movement of type `count` is written; there is no second correction row. The gap is the difference between the previous book quantity and the new `menge`. |
| Rebind a sticker | Leadership hangs a bound label onto another package. `identifies` is replaced; the execute result lists the removed edge. Status stays `gebunden`. |

The package list a manager opens is the book quantity per package, plus the
movement rows linked to it. That is the stock this skill maintains.

---

## 2. The agent's role

| Task | What you do |
|---|---|
| Read the current package list | On a schedule agreed in the intake, list packages and quote `menge`, `einheit`, `lot`, `bestBefore`, name and site; list labels by `labelStatus` and `charge`. Quote values from a read-back. |
| Read movement history | Walk the `moves` links of a package and quote type, quantity, time, person, place and reason. |
| Watch lots and best-before dates | Flag packages whose `bestBefore` falls inside an agreed window, or is already past, using the dates you read on the packages. |
| Watch count gaps | After a count, compare the new `menge` with the previous book quantity and name the difference. |
| Escalate to a human | Stop and report when a stop rule fires, when data is missing, or when a proposed action needs a decision. |
| Leave the scan to people | Staff bind labels through the scan page. Managers book putaway, pick, relocate and count on the manager path. The agent does not pretend a tool write is a scan. |

---

## 3. The control loop

| Step | What you do |
|---|---|
| Measure | List packages and labels; read a bound label's `identifies` edge; read movements on a package; read `label_bind` and stock-action rows in the action log. |
| Assess | Notice missing `menge`, a surprising number of `frei` or `gesperrt` labels, a best-before date inside the agreed window, or a count that differs from the previous book quantity. |
| Act | Print, bind, rebind and lock labels as the workspace allows; book putaway, pick, relocate or count as a manager; report findings to the human. Do not edit `menge` "to correct stock". |
| Check | Read back every write (label status, `identifies`, package fields, movement, action log). |

---

## 4. Indicators a member can quote

| Indicator | How you get it |
|---|---|
| Packages on file | Number of package objects, and `menge` per package (the book quantity the bookings maintain). |
| Labels by status | Counts of `frei`, `gebunden` and `gesperrt`, plus labels per charge. |
| Bind evidence | Successful `label_bind` rows (who, when, which label). |
| Movements per package | The `stockMovement` rows linked with `moves`, with type, quantity, place, time and person. |
| Count gap | Previous book quantity versus the counted `menge`. |
| Best-before watch list | Packages whose `bestBefore` is inside the agreed window, read from the package field. |

A manager list or CSV (phase 4) can show these columns. A formal report or chart
is ordered through the service channel, not built by a member.

---

## 5. What the agent never does alone

- Never invent a label code or print a QR that encodes a UDID.
- Never put `menge` on the label, and never edit `menge` on the package by hand.
- Never grant staff warehouse read so a scan or a picker "works".
- Never tell the customer that staff can book putaway, pick, relocate or count
  through the team door unless that path has been measured in this workspace.
- Never install a stock action whose function is not allowed in the package's
  scope.
- Never leave `label_rebind` without `require_scope_write`.
- Never place a supplier order, and never present a package list as a legally
  required stock book.
- Never report completion without quoting the checks in [SKILL.md](../SKILL.md)
  and the acceptance scenario.
