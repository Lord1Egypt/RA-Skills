# Phase 2 — bind, several labels on one package, lock, reprint

**Goal:** a free label can be bound to a package; one package can carry several
labels; a second bind of the same label is rejected; a locked label no longer
resolves; reprinting the same charge creates no new labels.

**Input:** phase 1 gate passed.

---

## 1. Definitions

### 1.1 Action `label_bind`

Proven behaviour (quote your live actiondef; do not invent a second key):

| Field | Value |
|---|---|
| Key | `label_bind` |
| Object type | `label` |
| Condition | `labelStatus` equals `frei` (plain-text message on failure) |
| Scan | `ein_code: true` (single scan). |
| Prompt | package, required, `object_types: [package]` (object selection; the client fills the UDID) |
| Effect | create link `identifies` from the label to the package; set `labelStatus=gebunden` |
| Second bind | `require: absent` on that link → HTTP 400, platform text that the precondition is not met |

If you copy the action into the customer warehouse / team scopes, keep this
behaviour. Add `require_scope_write` on the manager-facing copy if managers also
have a button. The staff-facing copy (phase 3) runs from the team door with
`action.result_scope_id = <warehouse_scope_id>` and a guard if the intake limits
who may bind.

### 1.2 Several labels on one package

Uniqueness is on the **label** side: one label identifies at most one package.
The package side is not unique. Four labels on one crate is a proven case. Bind
four free labels of the test charge to package A.

### 1.3 Lock (`gesperrt`)

A label that is lost or replaced is set to `gesperrt`. After that it must no
longer resolve through `/q/<code>` or the scan page (no object name, no bind).
Discover the live action or manager path for the status change with
`onto_actiondef_list`. Only the warehouse lead / manager may run it
(`require_scope_write`). Do not delete the label object to "lock" it — the code
must remain reserved so a found sticker stays dead.

### 1.4 Reprint

Printing the **same** `charge` again produces a new PDF of the existing labels and
**must not** create new label objects. Count labels for that charge before and
after; the numbers must match.

To hang a bound label onto a different package, use `label_rebind` in
[phase 5](phase5.md). Do not delete the `identifies` link by hand and bind again.

---

## 2. Recipe

1. As manager, run `label_bind` on one free label and select package A. Read the
   label (`labelStatus=gebunden`) and `onto_object_graph` (`identifies` → package A).
   Read package A: `menge` unchanged by the bind (bind does not book quantity).
2. Bind three further free labels to the same package A. Graph: four incoming
   `identifies` edges (or four labels whose graph points at A).
3. Run `label_bind` again on a bound label. Expect HTTP 400 and no change on
   read-back.
4. Lock one label (a spare free label, or a bound one that you treat as lost —
   quote which). Confirm `labelStatus=gesperrt` and that resolve/scan no longer
   opens an object (browser, phase 2 or 3).
5. Reprint the same charge. Count labels for the charge before and after.

---

## 3. Checks via MCP

- One bound label: `identifies` quoted, `labelStatus=gebunden`.
- Package A: four labels identify it; `menge` still the value from phase 1.
- Second bind: 400, status still `gebunden`, still one `identifies` edge.
- Locked label: `gesperrt`.
- Charge count unchanged after reprint.

## 4. Checks in the browser (manager)

- The label list shows `frei` / `gebunden` / `gesperrt` correctly.
- Opening a bound label shows the package name.
- The reprinted PDF still lists the same codes (spot-check three).

## 5. Phase gate

Steps 1–5 quoted. Status: "Stage 2 of 5 complete".

## 6. Typical errors

- Treating a 400 on the second bind as a platform fault and then deleting the link.
- Changing quantity during bind "to record a goods receipt" — bind does not
  change `menge`. Book a `stock_putaway` in phase 5.
- Locking by deleting the object, so a later scan of the found sticker could be
  bound to something else if the code were reissued.
