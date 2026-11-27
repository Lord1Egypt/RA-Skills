# Intake — what to ask the business before you build

Send these questions to the business (owner or manager) and get written answers.
Do not start phase 0 with gaps in sections **A, B, D and E**. Section **C** may be
completed before phase 1 (print and bind) if A/B/D/E are already closed.
DemoRestaurant answers below are **examples**; never use them as defaults for a real
customer.

Answers are kept in a short intake record (plain text or a comment on the business
object once it exists). Staff personal data never goes into chat logs or public places.

If [shift-planning](../../shift-planning/references/intake.md) was already answered
for this business, reuse those answers for the legal name, sites, people, label
language, slug, budget contact and time zone. Ask only what is new here.

## A. Business and structure

| # | Question | Why | Example answer |
|---|---|---|---|
| 1 | Name of the business (legal and short name)? Already has shift-planning scopes? | `organisation`, scope slug, reuse of `_master` | "DemoRestaurant GmbH", short `demorestaurant`; master already exists |
| 2 | Sites (addresses)? One or several? Is stock kept per site? | one `building` per site; name labels and packages per site | one site |
| 3 | Physical storage areas (kitchen, cellar, cold room, off-site)? Fixed slots or chaotic (the slot exists when the package is put down)? | `storage` objects | kitchen + cellar; chaotic slots with a code on the shelf |
| 4 | Units in use (piece, kg, litre, …)? Lot / best-before required? | `einheit`, `lot` and `bestBefore` on the package | piece, kg, litre; lots and best-before on each package |
| 5 | Country / region and time zone? | country module, time handling | Germany, Europe/Berlin. **Not Europe/Berlin → stop** and file `ontouser_service_request`. |
| 6 | Who maintains the list of packages and storage locations? | phase 1 rights | warehouse lead |

## B. People and roles

| # | Question | Why | Example answer |
|---|---|---|---|
| 7 | **Who is the manager** with full rights? Human, agent, or both? | rights matrix | owner + one agent |
| 8 | Is there a warehouse lead who binds and prints but must not change the business or people in master? | separate rights (warehouse write, master read) | one warehouse lead |
| 9 | **People who scan:** first name, last name, login e-mail, site. Reuse the shift-planning persons where they are the same people. | `person`, staff accounts | two warehouse staff, optionally one kitchen person |
| 10 | Does every scanner have their own e-mail and a device? | staff accounts, scan page | yes |
| 11 | **Visible to colleagues:** staff can read master packages (name, `menge`, `einheit`, `lot`, `bestBefore`) and storage locations. Is that acceptable? | E2 on master | yes for name, quantity, lot and best-before; no purchase prices |

## C. Rules and process

| # | Question | Why | Example answer |
|---|---|---|---|
| 12 | Who may bind a free label to a package — only warehouse staff, or also kitchen? | phase 3 actions and guards | warehouse staff only |
| 13 | How many labels per package are typical? (The platform allows several; four on one crate is proven.) | phase 2 | one as default, extras when a crate has more than one visible face |
| 14 | Who may lock a label (`gesperrt`) when a sticker is lost or replaced? | phase 2 | warehouse lead only |
| 15 | Who prints a charge, and who reprints the same charge? | phase 1 and 2 | warehouse lead |
| 16 | Who may book putaway, pick, relocate and count (managers / warehouse lead)? | phase 5, manager path | warehouse lead and owner |
| 17 | Who may rebind a bound label onto another package? | `label_rebind` with `require_scope_write` | warehouse lead only |

## D. Naming and language

| # | Question | Why | Example answer |
|---|---|---|---|
| 18 | **Label language** for staff-facing texts (views, buttons)? | labels, country module | German |
| 19 | **Naming pattern** for packages, storage and label charges? | readable lists | `PKG-<site>-<name>`, `LOC-<area>-<n>`, charge `YYYY-MM-DD-<n>` |
| 20 | Scope slug (lower case `a-z0-9_`; the scope name may have 30 characters and `_warehouse` takes 10, so the slug has **at most 20**)? If shift-planning already used a slug, keep it and only add `_warehouse`. | scope names | `demorestaurant` → `demorestaurant_master`, `demorestaurant_warehouse`, `demorestaurant_team` |

## E. Budget and contact for the build

| # | Question | Why |
|---|---|---|
| 21 | Credit budget for setup and test, and who tops up? | stop rule on budget |
| 22 | Who answers questions during the build, and how fast? | stop-and-ask points |
| 23 | Who logs in as staff for the acceptance test, and who holds a printed test sheet to scan? | browser and scan checks |

## Mapping to the build

| Intake | Where it is used |
|---|---|
| 1, 2, 20 | phase 0 scope names; phase 1 business/site objects (reuse if present) |
| 3, 4, 19 | phase 1 storage, packages, `einheit`, `lot`, `bestBefore` |
| 7, 8, 10, 12–17 | phase 0 rights; phases 2–3 and 5 actions |
| 9 | phase 1 people; phase 3 accounts |
| 5 | country module (e.g. [country-de.md](country-de.md)) |
| 18, 19 | all labels and names |
| 21–23 | measurement and acceptance |

**Option values:** create **scope-specific** property definitions for any new
option list you introduce, with **English** values. Do **not** replace the
platform values `frei` / `gebunden` / `gesperrt` on `labelStatus` — `label_bind` and
`label_rebind` depend on them. The name the business uses becomes the option **label** in the
language of question 18 (see [country-de.md](country-de.md)).
