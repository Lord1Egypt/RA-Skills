---
name: maintenance-inspections
description: Use when an agent must set up maintenance and inspection deadlines on Telesherpa — three scopes (master data, maintenance, team), assets with recurring serviceOrders as the source of truth for each due date, views for overdue / due in 30 days ({today} to {today+30}) / all open inspections (excluding defects) / defects, start cards in the team scope, a form that records an inspection (result, note, photos, signature, date, optional next due date) and updates the same open order, and a form that reports a defect on an asset. Also use when extending or auditing such a workspace.
version: "1.0"
author: Telesherpa
license: MIT
platforms: [linux, macos, windows]
---

# Maintenance and inspection deadlines (Telesherpa industry solution)

**Location in the repo:** `industry-solutions/maintenance-inspections/`, next to
`telesherpa-ontology-platform/` and `industry-solutions/shift-planning/`. Load the
platform skill first (`telesherpa-ontology-platform/SKILL.md`); this skill assumes
you can register, authenticate and call MCP tools.

**Language:** this file is English because agents read it. Answer the customer in
their language. Keep tool names and JSON keys verbatim. **Option values** are plain
English strings with no translation layer (see phase 0). The placeholders
`{today}` and `{today+N}` are platform values — do not replace them with a fixed
date. Labels shown to the customer's staff are set in the label language agreed in
[intake](references/intake.md). **Tool responses and error texts may use the
platform language.** Read the returned allowed keys and error meaning; never
translate keys or option values back into a call.

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
| 3 | The type `serviceOrder` in the maintenance scope carries `dueDate` (date), `intervalDays` (int), `intervalKm` (int, optional), `lastDone` (date), `kind`, `orderKind` (`scheduledInspection` / `defect` / `contractMaintenance` / `inspectionProtocol`), `result` (`pass` / `defect`) and `inspectionNote` | `onto_type_show` |
| 4 | Views exist, and the start cards are registered in the team scope and point at team-scope views | `onto_settings_list` / `onto_interface_index` per scope, `onto_startcard_index` |
| 5 | `record_inspection` is a `form_answer` action bound to its form; `apply_inspection` and its insert and update triggers are present; `report_defect` is present; both actions write to the maintenance scope (`result_scope_id`) | `onto_actiondef_list`, `show_formdef`, function and trigger index/show |
| 6 | Objects per type match the intake (business, site, people, assets, service orders) | `onto_object_index` |
| 7 | One open scheduled inspection really points at its asset, and the due date sits on that order | `onto_object_graph` on the order (`concerns` with linkvalue `ofAsset`); `onto_object_show` (`dueDate`, `kind`, `orderKind`, `orderStatus`) |
| 8 | One real end-to-end step as manager: record an inspection with a result, an inspection date, a photo and a signature; the same order stays `open` and its next due date is either the date typed or, if that field was left empty, the inspection date plus `intervalDays` | the form in the browser, then a read-back of the duty (`result`, `lastDone`, `dueDate`, `orderStatus`) and of the protocol (`orderKind=inspectionProtocol`, `concerns` / `ofOrder`) |
| 9 | One defect reported on an asset appears in the defects view and not in all open inspections | the form action, then the two views |
| 10 | The credit balance you report is the one you measured | `onto_credit_balance` |

A status message names its stage — **"stage X of 2 (0–2)"**. "Everything is set up" is not a
status: it names no phase, no number and no check. If you cannot fill the table, you are
not done, and the correct answer is the missing line, not a summary.

## Status

| Field | Content |
|---|---|
| Verified against | **platform schema 2026-11-16** (Europe/Berlin). Types, properties, links (`concerns` with `ofAsset` and `ofOrder`) and the views, forms, function and triggers below were read with member tools on that date. The manager path — including the record-inspection form, photos, signature and the automatic next due date — was executed and read back in the browser on that date. Treat points marked "(confirm)" as open until they are quoted from your workspace. |
| Status | Version 1.0. Recurring inspection duties as `serviceOrder` rows, the four lists, the team start cards, `record_inspection` (a form; the order stays open; the next due date is typed or computed from the interval) and `report_defect` are in this skill. The checks describe the **manager path**. |
| Platform skill state | Links point to the main branch of the platform skill, read on 2026-11-16. If a linked file has moved, look it up by name and report the broken link; do not guess its content. |
| Industry | Businesses that keep a fleet, tools, devices or machines and must track recurring inspections and defects. ExampleWorks values are examples. |
| Tool count | **Not stated on purpose.** Measure: `GET https://mcp.telesherpa.com/health` (field `tools`) and `auth_status` for what *your* account sees. |

## Goal

Managers maintain sites, people and assets (vehicles, devices, tools, machines)
in master data. Each recurring inspection duty is an open `serviceOrder` in the
maintenance scope: the due date, the interval and the kind live on that order,
not on a second requirement type. The order is linked to its asset with
`concerns` and linkvalue `ofAsset`.

Managers work from start cards on the team door: overdue inspections, inspections
due from `{today}` through `{today+30}`, all open inspections (defects excluded),
and open defects. **Record inspection** opens a form on an open or in-progress
order. Saving it creates a protocol (`serviceOrder` with
`orderKind=inspectionProtocol`) linked to the duty with `concerns` /
`ofOrder`, stores the result, note, photos and signature on that protocol, and
writes `result`, `lastDone` and the next `dueDate` back to the duty. If the next
due date is left empty, it becomes the inspection date plus `intervalDays`; if a
date is entered, that date is used. The duty's `orderStatus` stays open, so the
same row remains on the lists when it is due again. **Report defect** on an
asset creates a new `serviceOrder` with `orderKind=defect` in the maintenance
scope, linked to that asset.

The operating picture — flows, how an agent measures and steers the workspace, and
what the agent never does alone — is in
[operating-model.md](references/operating-model.md).

**Charts and reports: offer them, do not build them yourself.** A member cannot
build a report; order it through the service channel. The
menu, the wording and the request template are in the platform skill:
[reports.md](../../telesherpa-ontology-platform/references/features/reports.md).
What a member *can* build is a block view.

## Definition of Done — per phase, checkable

"The workspace is configured" means one sentence, and it has a test: **a person who has
never seen the build can open the start cards, see overdue and upcoming inspections
with their asset names, record an inspection (result, photo, signature, date, and
either a typed next due date or none) so the same order stays open with the new
due date, and report a defect on an asset — without asking anyone.**
Everything below is a precondition for saying that, not a description of it.

| Phase | Minimum artefact | The proof you must quote |
|---|---|---|
| 0 | three scopes with the agreed suffixes, the rights matrix, types activated, property definitions in the maintenance scope | `ontouser_scope_index` lists three; `onto_type_show` on `serviceOrder` in the maintenance scope quotes the fields above |
| 1 | business and site (reused or created), people, assets, one open `serviceOrder` per agreed duty, each linked `concerns` / `ofAsset` | object counts per type; one order read back with `dueDate`, `kind`, `orderKind` and a single `ofAsset` edge |
| 2 | the four lists (work and team counterparts), start cards on the team door, `record_inspection` (form, function, triggers), `report_defect` | start cards quoted from `onto_startcard_index`; one recorded inspection stays `open` with a computed or typed `dueDate` and a protocol linked `ofOrder`; one defect appears in the defects view and not in all open inspections; saving without a result or without an inspection date is refused |

**The hard rule:** the workspace counts as configured only when
[acceptance-scenario.md](references/acceptance-scenario.md) has run **end to end once** and
its result is quoted, step by step. Until then the status is "stage X of 2".

**"Created" is not "configured".** An object list proves that rows exist. A working
workspace proves that the next person can open the lists, record an inspection and
report a defect.

## Build order — phases 0–2

Every phase file uses the same frame: *goal · definitions · config snippets ·
checks via MCP · checks in the browser · acceptance · typical errors*.

| Phase | File | Core |
|---|---|---|
| 0 | [phase0.md](references/phase0.md) | three scopes, rights matrix, object types, properties, link types, smoke test |
| 1 | [phase1.md](references/phase1.md) | reuse or create sites and people, assets, recurring service orders, `concerns` / `ofAsset` |
| 2 | [phase2.md](references/phase2.md) | views, start cards, `record_inspection` (form, function, triggers), `report_defect` |

Before you start: [prerequisites.md](references/prerequisites.md) →
[intake.md](references/intake.md) (ask the business, do not guess) → phase 0.
End-to-end check: [acceptance-scenario.md](references/acceptance-scenario.md).
Paid test runs: [measurement.md](references/measurement.md).
Operating model: [operating-model.md](references/operating-model.md).

Working conventions for every phase:
- Test objects carry the prefix `TEST-<phase>-` in name and `external_id`.
- Save the current definition (read it, keep the JSON) before you change it.
- **Read back after every write.** A write response describes intent, the read-back describes state.
- **One write at a time.** Do not fire parallel creates of objects or links; a timeout leaves you unsure what landed.

## Core rules (read before phase 0)

Short form. The platform references linked below are authoritative.

1. **The open `serviceOrder` is the source of truth for the deadline.** `dueDate`,
   `intervalDays`, `kind` and `lastDone` hang on the order. Do not treat comfort
   date fields on the asset as the duty, and do not invent a second requirement
   type. One open scheduled order per asset and kind is the duty.
2. **E2 split — basic vs protected.** Master objects hold **basic** data (name,
   login e-mail, site, asset identifiers). Contractor commercial terms do not
   belong on those objects. See
   [scopes-and-permissions.md](../../telesherpa-ontology-platform/references/features/scopes-and-permissions.md).
3. **The asset column needs `concerns` with linkvalue `ofAsset`.** Create that
   value on the edge. An edge with an empty linkvalue leaves the asset name blank
   in the lists. If the edge already exists without the value, update that edge;
   do not add a second `concerns` link. Each scheduled order points to **one**
   asset.
4. **`record_inspection` is a form, and it keeps the duty open.** The action type
   is `form_answer`, bound to a formdef. Saving creates a protocol
   (`orderKind=inspectionProtocol`, `orderStatus=done`) linked to the duty with
   `concerns` / `ofOrder`. Photos and the signature live on the protocol, not on
   the duty. A function `apply_inspection`, run by insert and update triggers on
   that protocol, writes `result`, `inspectionNote`, `lastDone` and `dueDate` to
   the duty. It does **not** set `orderStatus`, `completedAt` or `description` on
   the duty. Closing the duty would drop the recurring row out of the lists.
5. **Next due date: typed date wins, otherwise inspection date plus interval.**
   If `nextduedate` is a real `YYYY-MM-DD` date, that value becomes `dueDate`. If
   the field is left empty, the function uses `date_add(lastdone, intervalDays)`
   on the duty. Empty form fields are not stored, so a placeholder such as
   `{nextduedate}` can arrive as literal text; the function must accept a next
   due date only when it matches `YYYY-MM-DD`.
6. **Photos and signature belong in the formdef, not in action prompts.** Action
   prompts accept only `text`, `textarea`, `int`, `float`, `select`, `picker`,
   `switch`, `date`, `datetime` and `time`. Use form widgets `images` and
   `signature`. Date fields on the form use widget `datepicker` with `mode: date`
   and values `YYYY-MM-DD`. Form widget keys are stored as they are written
   (`lastdone`, `nextduedate`, `result`, `note`); trigger placeholders must use
   those exact keys, not camelCase duty field names.
7. **`report_defect` creates the defect order.** The form action, run on an asset,
   writes a `serviceOrder` with `orderKind=defect` and `orderStatus=open` into the
   maintenance scope and sets `concerns` / `ofAsset`. Recording an inspection with
   `result=defect` does **not** create a second defect order; use `report_defect`
   when a defect order is needed.
8. **All open inspections exclude defects.** That view filters `orderStatus != done`
   and `orderKind != defect`. Defects have their own view (`orderKind = defect`
   and `orderStatus != done`).
9. **The 30-day list is a fixed window.** It filters `orderStatus != done` and
   `dueDate >= {today}` and `dueDate <= {today+30}`. The placeholders stay stored
   as `{today}` and `{today+30}`; do not replace them with a fixed date. The
   window is not a navigable period. Overdue is `orderStatus != done` and
   `dueDate < {today}`.
10. **Start cards live in the team scope and point at team-scope views.** A card
    that points at a work-scope view is rejected (HTTP 400). Install the
    counterparts in the team scope first, then the cards.
11. **List rows need a hidden `udid` column for row actions.** Put system column
    `udid`, `hidden: true`, first. Then `row_actions` can run `record_inspection`
    on the row and can include a detail link `ontouser/object/show/{udid}`.
    Without the hidden column, the row action has no object to run on.
12. **Do not set `data_scope_id` on the inspection lists.** A person-binding on
    the view would hide unassigned orders.
13. **Action conditions use operator `ne`, not `neq`.** Unknown operators are not
    treated as a match, so a condition written with `neq` can hide the button.
    View filters use operators such as `!=`, `<`, `>=`, `<=`.
14. **Rights are fail-closed.** No grant means no access; an empty list means empty.
    Set read, write and manage explicitly.
15. **Delete one id at a time.** Never by name, prefix or pattern. Deleting costs
    the `delete_*` price from the live table (see prerequisites).
16. **UDIDs always lower case.** Mixed case silently never matches.
17. **Every manager view in the maintenance scope sets `view_config.access.require`
    to `write`.** Team counterparts of the deadline and defect lists set
    `access.require` to the maintenance scope id. The asset list used to report a
    defect has no such gate.
18. **Create an action with exactly one scope in `body.scopes`.** Add further
    scopes in a later save. A create call with several scopes is rejected (HTTP 400).
19. **`ontouser_scope_types_set` replaces the list.** Include every type the scope
    must keep.
20. **Time:** stored and returned as **UTC**, with the `_local`/`value_local` sibling in the viewer's zone. **Naive input is read in the viewer's zone** (default `Europe/Berlin`, measured 2026-11-25: `2026-11-10 09:00:00` is stored as `08:00:00` UTC); append `Z` or an offset (`2026-11-10T09:00:00Z`) and it is taken literally.
21. **Prices only from the live list.** Call `onto_credit_pricing` at the start of
    the run. Do not copy a price table from memory or from this skill. The platform
    skill and [tool-traps.md](../../telesherpa-ontology-platform/references/features/tool-traps.md)
    describe how to read it.

### Link types of this solution — use these, invent none

| Link | Direction | What it carries |
|---|---|---|
| `concerns` (linkvalue `ofAsset`) | **serviceOrder → asset** (`car`, `device`, `tool`, `machine`, `building`) | the asset the duty or defect is about. Set when the order is created; required for the asset column |
| `concerns` (linkvalue `ofOrder`) | **protocol → duty** (both `serviceOrder`) | the open inspection the protocol belongs to. Set by `record_inspection` |
| `bestehtAus` | organisation → building (and further, if used) | the site tree, same as shift-planning |

**No invention.** A link type that is not in `onto_link_index` with matching `types1`
and `types2` for the pair you need does not exist for you. And: a link you have not
read back with `onto_object_graph` or `onto_object_show` does not exist in the
report either.

Platform references (do not duplicate them here):

| Topic | Reference |
|---|---|
| Scopes, rights, three-scope pattern | [scopes-and-permissions.md](../../telesherpa-ontology-platform/references/features/scopes-and-permissions.md) |
| Scope bridges (`result_scope_id`) | [scope-bridges.md](../../telesherpa-ontology-platform/references/features/scope-bridges.md) |
| Tool traps, prices, time, async triggers | [tool-traps.md](../../telesherpa-ontology-platform/references/features/tool-traps.md) and [references/tool-traps.md](references/tool-traps.md) |
| Reports and charts — what to order for the manager | [reports.md](../../telesherpa-ontology-platform/references/features/reports.md) |
| Member-agent rules | [member-agent-rules.md](../../telesherpa-ontology-platform/references/features/member-agent-rules.md) |
| Notifications | [notifications-and-link-events.md](../../telesherpa-ontology-platform/references/features/notifications-and-link-events.md) |
| Start cards | [start-cards.md](../../telesherpa-ontology-platform/references/features/start-cards.md) |
| Forms | [form-engine.md](../../telesherpa-ontology-platform/references/features/form-engine.md) |
| Block views | [view-blocks.md](../../telesherpa-ontology-platform/references/features/view-blocks.md) |
| Triggers and functions | [automation-and-functions.md](../../telesherpa-ontology-platform/references/features/automation-and-functions.md) |
| Managed staff accounts, invite codes | [company-manager.md](../../telesherpa-ontology-platform/references/features/company-manager.md) |
| People, sites, three-scope recipe | [shift-planning](../shift-planning/SKILL.md), especially phase 0 and phase 1 |

## Stop and escalate

Stop, do not improvise, and report when any of these happens. **Inventing a
workaround is forbidden** — e.g. closing a recurring order so it "looks done",
inventing a second requirement type, or leaving `concerns` without `ofAsset`
because the name "still shows in the object header".

| Situation | What you do |
|---|---|
| HTTP **402** | The executing account has no credits. Check `onto_credit_balance` of *that* account. Stop and ask for credits. Do not retry. |
| HTTP **403** / scope write refused | Check rights. If the design says the account must not have the right, the fix is a bridge or a gate, not a grant. |
| HTTP **400** on `record_inspection` when dates are filled | Check that the form date widgets use `mode: date` and the client sent `YYYY-MM-DD`. Fix the definition; do not widen fields to date-time. |
| Required object type missing from `ontouser_scope_types` / `onto_type_show` | Stop. File `ontouser_service_request` (template in [prerequisites.md](references/prerequisites.md)). Do not substitute another type silently. |
| A tool reports unknown parameters | Read the allowed keys and fix the call once. If the documented parameter is not accepted, stop and report (the skill is out of date). |
| Smoke test (phase 0) deviates from this skill | Stop before building. Report the deviation with tool, call and response. |
| MCP timeout / connection drop on a write | Read back. Only repeat if the read-back proves nothing was written. |
| 3 consecutive failed attempts at the same step, or spend above the agreed budget | Stop and report (see [measurement.md](references/measurement.md)). |
| The business is not on Europe/Berlin time | Stop before phase 0 and file `ontouser_service_request`. |
| Anything that would message real people outside a test | Ask the human first. |
| Intake answer missing (sites, kinds and intervals, who records inspections) | Ask; do not assume ExampleWorks defaults for a real customer. |
| **You are about to report completion** | Stop. Run the checks above and quote the values. |

Report format (to the human and, for platform faults, via `ontouser_service_request`
with `category: "bug"`): what you tried (tool + arguments without secrets), what you
expected, what came back (status + error text), what you did not do because of it.

### Report shape — use this, every time

```
Stage X of 2 (0–2).

| Check | Value read back |
|---|---|
| scopes                | 3 — …_master, …_maintenance, …_team |
| objects per type      | person …, building …, car …, device …, tool …, machine …, serviceOrder … |
| views / start cards   | four work lists + five team views; five start cards on the team door |
| actions               | record_inspection (form_answer, order stays open), apply_inspection, report_defect |
| sample order          | concerns/ofAsset → asset … ; dueDate … ; orderStatus open |
| last inspection       | result / lastDone / dueDate quoted (typed or computed); protocol ofOrder; orderStatus still open |
| last defect           | one open defect on the asset; not in all open inspections |
| acceptance steps      | k of 17 passed (0.1 … 2.8), negative tests m of 2 open |

Not done: <bullet list, each with the stage it belongs to>
```

Two lines are forbidden in this report: "everything is set up" and "done". The
count of passed acceptance steps is the only honest answer to "are you finished" —
the scenario has **17 steps** (0.1 … 2.8) and **2 negative tests** (N1–N2).
Both counts are in the acceptance file; do not restate them from memory.

## Reference files

- [prerequisites.md](references/prerequisites.md) — account, rights, credits, live price list, missing types
- [intake.md](references/intake.md) — questionnaire for the business
- [phase0.md](references/phase0.md) — scopes, rights, types, properties, smoke test
- [phase1.md](references/phase1.md) — sites, people, assets, recurring service orders
- [phase2.md](references/phase2.md) — views, start cards, record inspection, report defect
- [glossary.md](references/glossary.md) — terms and keys
- [country-de.md](references/country-de.md) — Germany: display labels
- [acceptance-scenario.md](references/acceptance-scenario.md) — end-to-end test with expected values
- [definition-of-done.md](references/definition-of-done.md) — the audit before any status report
- [measurement.md](references/measurement.md) — paid test run: budget, stop criteria, log template
- [publication-check.md](references/publication-check.md) — what must never be in this public skill
- [operating-model.md](references/operating-model.md) — maintenance control: flows, agent loop, limits
- [tool-traps.md](references/tool-traps.md) — solution-specific traps
