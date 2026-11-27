# Glossary

One term, one meaning, in every file. Column "Key" is the identifier you type
(verbatim). Country-specific display labels are kept in the country module; the
label language of a real customer comes from intake 18.

## Key concepts

### Team door
The **team scope** is the staff's door into the workspace. Staff hold **read +
write** there, **read (no write)** on master, and **no membership** on the
warehouse scope. Every view a staff member opens and every button they press
lives in the team scope; the bind writes back through a scope bridge. The same
idea as in [shift-planning](../../shift-planning/references/glossary.md) — reuse
that glossary for person, signed-in person, management gate and scope bridge.
Stock bookings in this skill are run on the manager path.

### Label (type `label`)
A printed sticker with its own `code` and `charge`. It is a **pointer**, not the
stock. Status (`labelStatus`): `frei` (unbound), `gebunden` (bound to a package),
`gesperrt` (intentionally dead, no longer resolves). Several labels may point at
the same package; each label points at at most one package.

### Code
The platform-assigned Crockford Base32 value on the label (12 characters plus a
check digit, without `I`, `L`, `O`, `U`). Not the object UDID. Printed as the
public-app short URL `/q/<code>`, in groups of four.

### Charge
The batch identifier (`charge`) shared by the labels of one print sheet. A
reprint of the same charge must not create new labels.

### Package (type `package`)
The physical unit (crate, bag, bottle group). Carries `menge` (int, the book
quantity), `einheit` (string), `lot` (string) and `bestBefore` (date). Change
`menge` only by booking a movement.

### Storage (type `storage`)
A physical slot (shelf, floor mark, box) with a `description`. Bookings record
the place on the movement link `movesTo`.

### Stock movement (type `stockMovement`)
One booking row. Fields: `movementType` (`putaway`, `pick`, `relocate`, `count`),
`menge` (the booked or counted quantity), `bookingTime`, `bookedBy`, and `grund`
on a count. Links: `moves` to the package, `movesTo` to the storage location
named in the prompt. The type also has `einheit` and `movesFrom`; quote them when
the read-back shows them.

### `identifies`
Link type, direction **label → package**, unique on the label side. Set by
`label_bind`, moved by `label_rebind`.

### `label_bind`
Single-scan action (`ein_code`) on a free label. Prompts for a package, writes
`identifies` and `labelStatus=gebunden`. A second bind is rejected.

### `label_rebind`
Action on a bound label. Prompts for the new package (`paket`), replaces
`identifies` (`replace: "source"`), leaves `labelStatus=gebunden`, and reports
the removed edge as `links_entfernt`. Install it with `require_scope_write` so
only leadership can run it.

### Stock actions
Single-scan actions on a package (`ein_code`): `stock_putaway`, `stock_pick`,
`stock_relocate`, `stock_count`. They call `stock_move_apply` (putaway, pick,
relocate) or `stock_count_apply` (count) in the same scope as the package.

### Short URL
`/q/<code>` on the public app. After sign-in it opens the linked object; before
sign-in the object name is hidden.

### Warehouse scope
The work scope (`<company>_warehouse`) that holds labels, print files, movement
functions, stock actions and manager views. Staff are not members of it.

### Preset `lager`
Catalogue bundle of `package`, `storage`, `label`, `person`, `file`. It does not
include `organisation` or `building`. After the preset, install `stockMovement`,
the two functions and the stock actions on the warehouse (and on the package
scope, as phase 0 describes).

## Keys (verbatim)

| Term | Key |
|---|---|
| Label type | `label` |
| Package type | `package` |
| Storage type | `storage` |
| Movement type | `stockMovement` |
| Label status property | `labelStatus` |
| Status values | `frei`, `gebunden`, `gesperrt` |
| Code / charge / printed | `code`, `charge`, `printedAt`, `printedBy` |
| Quantity / unit / lot / best-before | `menge`, `einheit`, `lot`, `bestBefore` |
| Movement fields | `movementType`, `menge`, `grund`, `bookingTime`, `bookedBy` |
| Movement types used by the actions | `putaway`, `pick`, `relocate`, `count` |
| Bind action | `label_bind` |
| Rebind action | `label_rebind` |
| Stock actions | `stock_putaway`, `stock_pick`, `stock_relocate`, `stock_count` |
| Stock functions | `stock_move_apply`, `stock_count_apply` |
| Bind link | `identifies` |
| Movement links | `moves`, `movesTo` |
| Site tree | `bestehtAus` |
| File link | `hasfile` |
| Scan flag | `ein_code` |
| Catalogue preset | `lager` |
