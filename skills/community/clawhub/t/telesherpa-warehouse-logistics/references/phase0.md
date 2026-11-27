# Phase 0 — scopes, rights, object types, properties

**Goal:** three scopes with the right types activated, the rights of every account
written down and set, the stock functions and actions installed in matching
scopes, and a smoke test that proves the **definitions** are in place
(scopes, types, fields, option values, link types, functions, actions, rights).
No business data yet (that is phase 1).

**Input:** answered [intake](intake.md) (questions 1, 5, 7, 18, 20, 21) and the
checks from [prerequisites](prerequisites.md).

**Budget (pay-per-use):** the live volume price of every **new** scope, plus reads
and any definition writes the live table prices. If you reuse an existing
`_master` or `_team` from shift-planning, do not create them again and do not
bill them twice. Log what is booked.

Placeholders: `<company>` (slug from intake 20), `<master_scope_id>`,
`<warehouse_scope_id>`, `<team_scope_id>` (numbers returned by
`ontouser_scope_create` or by `ontouser_scope_index` when reusing). Never publish
those numbers.

---

## 1. Definitions

### 1.1 Scopes

| Scope name | Purpose | Holds | Who works here |
|---|---|---|---|
| `<company>_master` | master data | business, sites, people (**basic** fields), storage locations, packages (`menge`, `einheit`, `lot`, `bestBefore`) | managers write; staff read |
| `<company>_warehouse` | warehouse work | labels, print charges and files, `stockMovement` rows, functions, action definitions, manager views | managers (and a warehouse lead) |
| `<company>_team` | team door | staff views, the start card for the scan page, staff-facing bind actions shared with warehouse | staff |

Rules:
- Names: `a-z0-9_`, max 30 characters. Check the longest one (`<company>_warehouse`).
- The scope is the lock. Never rely on a view filter to hide data.
- **Reuse.** If shift-planning already created `_master` and `_team` for this
  business, add only `_warehouse`, keep the existing people and sites, and record
  that decision in the run log. A second master with a copy of the persons is a
  defect.
- Write all three names and returned ids into your run log (not into the public skill).
- **Links cross scopes.** `identifies` runs from a label in warehouse to a package
  in master. The manager creates the first test bind (write on both scopes). Staff
  create further binds through the scan and the scope bridge. A movement links
  from a `stockMovement` to a package on master and to a storage location on
  master; after the first test booking, quote the scope the movement landed in.

### 1.2 Rights matrix

Read / Write / Manage per account. `–` = no grant at all.

| Account | `<company>_master` | `<company>_warehouse` | `<company>_team` |
|---|---|---|---|
| Manager / owner (builds the workspace) | R W M | R W M | R W M |
| Warehouse lead (optional, intake 8) | R – – | R W – | R W – |
| Warehouse staff (scanner) | **R – –** | **– – –** | R W – |
| Kitchen (only if intake 12 allows them to bind) | R – – | **– – –** | R W – (only the bind action) |

Notes:
- **Staff: no membership on warehouse.** A label opens for a staff member through
  the **scan** (the code), not through a scope right. The write door for bind is
  the **scope bridge**. A direct `onto_object_show` of a warehouse label as staff
  must answer 404 / no access (confirm in phase 3).
- **Staff: read on master, no write.** Needed so the package picker on `label_bind`
  can list packages and so storage names resolve. Do not put protected data on
  those objects.
- Do not grant warehouse read "so views work".
- Stock bookings (`stock_putaway`, `stock_pick`, `stock_relocate`, `stock_count`)
  and `label_rebind` stay on the manager path in this skill.

### 1.3 Types to activate

On `_master`: `organisation`, `building`, `person`, `storage`, `package`, `file`.
On `_warehouse`: `label`, `stockMovement`, `file`, `comment` (if you keep notes),
plus whatever the print path requires — read it from `onto_type_show` / the
type's interfaces and quote it.
On `_team`: no extra master types required; views and actions live here.

Activation: `ontouser_scope_types_set` **replaces** the list. Include every type
the scope must keep. The preset `lager` may be applied only on an empty scope
after `onto_catalog_index` has been read; it will not add `organisation` or
`building`. Types are global; then apply the preset; then install functions and
actions for this warehouse — one planned rollout, not a chain of one-off edits.

`onto_type_show` must quote at least:

- `label`: `code`, `charge`, `labelStatus` (options `frei`, `gebunden`, `gesperrt`),
  `printedAt`, `printedBy`; action keys `label_bind` and `label_rebind`.
- `package`: `menge` (int), `einheit` (string), `lot` (string), `bestBefore`
  (date). Action keys: `stock_putaway`, `stock_pick`, `stock_relocate`,
  `stock_count`.
- `stockMovement`: `movementType` (options include `putaway`, `pick`, `relocate`,
  `count`), `menge` (int), `einheit`, `grund`, `bookingTime`, `bookedBy`.
- `storage`: `description` (and the `address` set if present).

### 1.4 Properties and option values

Do **not** override `labelStatus` with English values. The proven actions
`label_bind` and `label_rebind` condition on `frei` / `gebunden` and write
`gebunden`. You may set **labels** (the words staff see) in the intake language;
the values stay as they are.

For any other option list you add (for example a site code), use English camelCase
values and labels in the intake language. The stock actions write the English
`movementType` values `putaway`, `pick`, `relocate` and `count`.

### 1.5 Link types

Confirm with `onto_link_index` (do not invent):

| Key | types1 → types2 | Unique? | Used for |
|---|---|---|---|
| `identifies` | `label` → `package` | yes (label side) | bind and rebind |
| `moves` | `stockMovement` → `package` | no | every booking |
| `movesTo` | `stockMovement` → `storage` | no | the place in the prompt |
| `bestehtAus` | organisation / building / … | no | site tree |
| `hasfile` | any → `file` | no | print PDF |

### 1.6 Functions and actions

Install these **in the same scopes as the packages they will book** (include
`<master_scope_id>` in each function's `scopes` if packages live on master, and
install the actions so they can run there). A mismatch returns HTTP 403,
"Function in diesem Scope nicht erlaubt".

**`stock_move_apply`** — used by putaway, pick and relocate.

- Inputs: `objekt` (package, required), `zugang` (int, required), `art` (string,
  required), `vorzeichen` (int, default 1), `platz` (storage, optional).
- Body: new quantity = current `menge` + `zugang` × `vorzeichen`.
- Effects: create a `stockMovement` named `Bewegung {art}` with
  `movementType={art}`, `menge={zugang}`, `bookingTime={now}`,
  `bookedBy={user_email}`; links `moves` → the package and `movesTo` → the
  place; then set `menge` on the package to the result.

**`stock_count_apply`** — used by count.

- Inputs: `objekt` (package, required), `ist` (int, required), `grund` (string,
  optional), `platz` (storage, optional).
- Body: the counted quantity `ist`.
- Effects: create a `stockMovement` named `Inventur {now}` with
  `movementType=count`, `menge={ist}`, `grund={grund}`, `bookingTime={now}`,
  `bookedBy={user_email}`; links `moves` and `movesTo`; then set `menge` on the
  package to `ist`.

**Actions** (canonical keys; `scan.ein_code`, `ausfuehrung: auto`, roles include
`member`, and `require_scope_write: <warehouse_scope_id>` on manager actions):

| Key | Prompts | Function inputs |
|---|---|---|
| `stock_putaway` | `platz` (storage, required), `zugang` (int, required) | `art=putaway`, `vorzeichen=1` |
| `stock_pick` | `zugang` (int, required), `platz` (storage, optional) | `art=pick`, `vorzeichen=-1` |
| `stock_relocate` | `platz` (storage, required), `zugang` (int, optional; pass the current book quantity) | `art=relocate`, `vorzeichen=0` |
| `stock_count` | `ist` (int, required), `platz` (storage, optional), `grund` (text, optional) | `stock_count_apply` |
| `label_rebind` | `paket` (package, required); condition `labelStatus=gebunden` | update: replace `identifies` (`replace: "source"`) |
| `label_bind` | as in phase 2; also on the team door with a scope bridge | update: `labelStatus=gebunden` + `identifies` |

---

## 2. Recipe

1. Measure credits and prices ([prerequisites](prerequisites.md)).
2. `ontouser_scope_index` — if `_master` / `_team` exist, reuse them.
3. `ontouser_scope_create` only for scopes that do not exist. Read each back.
4. `onto_catalog_index` — note the `lager` preset, then `ontouser_scope_types_set`
   per scope, including `stockMovement` on the warehouse.
5. `onto_type_show` on every type in §1.3. Quote fields and action keys.
6. `onto_link_index` — quote `identifies`, `moves`, `movesTo`.
7. Install `stock_move_apply` and `stock_count_apply` with `scopes` that include
   the package scope. Install the six actions above. Read both back.
8. Set rights with `ontouser_team_set_scope_rights` as in §1.2. Read back with
   `ontouser_team_show`.
9. Do not create business objects yet.

---

## 3. Checks via MCP

- Three scopes in `ontouser_scope_index`, suffixes as agreed, `can_manage_scope` for you.
- Types present; `label`, `package` and `stockMovement` fields quoted.
- `identifies`, `moves` and `movesTo` present, directions as in §1.5.
- `stock_move_apply` and `stock_count_apply` list the package scope in `scopes`.
- The six action keys are present; `label_rebind` carries `require_scope_write`.
- Field / staff test account: **403** (or equivalent no-access) on the warehouse
  scope; read on master succeeds.

## 4. Checks in the browser

Not required in phase 0 beyond signing in as manager and confirming the three
scopes are visible. Staff browser checks start in phase 3.

## 5. Phase gate

You may enter phase 1 only when the MCP checks above are quoted. Status: "Stage 0
of 5 complete".

## 6. Typical errors

- Creating a second `_master` although shift-planning already has one.
- Applying `lager` and dropping `organisation` / `building` from an existing master.
- Overriding `labelStatus` to `free` / `bound` / `locked` and then watching
  `label_bind` fail.
- Granting staff warehouse read after the 403 "looks inconvenient".
- Installing a stock action that points at a function whose `scopes` omit the
  package's scope — the first booking then returns 403.
