---
name: warehouse-logistics
description: Use when an agent must set up warehouse logistics with QR labels on Telesherpa — three scopes (master data, warehouse, team), packages with quantity, lot and best-before, printed labels with their own codes, single-scan bind and rebind, Avery 3475 print sheets, and single-scan stock bookings (putaway, pick, relocate, count) that write a stockMovement and update package quantity. Also use when extending or auditing such a workspace.
version: "1.0"
author: Telesherpa
license: MIT
platforms: [linux, macos, windows]
---

# Warehouse logistics with QR labels (Telesherpa industry solution)

**Location in the repo:** `industry-solutions/warehouse-logistics/`, next to
`telesherpa-ontology-platform/` and `industry-solutions/shift-planning/`. Load the
platform skill first (`telesherpa-ontology-platform/SKILL.md`); this skill assumes
you can register, authenticate and call MCP tools.

**Language:** this file is English because agents read it. Answer the customer in
their language. Keep tool names and JSON keys verbatim. **Option values** are plain
strings with no translation layer. One exception is documented in phase 0: the
platform actions `label_bind` and `label_rebind` are proven against the platform
values `frei`, `gebunden` and `gesperrt` — do not replace them. Other option values
you create yourself are English (see phase 0). Labels shown to the customer's staff
are set in the label language agreed in [intake](references/intake.md). **Tool
responses and error texts may use the platform language.** Read the returned allowed
keys and error meaning; never translate keys or option values back into a call.

**Reuse, do not copy.** People, sites (`organisation`, `building`) and the
three-scope pattern already live in
[shift-planning](../shift-planning/SKILL.md). If that workspace exists for the same
business, reuse its master data (and, if the intake says so, its team door). Link to
those files; do not duplicate their recipes here.

## Before you claim anything — the checks

**A workspace is not set up because objects exist.** Before you write any progress or
completion report, run these checks and quote the values you read back. A statement
without numbers from a read-back is a claim, not a status.

| # | Check | Query |
|---|---|---|
| 1 | The three scopes exist with the agreed suffixes, and you are manager of all three | `ontouser_scope_index` |
| 2 | Per scope: number of objects, members, managers | `onto_scope_index` (fields `obj_count`, `user_count`, `manager_count`) |
| 3 | The type `label` carries `code`, `charge`, `labelStatus` (`frei` / `gebunden` / `gesperrt`), `printedAt`, `printedBy`; `package` carries `menge` (int), `einheit`, `lot` and `bestBefore`; `stockMovement` carries `movementType`, `menge`, `einheit`, `grund`, `bookingTime`, `bookedBy` | `onto_type_show` |
| 4 | Views exist, and the start card is registered | `onto_settings_list` per scope, `onto_startcard_index` |
| 5 | `label_bind`, `label_rebind`, `stock_putaway`, `stock_pick`, `stock_relocate` and `stock_count` are present; each stock action points at a function whose `scopes` include the package's scope; every manager action carries `require_scope_write` | `onto_actiondef_list`, `onto_function_index` |
| 6 | Objects per type match the intake (business, site, people, storage, packages, labels) | `onto_object_index` |
| 7 | One bound label really points at a package, and the quantity sits on that package | `onto_object_graph` on the label (`identifies`); `onto_object_show` on the package (`menge`, `einheit`, `lot`, `bestBefore`) and on the label (no `menge`) |
| 8 | One real end-to-end step as staff: a free label is bound through a single scan | the scan (`GET /ontouser/scan` or the HTTP contract in the platform scan chapter), then a read-back of `labelStatus` and the `identifies` edge |
| 9 | A print sheet for one charge exists; a reprint of that charge creates no new labels | the PDF, opened and read; `onto_object_index` counts for that `charge` before and after |
| 10 | One manager booking each of `stock_putaway`, `stock_pick`, `stock_relocate` and `stock_count`, plus one `label_rebind`, was read back (quantity, movement, `moves` / `movesTo`, `identifies`) | `onto_object_execute_action` then `onto_object_show` |
| 11 | The credit balance you report is the one you measured | `onto_credit_balance` |

A status message names its stage — **"stage X of 5 (0–5)"**. "Everything is set up" is not a
status: it names no phase, no number and no check. If you cannot fill the table, you are
not done, and the correct answer is the missing line, not a summary.

## Status

| Field | Content |
|---|---|
| Verified against | **platform schema 2026-11-13** (Europe/Berlin). Types, properties, links (`identifies`, `moves`, `movesTo`) and the catalogue preset `lager` were read with member tools on that date. Stock bookings and `label_rebind` were executed and read back on that date. Treat points marked "(confirm)" as open until they are quoted from your workspace. |
| Status | Version 1.0. Labels, print sheets, single-scan bind and rebind, the three-scope layout, and single-scan putaway, pick, relocate and count (each writing a `stockMovement` and updating `menge`) are in this skill. |
| Platform skill state | Links point to the main branch of the platform skill, read on 2026-11-13. The platform skill may not document the `label` type, the short URL `/q/<code>`, `label_bind`, `label_rebind`, `identifies`, Avery 3475 print, `stockMovement` or the stock actions. For those topics this file and a live `onto_type_show` / `onto_link_index` / `onto_actiondef_list` win. If a linked file has moved, look it up by name and report the broken link; do not guess its content. |
| Industry | Restaurants and other businesses that store goods in packages and scan labels. Restaurant values are examples (DemoRestaurant). |
| Tool count | **Not stated on purpose.** Measure: `GET https://mcp.telesherpa.com/health` (field `tools`) and `auth_status` for what *your* account sees. |

## Goal

Managers maintain sites, storage locations, packages and printed labels. A package
carries its book quantity (`menge`), unit (`einheit`), lot (`lot`) and best-before
date (`bestBefore`). A label is only a pointer: it has its own code, it can be
printed, locked, issued more than once for the same package, and rebound onto
another package by leadership. A single scan binds a **free** label to a package.
Staff reach the bind action through the team door and the scan page. After sign-in,
the short URL on the sticker opens the linked package; **before** sign-in the object
name is not shown.

Managers book stock through single-scan actions on the package: put away, pick,
relocate and count. Each booking creates a `stockMovement` and updates `menge` in
the same run. The place named in the prompt is recorded on the movement as
`movesTo`.

The operating picture — flows, how an agent measures and steers the warehouse, and
what the agent never does alone — is in
[operating-model.md](references/operating-model.md).

**Charts and reports: offer them, do not build them yourself.** A member cannot
build a report; order it through the service channel. The
menu, the wording and the request template are in the platform skill:
[reports.md](../../telesherpa-ontology-platform/references/features/reports.md).
What a member *can* build is a block view and, where the view allows it, a CSV of
labels, packages and movements for the manager (phase 4).

## Definition of Done — per phase, checkable

"The workspace is configured" means one sentence, and it has a test: **a person who has
never seen the build can print a sheet of labels, stick one on a package, bind it with
a single scan, see the quantity on that package, and a manager can put away, pick,
relocate and count that package — without asking anyone.**
Everything below is a precondition for saying that, not a description of it.

| Phase | Minimum artefact | The proof you must quote |
|---|---|---|
| 0 | three scopes with the agreed suffixes, the rights matrix, types activated, functions and actions installed in matching scopes, the smoke test | `ontouser_scope_index` lists three; the staff test returns **403** on the warehouse scope; `onto_type_show` on `label`, `package` and `stockMovement` quotes the fields above; `onto_function_index` shows `stock_move_apply` and `stock_count_apply` with the package scope in `scopes` |
| 1 | business and site (reused or created), people, storage locations, packages with `menge`/`einheit`/`lot`/`bestBefore`, one label charge, one print sheet | object counts per type; one package read back with quantity, lot and best-before; one label read back with `code`, `charge` and `labelStatus=frei` |
| 2 | bind, several labels on one package, lock, reprint of the same charge | `identifies` on a bound label; four labels on one package; a locked label no longer resolves; label count for the charge unchanged after reprint |
| 3 | staff accounts, start card, a bind performed as staff through a single scan, short-URL behaviour | the staff login binds a free label; `/q/<code>` hides the name before sign-in and opens the package after |
| 4 | action-log evidence and a manager list or CSV of labels, packages and movements | one `label_bind` row in `onto_action_logs`; the list or CSV opened and read |
| 5 | putaway, pick, relocate, count and label rebind, each read back | `menge` after putaway and pick; unchanged `menge` after relocate; absolute `menge` after count; `identifies` on the new package after rebind; each movement has `moves` and `movesTo` |

**The hard rule:** the workspace counts as configured only when
[acceptance-scenario.md](references/acceptance-scenario.md) has run **end to end once** and
its result is quoted, step by step. Until then the status is "stage X of 5".

**"Created" is not "configured".** An object list proves that rows exist. A working
workspace proves that the next person can print, stick, bind and book.

## Build order — phases 0–5

Every phase file uses the same frame: *goal · definitions · config snippets ·
checks via MCP · checks in the browser (per role) · acceptance · typical errors*.

| Phase | File | Core |
|---|---|---|
| 0 | [phase0.md](references/phase0.md) | three scopes, rights matrix, object types, properties, link types, functions, actions, smoke test |
| 1 | [phase1.md](references/phase1.md) | reuse or create sites and people, storage, packages, a label charge, Avery 3475 print, manager lists |
| 2 | [phase2.md](references/phase2.md) | `label_bind`, several labels on one package, lock (`gesperrt`), reprint of the same charge |
| 3 | [phase3.md](references/phase3.md) | staff accounts, scan page, start card, short URL before and after sign-in |
| 4 | [phase4.md](references/phase4.md) | action log, manager list or CSV of labels, packages and movements |
| 5 | [phase5.md](references/phase5.md) | `stock_putaway`, `stock_pick`, `stock_relocate`, `stock_count`, `label_rebind`, lot and best-before |

Before you start: [prerequisites.md](references/prerequisites.md) →
[intake.md](references/intake.md) (ask the business, do not guess) → phase 0.
End-to-end check: [acceptance-scenario.md](references/acceptance-scenario.md).
Paid test runs: [measurement.md](references/measurement.md).
Operating model: [operating-model.md](references/operating-model.md).

Working conventions for every phase:
- Test objects carry the prefix `TEST-<phase>-` in name and `external_id`.
- Save the current definition (read it, keep the JSON) before you change it.
- **Read back after every write.** A write response describes intent, the read-back describes state.
- Leave e-mail/push off on notification rules unless the intake asks for a notice you can actually send and test.

## Core rules (read before phase 0)

Short form. The platform references linked below are authoritative.

1. **Staff have no right on the warehouse scope** (neither read nor write) and
   **read (no write) on master**. They reach a label **through the scan** (the code
   on the sticker), not through a warehouse membership. Writing the bind goes
   through a **scope bridge** (`action.result_scope_id`) limited to the keys in
   `action.props` and the `identifies` link. Do not grant warehouse read "so the
   scan works". If a staff bind fails because the object is unreachable, stop and
   report — do not widen rights as a workaround. Stock bookings in this skill are
   described on the **manager path** (an account with write on the warehouse and
   on the package's scope). Do not tell the customer that staff can book putaway,
   pick, relocate or count through the team door unless you have measured that
   path in *this* workspace.
2. **E2 split — basic vs protected.** Master objects that staff can read hold only
   **basic** data (name, login e-mail, site, storage location, package name, `menge`,
   `einheit`, `lot`, `bestBefore`). Supplier terms and purchase prices do not belong
   on staff-readable master objects. See
   [scopes-and-permissions.md](../../telesherpa-ontology-platform/references/features/scopes-and-permissions.md).
3. **A label is a pointer, not the stock.** `menge` (int), `einheit`, `lot` and
   `bestBefore` hang on the `package`. They do not hang on the label. Several labels
   may identify one package (proven: four labels on one crate). Each label points to
   **at most one** package (`identifies` is unique on the label side).
4. **The code is not the object UDID.** The platform assigns a Crockford Base32
   code (12 characters plus a check digit, without `I`, `L`, `O`, `U`). You never
   invent the code. The sticker prints it as the public-app short URL `/q/<code>`.
   After sign-in the scan opens the linked object; before sign-in the object name is
   not visible. Checkpoint codes in the platform skill still use a raw UDID — that
   is a different feature; do not put a UDID in a warehouse label.
5. **`label_bind` is a single-scan action** (`scan.ein_code`). Condition:
   `labelStatus` is `frei`. The action prompts for the package (`object_types:
   [package]`, the client fills the UDID), sets the link `identifies` and
   `labelStatus=gebunden`. A second bind is rejected (`require: absent`) — proven
   result: HTTP 400, platform message that the precondition is not met. To hang an
   already bound label on another package, use `label_rebind` (phase 5).
6. **Status values** on `labelStatus`: `frei` | `gebunden` | `gesperrt`. `gesperrt`
   means the sticker is intentionally dead (lost or replaced) and must no longer
   resolve. Do not rename these values.
7. **Print.** A charge of labels is printed on Avery Zweckform 3475, 70 × 36 mm,
   3 × 8 = 24 labels per A4 sheet, QR 26 mm, error-correction level M, the code
   readable in groups of four, the charge on the PDF. A reprint of the **same**
   charge must not create new labels. Discover the live print action or view with
   `onto_actiondef_list` and the type's interfaces; do not invent a tool name. If
   no print path is visible after the types are activated, stop and file
   `ontouser_service_request`.
8. **Rights are fail-closed.** No grant means no access; an empty list means empty.
   Set read, write and manage explicitly.
9. **Delete one id at a time.** Never by name, prefix or pattern. Deleting costs
   the `delete_*` price from the live table (see prerequisites).
10. **UDIDs always lower case.** Mixed case silently never matches.
11. **Every manager view sets `view_config.access.require`.** Every manager action
    sets `require_scope_write: <warehouse_scope_id>`. Staff-only-own-row actions
    carry a guard in the live format
    (`"guards": [{"type": "linked_to_user", "linktype": "…", "message": "…"}]`).
    See [scope-bridges.md](../../telesherpa-ontology-platform/references/features/scope-bridges.md).
    Install `label_rebind` with `require_scope_write` so only leadership can run it.
12. **Unlink with `remove: "pair"`**, never `remove: true`. `label_rebind` already
    replaces `identifies` on the label side (`replace: "source"`) and the execute
    response reports the removed edge as `links_entfernt`.
13. **Time:** stored and returned as **UTC**, with the `_local`/`value_local` sibling in the viewer's zone. **Naive input is read in the viewer's zone** (default `Europe/Berlin`, measured 2026-11-25: `2026-11-10 09:00:00` is stored as `08:00:00` UTC); append `Z` or an offset (`2026-11-10T09:00:00Z`) and it is taken literally.
14. **Scan routes are not an MCP tool.** `POST /onto/object/match_actions`,
    `POST /onto/object/execute_action`, `POST /onto/object/counter` and
    `GET /ontouser/scan` run over HTTP with session/bearer (role `member`). Details:
    [scan-and-checkpoints.md](../../telesherpa-ontology-platform/references/features/scan-and-checkpoints.md).
    Use that chapter for the server contract, `ein_code`, prompts, `require`,
    feedback and `dedupe_ms`. The stock actions in this skill are single-scan
    (`scan.ein_code`): one code identifies the package, then the action prompts
    for quantity and, where required, the storage location.
15. **Prices only from the live list.** Call `onto_credit_pricing` at the start of
    the run. Do not copy a price table from memory or from this skill. The platform
    skill and [tool-traps.md](../../telesherpa-ontology-platform/references/features/tool-traps.md)
    describe how to read it.
16. **Change `menge` only by booking a movement.** Putaway adds the booked quantity,
    pick subtracts it, relocate leaves it unchanged, count sets it to the counted
    quantity. Do not use `onto_object_set_property` on `menge` to "correct" stock.
17. **The stock action and its function must be allowed in the package's scope.**
    If the function's `scopes` list does not include that scope, the execute call
    returns HTTP 403 with the platform message that the function is not allowed in
    this scope, and no movement is written. Fix the function (or install the
    canonical keys so action and function share the same scopes). Do not widen
    account rights as a workaround.

### Link types of this solution — use these, invent none

| Link | Direction | What it carries |
|---|---|---|
| `identifies` | **label → package** | the package the sticker points at. Unique on the label side. Set by `label_bind`, moved by `label_rebind` |
| `moves` | **stockMovement → package** | the package the booking applies to |
| `movesTo` | **stockMovement → storage** | the storage location named in the booking prompt |
| `bestehtAus` | organisation → building (and further, if used) | the site tree, same as shift-planning |
| `hasfile` | any → file | the print PDF and attachments |

The type also defines `movesFrom` (movement → storage). The shipped functions
record the prompted place on `movesTo`. Quote what you read back; do not invent a
second place link in the report if it is not there.

**No invention.** A link type that is not in `onto_link_index` with matching `types1`
and `types2` for the pair you need does not exist for you. `identifies` is defined
**label → package** only. And: a link you have not read back with `onto_object_graph`
or `onto_object_show` does not exist in the report either.

Platform references (do not duplicate them here):

| Topic | Reference |
|---|---|
| Scopes, rights, three-scope pattern | [scopes-and-permissions.md](../../telesherpa-ontology-platform/references/features/scopes-and-permissions.md) |
| Scope bridges (`result_scope_id`) | [scope-bridges.md](../../telesherpa-ontology-platform/references/features/scope-bridges.md) |
| Tool traps, prices, time, async triggers | [tool-traps.md](../../telesherpa-ontology-platform/references/features/tool-traps.md) and [references/tool-traps.md](references/tool-traps.md) |
| Reports, charts, CSV — what to order for the manager | [reports.md](../../telesherpa-ontology-platform/references/features/reports.md) |
| Member-agent rules | [member-agent-rules.md](../../telesherpa-ontology-platform/references/features/member-agent-rules.md) |
| Notifications | [notifications-and-link-events.md](../../telesherpa-ontology-platform/references/features/notifications-and-link-events.md) |
| Start cards | [start-cards.md](../../telesherpa-ontology-platform/references/features/start-cards.md) |
| Forms | [form-engine.md](../../telesherpa-ontology-platform/references/features/form-engine.md) |
| Block views | [view-blocks.md](../../telesherpa-ontology-platform/references/features/view-blocks.md) |
| Triggers and functions | [automation-and-functions.md](../../telesherpa-ontology-platform/references/features/automation-and-functions.md) |
| Managed staff accounts, invite codes | [company-manager.md](../../telesherpa-ontology-platform/references/features/company-manager.md) |
| QR scan (HTTP, not MCP) | [scan-and-checkpoints.md](../../telesherpa-ontology-platform/references/features/scan-and-checkpoints.md) |
| QR checkpoint rounds (different feature: UDID on the point) | [checkpoint-rounds.md](../../telesherpa-ontology-platform/references/best_practices/checkpoint-rounds.md) |
| People, sites, three-scope recipe | [shift-planning](../shift-planning/SKILL.md), especially phase 0 and phase 1 |

## Stop and escalate

Stop, do not improvise, and report when any of these happens. **Inventing a
workaround is forbidden** — e.g. granting staff warehouse read, inventing label
codes, putting quantity on the label, or editing `menge` by hand instead of
booking a movement.

| Situation | What you do |
|---|---|
| HTTP **402** | The executing account has no credits. Check `onto_credit_balance` of *that* account. Stop and ask for credits. Do not retry. |
| HTTP **403** / scope write refused | Check rights. If the design says the account must not have the right, the fix is a bridge or a gate, not a grant. If the message says the function is not allowed in this scope, align the function's `scopes` with the package's scope and retry once. |
| Required object type missing from `ontouser_scope_types` / `onto_type_show` | Stop. File `ontouser_service_request` (template in [prerequisites.md](references/prerequisites.md)). Do not substitute another type silently. |
| No print path is visible for Avery 3475 after types are activated | Stop and file a service request. Do not generate QR images from UDIDs yourself. |
| A tool reports unknown parameters | Read the allowed keys and fix the call once. If the documented parameter is not accepted, stop and report (the skill is out of date). |
| Smoke test (phase 0) deviates from this skill | Stop before building. Report the deviation with tool, call and response. |
| MCP timeout / connection drop on a write | Read back. Only repeat if the read-back proves nothing was written. |
| 3 consecutive failed attempts at the same step, or spend above the agreed budget | Stop and report (see [measurement.md](references/measurement.md)). |
| The business is not on Europe/Berlin time | Stop before phase 0 and file `ontouser_service_request`. |
| Anything that would message real people outside a test | Ask the human first. |
| Intake answer missing (sites, units, who may bind, who may book, how labels are handed out) | Ask; do not assume DemoRestaurant defaults for a real customer. |
| **You are about to report completion** | Stop. Run the checks above and quote the values. |

Report format (to the human and, for platform faults, via `ontouser_service_request`
with `category: "bug"`): what you tried (tool + arguments without secrets), what you
expected, what came back (status + error text), what you did not do because of it.

### Report shape — use this, every time

```
Stage X of 5 (0–5).

| Check | Value read back |
|---|---|
| scopes                | 3 — …_master, …_warehouse, …_team |
| objects per type      | person 3, building 1, storage 2, package 2, label 24, stockMovement … |
| views / start card    | … ; start card "Scan" |
| actions               | label_bind, label_rebind, stock_putaway, stock_pick, stock_relocate, stock_count; manager actions gated |
| functions             | stock_move_apply and stock_count_apply, scopes include the package scope |
| bound label           | identifies → package … ; menge n on the package |
| last bookings         | putaway / pick / relocate / count quoted with menge and movesTo |
| acceptance steps      | k of 38 passed (0.1 … 5.8), negative tests m of 14 open |

Not done: <bullet list, each with the stage it belongs to>
```

Two lines are forbidden in this report: "everything is set up" and "done". The
count of passed acceptance steps is the only honest answer to "are you finished" —
the scenario has **38 steps** (0.1 … 5.8) and **14 negative tests** (N1 … N14).
Both counts are in the acceptance file; do not restate them from memory.

## Reference files

- [prerequisites.md](references/prerequisites.md) — account, rights, credits, live price list, missing types
- [intake.md](references/intake.md) — questionnaire for the business
- [phase0.md](references/phase0.md) — scopes, rights, types, properties, functions, actions, smoke test
- [phase1.md](references/phase1.md) — sites, people, storage, packages, label charge, print
- [phase2.md](references/phase2.md) — bind, lock, reprint
- [phase3.md](references/phase3.md) — staff scan, start card, short URL
- [phase4.md](references/phase4.md) — action log, manager list or CSV
- [phase5.md](references/phase5.md) — stock bookings, rebind, lot and best-before
- [glossary.md](references/glossary.md) — terms and keys
- [country-de.md](references/country-de.md) — Germany: display labels
- [acceptance-scenario.md](references/acceptance-scenario.md) — end-to-end test with expected values
- [definition-of-done.md](references/definition-of-done.md) — the audit before any status report
- [measurement.md](references/measurement.md) — paid test run: budget, stop criteria, log template
- [publication-check.md](references/publication-check.md) — what must never be in this public skill
- [operating-model.md](references/operating-model.md) — warehouse control: flows, agent loop, limits
- [tool-traps.md](references/tool-traps.md) — warehouse-specific traps
