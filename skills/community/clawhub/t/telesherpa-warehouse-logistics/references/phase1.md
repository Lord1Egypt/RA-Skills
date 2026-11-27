# Phase 1 — sites, people, storage, packages, label charge, print

**Goal:** the manager can see sites, people, storage locations and packages with a
quantity, and holds one printed charge of free labels. Nothing is bound yet.

**Input:** phase 0 gate passed; intake 1–6, 9, 19, 23.

**Budget:** measure before and after. Main costs are `create_object` (people,
storage, packages, labels) and the print path (confirm whether it books `action`
and/or `file_upload`).

Reuse people and sites from [shift-planning phase 1](../../shift-planning/references/phase1.md)
when they already exist. This file does not repeat that recipe.

---

## 1. Definitions

### 1.1 Master objects

| Type | Name pattern (intake 19) | Required fields / links |
|---|---|---|
| `organisation` | business legal or short name | — |
| `building` | site | `bestehtAus` from the organisation; address set if used |
| `person` | staff name | `email` = the login, lower case; basic fields only |
| `storage` | `LOC-…` | `description`; optional address |
| `package` | `PKG-…` | `menge` (int, ≥ 0), `einheit` (string from intake 4), `lot` and `bestBefore` when the intake uses them. Do not write `place` as a second location next to movements |

### 1.2 Labels and print

A label is created by the **platform** as part of a charge, not by you inventing a
code. After creation, every label in the charge must read back with:

- `code` — Crockford Base32, 12 characters plus a check digit, without `I`, `L`,
  `O`, `U`
- `charge` — the charge identifier you printed
- `labelStatus` = `frei`
- `printedAt` / `printedBy` set once the sheet has been printed (confirm)

The print sheet is Avery Zweckform 3475: 70 × 36 mm, 3 × 8 = 24 labels per A4,
QR 26 mm, error-correction level M, the code readable in groups of four, the
charge printed on the PDF. Discover the live action or view with
`onto_actiondef_list` and the interfaces on `label` (or on a charge object if one
exists). Quote the key you used. If nothing is offered, stop and file
`ontouser_service_request` — do not draw QR codes from UDIDs.

### 1.3 Manager views

In the warehouse scope, with `view_config.access.require` set:

- Labels (filter by `labelStatus` and `charge`)
- Packages (name, `menge`, `einheit`, `lot`, `bestBefore`, site if encoded in the name)
- Storage locations (master; a manager list may live in master or warehouse, but
  staff must not be given warehouse read to see storage — storage is in master)

Follow [view-blocks.md](../../../telesherpa-ontology-platform/references/features/view-blocks.md).
Rebuild from blocks; hard-reload before you judge the page.

---

## 2. Recipe

1. Reuse or create the organisation and one building. Read back. Link `bestehtAus`.
2. Reuse or create the persons from intake 9 (manager, warehouse lead, staff M1).
   Read back the emails.
3. Create at least two `storage` objects. Read back.
4. Create at least two `package` objects with different `menge` / `einheit`, and
   with `lot` / `bestBefore` when the intake uses them. Read back. Confirm each
   object has quantity and unit, and has **no** `identifies` edge yet.
5. Create one charge of labels (a full 24-up sheet is the proven format; a smaller
   test charge is acceptable if the platform allows it — quote the count). Read
   every new label, or a sample of five plus the total count, and check the code
   format.
6. Print the charge. Open the PDF. Check layout, QR size and the charge line.
7. Build the three manager views. Read them back via `onto_settings_list` /
   `onto_interface_show`.

Do not bind a label in this phase (that is phase 2). Do not write `place` on a
package as a second location next to the movement links.

---

## 3. Checks via MCP

- Object counts per type quoted.
- One package: `menge` and `einheit` present; `lot` / `bestBefore` present when set.
- One label: `code`, `charge`, `labelStatus=frei`; `menge` is **absent** on the label.
- Codes match the Crockford rule (spot-check at least five).
- Views exist and carry `access.require`.

## 4. Checks in the browser (manager)

- Lists show the test packages and the free labels of the charge.
- The PDF opens, shows 24 labels on an A4 3475 layout (or the quoted test count),
  the charge, and codes in groups of four.
- Staff login is not required yet.

## 5. Phase gate

Quoted object counts, one package with quantity, one free labelled charge, and a
PDF that was opened. Status: "Stage 1 of 5 complete".

## 6. Typical errors

- Inventing a `code` and writing it onto a hand-made `label` object.
- Storing quantity on the label "because the sticker is what people scan".
- Filling `place` "to remember the slot" — the booking records the place on `movesTo`.
- Printing with an external QR tool that encodes the UDID.
