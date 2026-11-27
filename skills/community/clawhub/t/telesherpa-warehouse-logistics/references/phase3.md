# Phase 3 — staff accounts, scan, start card, short URL

**Goal:** a staff member can bind a free label to a package with a single scan, the
start card leads them to the scan page, and the short URL hides the object name
until sign-in.

**Input:** phase 2 gate passed; intake 10, 12, 23.

Staff accounts, invitations and transfers follow
[company-manager.md](../../../telesherpa-ontology-platform/references/features/company-manager.md)
and the staff-account recipe in
[shift-planning phase 3](../../shift-planning/references/phase3.md) — reuse that
pattern, do not invent another one. The master `person.email` must equal the login.

---

## 1. Definitions

### 1.1 Staff path

- Rights as in phase 0: read on master, no membership on warehouse, read+write on
  the team door.
- `label_bind` for staff lives in the team scope, with
  `action.result_scope_id = <warehouse_scope_id>`, `scan.ein_code`, the package
  prompt, and a guard if only warehouse staff (not kitchen) may bind.
- Give the staff account a small credit balance (`ontouser_team_transfer`) before
  the first scan. A 402 is not a bind failure of the skill if you top up at once;
  log it.

### 1.2 Scan page

The bundled page is `GET /ontouser/scan` (role `member`). The contract is HTTP,
not MCP: `POST /onto/object/match_actions`, `execute_action`, `counter`. See
[scan-and-checkpoints.md](../../../telesherpa-ontology-platform/references/features/scan-and-checkpoints.md)
for `ein_code`, prompts, `blockiert`, `dedupe_ms` and feedback. The staff action
in this phase is `label_bind` after a **single** scan of a free label.

### 1.3 Start card

Register a start card in the team scope with `onto_startcard_save` and read it
back with `onto_startcard_index`. It should lead staff to the scan page and, if
you build one, to a team view of "labels I bound today" (only if that view can be
fed without granting warehouse read — confirm). Follow
[start-cards.md](../../../telesherpa-ontology-platform/references/features/start-cards.md).
A card has no roles: it is visible when the scope is readable **and** the target
view is in the interface list. **Do not** point the card at a manager view that
lives in the warehouse scope.

### 1.4 Short URL

The sticker carries the public-app short URL `/q/<code>` (the printed origin is
the public app host). Behaviour that is already proven:

- **Before sign-in:** the object name is not shown.
- **After sign-in:** a bound, not-locked label resolves to the linked object
  (the package it identifies, or the label that points at it — quote which one
  you observed).
- A `gesperrt` label must not resolve to the package.

---

## 2. Recipe

1. Create and activate the staff account for M1. Set rights. Transfer credits.
   Read back `ontouser_team_show`.
2. Save the start card. Quote `onto_startcard_index`.
3. As M1, open the scan page, scan a **free** label, confirm `label_bind` is
   offered (`ein_code`), pick package B, execute. Read back as manager:
   `labelStatus=gebunden`, `identifies` → package B, one row later in the
   action log (phase 4 will quote it).
4. As M1, request `onto_object_show` on that warehouse label UDID. Expect 404 /
   no access (confirm). The bind must still have succeeded.
5. Fetch `/q/<code>` **logged out** for a bound label: no object name.
6. Fetch `/q/<code>` **as M1** for the same bound label: the package is reachable.
7. Fetch `/q/<code>` for a `gesperrt` label: it does not open the package.

---

## 3. Checks via MCP

- Staff rights quoted: no warehouse membership, master read, team read+write.
- Start card row quoted.
- Label bound by M1: graph and status quoted.
- Staff show of the warehouse label: no access (confirm).

## 4. Checks in the browser (staff M1, plus one logged-out session)

- Start card is the first thing M1 sees and opens the scan page.
- A single scan of a free label offers bind and asks for the package.
- Short URL behaviour in §1.4 is visible, not only assumed from MCP.
- Manager-only buttons (print, lock) are invisible to M1. Direct execution is
  denied (negative test N5).

## 5. Phase gate

A staff bind, the start card, and both short-URL cases are quoted. Status:
"Stage 3 of 5 complete".

## 6. Typical errors

- Granting warehouse read after step 4 fails.
- Putting a warehouse manager view on the team start card.
- Testing only the MCP execute path and skipping the camera / scan page.
- Using a checkpoint-style QR that contains a raw UDID instead of the printed
  short URL.
