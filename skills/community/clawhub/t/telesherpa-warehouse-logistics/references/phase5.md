# Phase 5 — stock bookings, rebind, lot and best-before

**Goal:** a manager can put away, pick, relocate and count a package, hang a
bound label onto another package, and read lot and best-before on the package.
Every booking writes a `stockMovement` and updates `menge` in the same run.

**Input:** phases 0–4 complete (packages, storage, labels, bind, manager views).
Functions and actions from [phase0.md](phase0.md) §1.6 are installed and quoted.

**Budget (pay-per-use):** live prices for `onto_object_execute_action` (and for
any object or link writes the functions perform). Call `onto_credit_pricing` and
`onto_credit_balance` before the first booking and after the last. Log the keys
and numbers you actually read; do not copy a figure from this skill.

This phase describes the **manager path**. Do not add the stock actions to the
team door, and do not tell the customer that staff can book through that door,
unless you have measured that path in this workspace.

---

## 1. Definitions

### 1.1 Book quantity

`menge` on the package is the book quantity. The functions update it in the same
run as the movement:

| Action | Effect on `menge` | Movement `menge` | `movementType` |
|---|---|---|---|
| `stock_putaway` | previous + `zugang` | the booked `zugang` | `putaway` |
| `stock_pick` | previous − `zugang` | the booked `zugang` | `pick` |
| `stock_relocate` | unchanged (sign 0) | the `zugang` you passed | `relocate` |
| `stock_count` | set to `ist` | the counted `ist` | `count` |

Do not edit `menge` with `onto_object_set_property`. After a count there is no
second correction row; the gap is the difference between the previous book
quantity and the new `menge`. Put the reason in `grund`.

Each movement also stores `bookingTime` and `bookedBy` (the signed-in user's
e-mail). Count also stores `grund` when prompted. The place from the prompt is
written as `movesTo`. The movement is linked to the package as `moves`.

### 1.2 Single-scan booking

Each stock action has `scan.ein_code` and `ausfuehrung: auto`. One code
identifies the package (the package itself, or a bound label that resolves to
it). The action then prompts for quantity and, where required, the storage
location (`object_types: [storage]`, the client fills the UDID).

### 1.3 Lot and best-before

On the package, `lot` is a string and `bestBefore` is a date. Set them when the
package is created or when the intake says to fill them, and quote them on
read-back. They do not hang on the label or on the movement.

### 1.4 `label_rebind`

Condition: `labelStatus` is `gebunden`. Prompt: `paket` (the new package). The
action replaces `identifies` (`replace: "source"`). Status stays `gebunden`. The
execute response includes `links_entfernt` with the previous edge. Install the
action with `require_scope_write: <warehouse_scope_id>` so only leadership can
run it.

---

## 2. Recipe

1. Read `onto_credit_pricing` and `onto_credit_balance`. Save the table and the
   balance with a timestamp.
2. Pick a test package (prefix `TEST-5-`) and two storage locations. Set `lot`
   and `bestBefore` if empty. Quote the starting `menge`.
3. As manager, run `stock_putaway` with a required place and a quantity. Read
   back the package (`menge` increased) and the new movement (`movementType`,
   `menge`, `bookedBy`, `bookingTime`, `moves`, `movesTo`).
4. Run `stock_pick` with a quantity (place optional). Read back: `menge`
   decreased, movement type `pick`.
5. Run `stock_relocate` to the second place; pass the current book quantity as
   `zugang`. Read back: package `menge` unchanged, movement type `relocate`,
   `movesTo` is the new place.
6. Run `stock_count` with a counted quantity and a reason, optionally a place.
   Read back: package `menge` equals `ist`, one movement of type `count` with
   `grund`, no extra correction row.
7. Take a bound test label (or bind a free one first). Run `label_rebind` onto
   a second test package. Read back: the label still `gebunden`, `identifies`
   points at the new package, the old package no longer has that edge, and the
   execute result listed `links_entfernt`.
8. Quote `onto_credit_balance` again.

---

## 3. Checks via MCP

- Package `menge` after the four bookings matches the table in §1.1.
- Four `stockMovement` objects exist for the test package, with `moves` and
  `movesTo` as booked.
- `lot` and `bestBefore` are present on the test package when you set them.
- After rebind, `onto_object_show` on the label and `onto_object_graph` on both
  packages confirm the new `identifies` edge only.
- If a stock action returns 403 and the message says the function is not
  allowed in this scope: stop, fix the function's `scopes`, do not grant
  warehouse rights to staff as a workaround.

## 4. Checks in the browser (manager)

- The four stock buttons appear on a package for the manager and are hidden
  behind `require_scope_write`.
- After a booking, the package quantity and a movement row are visible in the
  manager list or detail (phase 4 views).
- `label_rebind` is available to the manager on a bound label and is not
  offered as a staff start-card action.

## 5. Phase gate

You may report "stage 5 of 5" only when the MCP checks above are quoted and the
acceptance steps 5.1–5.8 have passed. Combined with phases 0–4, that is the
end-to-end scenario.

## 6. Typical errors

- Pointing `stock_putaway` at a function registered only in another scope
  (HTTP 403, no movement).
- Omitting `zugang` on relocate so the function rejects a missing required
  input — pass the current book quantity.
- Setting `menge` by hand after a count "to make it tidy" and leaving no
  movement.
- Running `label_rebind` without `require_scope_write`.
- Claiming staff can book through the team door without a measured test in
  this workspace.
