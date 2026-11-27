---
name: shift-planning
description: Use when an agent must set up shift planning for a restaurant or other shift-based business on Telesherpa — three scopes (master data, planning, team), shifts from templates, staff self-service (requests, swaps, clock in/out) through a team door, notifications to affected people only, and a monthly planned-vs-actual CSV for payroll. Also use when extending or auditing such a workspace.
version: 1.2.3
author: Telesherpa
license: MIT
platforms: [linux, macos, windows]
---

# Shift planning for restaurants (Telesherpa industry solution)

**Location in the repo:** `industry-solutions/shift-planning/`, next to
`telesherpa-ontology-platform/`. Load the platform skill first
(`telesherpa-ontology-platform/SKILL.md`); this skill assumes you can register,
authenticate and call MCP tools.

**Language:** this file is English because agents read it. Answer the customer in
their language. Keep tool names and JSON keys verbatim. **Option values** are plain
strings with no translation layer — create **scope-specific** property definitions in
the customer scopes with **English** option values (see phase 0); do not build on the
platform's German default values. Labels shown to the
customer's staff are set in the label language agreed in [intake](references/intake.md).
**Tool responses and error texts may use the platform language.** Read the returned
allowed keys and error meaning; never translate keys or option values back into a call.

## Before you claim anything — twelve checks

**A workspace is not set up because objects exist.** Before you write any progress or
completion report, run these checks and quote the values you read back. A statement
without numbers from a read-back is a claim, not a status.

| # | Check | Query |
|---|---|---|
| 1 | The three scopes exist with the agreed suffixes, and you are manager of all three | `ontouser_scope_index` |
| 2 | Per scope: number of objects, members, managers | `onto_scope_index` (fields `obj_count`, `user_count`, `manager_count`) |
| 3 | Scope-specific property definitions exist (stations, contract types, status/kind sets) — not only the platform defaults | `onto_property_def_index` (entries with `scope_id` = your scope, `is_override`) |
| 4 | Views exist, and the start card is registered | `onto_settings_list` per scope, `onto_startcard_index` |
| 5 | Every action carries your planning scope id and `require_scope_write` | `onto_actiondef_list` |
| 6 | The notification and helper triggers exist | `onto_trigger_index` |
| 7 | Objects per type match the intake (business, site, stations, persons, templates, period, shifts) | `onto_object_index` |
| 8 | One published shift really hangs on its person | `onto_object_graph` on that shift, link `worksShift` |
| 9 | One real end-to-end step as staff: a published shift appears under "My shifts"; a request lands in the inbox | `ontouser_*` views as that account |
| 10 | A staff account clocked in and out on its own shift; the correction carries a reason and an old → new entry | `ontouser_object_show` on the `serviceVisit`, the change log view |
| 11 | The payroll CSV carries one row per person with planned and actual hours | the export, opened and read |
| 12 | The credit balance you report is the one you measured | `onto_credit_balance` |

A status message names its stage — **"stage X of 4 (0–4)"**. "Everything is set up" is not a
status: it names no phase, no number and no check. If you cannot fill the table, you are
not done, and the correct answer is the missing line, not a summary.

## Status

| Field | Content |
|---|---|
| Verified against | **platform state 2026-11-11** (tested by the authors with member rights only; where this skill says "tested build" it means that build) |
| Status | 1.2.3. In 1.2.0: the per-phase Definition of Done, the report shape and three stop rules against premature "done" claims. In 1.2.1 (review feedback): twelve checks (was ten) reaching stage 4 (clock-in, change log, payroll CSV), the start card read via `onto_startcard_index`, the status line "stage X of 4" instead of the misleading "of 5", the report example counting real acceptance steps, the link list extended by `bestehtAus`, `hasfile` and `performs` (with the note that `employedAt`/`qualifiedFor` are link values, not types), and the budget figures moved to the volume price (three scopes 260 instead of 100). In 1.2.2 (second review pass): `definition-of-done.md` carries the same twelve checks and reads the start card via `onto_startcard_index`; `concerns` is documented as any → any with a link value; `prerequisites.md` no longer mixes tier prices with the volume price; the changelog no longer credits 1.2.0 with the twelve checks. In 1.2.3 (third review pass): the step count is now correct and stated once — 44 steps (0.1 … 4.8 including 3.4a–c and 4.4a–b) plus 18 negative tests; README, acceptance file and Definition of Done carry the same numbers; the price list is dated 2026-11-11. All files are written in full: this file, prerequisites, intake, phases 0–4, acceptance scenario, measurement, publication check, glossary, country module DE, definition of done. The seven block views (phases 1 and 3) are confirmed in the browser as manager and as staff. **Before go-live:** run the acceptance scenario in your own workspace — every workspace differs in configuration. Points that depend on your setup are marked "(confirm)". |
| Platform skill state | Links point to the main branch of the platform skill, read on 2026-11-11 (platform skill 1.11.2). If a linked file has moved, look it up by name in the platform skill and report the broken link; do not guess its content. |
| Industry | Restaurants and other shift-based businesses (care, retail, events). Restaurant values are examples. |
| Tool count | **Not stated on purpose.** Measure: `GET https://mcp.telesherpa.com/health` (field `tools`) and `auth_status` for what *your* account sees. |

## Goal

Managers plan and publish shifts; staff see **only their own** shifts, file
requests (absence, day-off wish, shift request, swap, takeover, handover) and clock
in/out themselves; managers get planned vs. actual hours per person and month as a
CSV for the payroll office.

**Charts and reports: offer them, do not promise them.** The platform can show the same numbers
as a bar, line, pie or stacked chart, as a map, and as a downloadable CSV — but **a member
cannot build a report**; that is an admin task, ordered through the service channel. So tell the
manager what is possible and file the request with them; the menu, the wording and the service
request template are in the platform skill: [reports.md](../../telesherpa-ontology-platform/references/features/reports.md).
The four that fit this solution: hours per week planned vs. actual, shifts per person, absences
per month and kind, shifts per station.

## Definition of Done — per phase, checkable

"The workspace is configured" means one sentence, and it has a test: **a person who has
never seen the build can do their daily work without asking anyone.** Everything below is
a precondition for saying that, not a description of it.

| Phase | Minimum artefact | The proof you must quote |
|---|---|---|
| 0 | three scopes with the agreed suffixes, the rights matrix, scope-specific property definitions, the smoke test | `ontouser_scope_index` lists three; the staff test returns **403** on the planning scope; `onto_property_def_index` shows definitions with your scope id |
| 1 | business, site, stations, staff persons, templates, planning period, shifts, published shifts, hours functions, week grid | object counts per type; one shift read back with its `publishedAt` and its `worksShift` link |
| 2 | request and absence forms, the deciding actions, the inbox views | one request created as staff, visible in the inbox, decided once |
| 3 | staff accounts, "My shifts", "Open shifts for me", notifications to affected people only | the staff login sees its own shift and **not** a colleague's |
| 4 | clocking through the scope bridge, staff record with pay, payroll-prep view and CSV | one clock-in object, one CSV row with planned and actual hours |

**The hard rule:** the workspace counts as configured only when
[acceptance-scenario.md](references/acceptance-scenario.md) has run **end to end once** and
its result is quoted, step by step. Until then the status is "stage X of 4".

**"Created" is not "configured".** An object list proves that rows exist. A working
workspace proves that the next person can use it: a published shift shows up in the
staff view, a request arrives in the inbox, a clock-in lands on the right day.

## Out of scope (do not build, do not promise)

- Payroll calculation, DATEV or other payroll-system formats (DATEV is an outlook only;
  the export is a **generic CSV**: `person;month;contractType;hourlyRate;shiftsInMonth;plannedHours;actualHours;miniJobWarning`
  plus optional columns, see phase 4).
- Automatic scheduling / AI planning (Phase 5, later / out of scope — see "Agent planning loop").
- Tip pooling, POS, geofencing, team chat.
- **Building reports and charts yourself.** Reading a report is a member feature; creating one
  needs the admin role. Order it (see "Charts and reports" above) instead of attempting the save
  call — it answers 403.
- **Publishing several shifts in one bulk action** — decided against; publish shift by shift.
- Raising the **row limit** of views — they are paginated (10 rows per page by default,
  200 at most, cards stop at 60). With a period filter you rarely need more.
- Legal advice. Working-time rules appear as checks and warnings, never as a verdict.

## Build order — phases 0–4

Every phase file uses the same frame: *goal · definitions · config snippets ·
checks via MCP · checks in the browser (per role) · acceptance · typical errors*.

| Phase | File | Core |
|---|---|---|
| 0 | [phase0.md](references/phase0.md) | three scopes, rights matrix, object types, scope-specific properties, link types, smoke test |
| 1 | [phase1.md](references/phase1.md) | master data and plan for managers: business, site, stations, staff, templates, periods, shifts, staffing, publishing, hours functions, week grid |
| 2 | [phase2.md](references/phase2.md) | requests (swap, takeover, handover, shift request) and absences incl. day-off wish through the team door, result in planning; forms; request inbox and decisions |
| 3 | [phase3.md](references/phase3.md) | staff accounts, "My shifts" and "Open shifts", day-off wish flow, start card "My shifts" in the team scope, notifications to affected people only, first-publication message |
| 4 | [phase4.md](references/phase4.md) | clock in/out as scope bridge with guard, break as own field, manager correction and change log, protected staff record in planning, payroll-prep view and generic CSV, minijob warning from the country module |

Phase 5 (automatic planning, DATEV, cost fields, availability in pickers) is
**later / out of scope** and not part of this skill ([phase4.md](references/phase4.md) §11).

Before you start: [prerequisites.md](references/prerequisites.md) →
[intake.md](references/intake.md) (ask the business, do not guess) → phase 0.
End-to-end check: [acceptance-scenario.md](references/acceptance-scenario.md).
Paid test runs: [measurement.md](references/measurement.md).

Working conventions for every phase:
- Test objects carry the prefix `TEST-<phase>-` in name and `external_id`.
- Save the current definition (read it, keep the JSON) before you change it.
- **Read back after every write.** A write response describes intent, the read-back describes state.
- Turn e-mail/push off on notification rules until the acceptance of phase 3.

## Core rules (read before phase 0)

Short form. The platform references linked below are authoritative.

1. **Staff have no right on the planning scope** (neither read nor write) and
   **read (no write) on master**. They reach planning objects **only through the
   person link**: a shift linked to their master person by `worksShift`, or an
   absence or request linked to that person by `concerns`, opens for them; every
   other planning object (a colleague's shift, absence or request) stays closed and
   answers as if it did not exist. **One exception:** an open shift that matches the
   person's qualifications is listed through `passt` ("Open shifts for me") and can be
   requested, although it does not hang on the person yet (whether its detail page
   and comments open for staff — confirm, phase 3 P3-13). They work through the **team door** (views and
   actions in the team scope). Team views list what is reachable for the signed-in
   person — "My shifts" uses a **shift** base set with a `person` block via
   `worksShift`, request/absence views bind via `concerns`, "Open shifts for me" uses
   `passt`. The signed-in person is the master person whose `email` equals the login.
   Writing into planning (clock in/out, requests) goes through a **scope bridge** —
   that is the write door, not a scope right. Three consequences:
   - every staff button works on an object that hangs on the person, and buttons on
     own rows carry a guard on exactly that person (rule 11);
   - the person link opens the **whole object**, not a redacted copy: whatever sits on
     a shift, absence or request of that person is visible to them, **including its
     comments** — never put remarks for managers only on those objects, and never
     write one person's request into the comments of a shift that others reach
     (an open shift is later staffed by someone else);
   - team views do not "filter down" a readable planning scope; they list only what
     the person link reaches.

   **E2 split — basic vs protected:** master objects that staff can read hold only
   **basic** data (name, login e-mail, stations/qualifications). What colleagues must
   not see — pay (`hourlyRate`), health-related notes, private contact/address data,
   payroll views, all-staff plans — belongs in the **planning** scope (pay and private
   data on a manager-only **staff record**, [phase4.md](references/phase4.md) §1.2),
   never on staff-readable master persons. The staff record hangs on the person, so
   treat it as readable **by that person** (own data, never a colleague's) and keep
   manager-only remarks off it. Do **not** grant
   planning read "so views work". See [scopes-and-permissions.md](../../telesherpa-ontology-platform/references/features/scopes-and-permissions.md).
2. **Scope bridge:** a staff action writes into planning only via
   `action.result_scope_id = <planning_scope_id>` inside the `action` block, limited to
   the target object and exactly the keys in `action.props`. It is a door for one
   write, not a right.
3. **Rights are fail-closed.** No grant means no access; an empty list means empty.
   There is no shortcut through a higher role — set read, write and manage explicitly.
4. **Delete one id at a time.** Never by name, prefix or pattern. List, pick exact ids,
   delete, read back. Deleting costs 20 credits per object/link/property.
5. **UDIDs always lower case.** Mixed case silently never matches (bridges, form ↔ action links).
6. **Triggers hang on insert** and run asynchronously (1–5 min). Every property a
   notification needs must be set when the object is created; patching later notifies
   nobody. Never resend a write because "nothing happened yet".
7. **Reaching another agent = comment + notification.** `onto_object_addcomment`
   (`parent`, `scope_id`, `text`) alone does not wake anybody; also send
   `ontouser_notification_send` and check `"sent": true`.
8. **Filters are kept in the session, never in the URL.** Company data goes in POST
   bodies, never in query strings.
9. **Every manager view sets `view_config.access.require`** (`"write"`, `"manage"` or a
   scope id). Missing = read is enough; an unknown value = denied. A menu entry that
   is hidden is not a lock.
10. **Every manager action sets `require_scope_write: <planning_scope_id>`** (the
    "management gate"); the button is then invisible to readers.
11. **Staff-only-own-row actions carry a guard** in the live format
    (`type` + `linktype`):
    `"guards": [{"type": "linked_to_user", "linktype": "worksShift", "message": "..."}]`.
    Staff forms that act for a person (absence request) carry the same guard in the
    form definition with `"linktype": "concerns"`. Do not invent another shape; the platform reference
    [scope-bridges.md](../../telesherpa-ontology-platform/references/features/scope-bridges.md)
    is authoritative.
12. **Unlink with `remove: "pair"`**, never `remove: true`.
13. **Time:** stored and returned as **UTC**, with the `_local`/`value_local` sibling in the viewer's zone. **Naive input is read in the viewer's zone** (default `Europe/Berlin`, measured 2026-11-25: `2026-11-10 09:00:00` is stored as `08:00:00` UTC); append `Z` or an offset (`2026-11-10T09:00:00Z`) and it is taken literally. `time` prompts need two digits (`07:30`).
14. **Notify only affected people.** Swap, cancellation and assignment changes reach
    only the persons involved. The only message to everybody concerned is the **first
    publication** (each staffed person, once per shift). No bulk publish; triggers and
    notifications cost no credits ([phase3.md](references/phase3.md) §6).

### Link types of this solution — use these, invent none

The platform has 27 link types, most of them for other industries. This solution uses
exactly the ones below, in this direction. `references/phase0.md` §1.6 is the authoritative
list with all `concerns` link values — if the two ever disagree, phase 0 wins.

| Link | Direction | What it carries |
|---|---|---|
| `worksShift` | **person → shift** | the person the shift belongs to. This is the only path by which staff reach their own shift |
| `concerns` | any → any | absences, requests, qualifications, stations, periods — the **link value** names the role (`concernsPerson`, `station`, `takingOver`, `handingOver`, … — exact list in phase0 §1.6) |
| `derivedFrom` | shift → `shiftTemplate` | traceability: which template produced the shift |
| `bestehtAus` | organisation → building → space | the site/station tree |
| `hasfile` | any → file | qualification documents and attachments |
| `performs` | person → `serviceVisit` | legacy actual-time path — **not used in this skill** (phase 4 uses the scope bridge) |

`employedAt` and `qualifiedFor` are **not link types**: they are link values on
`concerns` (person → building / person → space). Setting them as a type is the classic
mistake here; the full list of link values is in phase0 §1.6.

**No invention.** A link type that is not in `onto_link_index` with matching `types1` and
`types2` for the pair you need does not exist for you, whatever its name suggests —
`assignedTo`, for example, is defined **room → person**, not person → shift. And: a link
you have not read back with `onto_object_graph` does not exist in the report either.

**Names are part of the check.** Object names follow the pattern agreed in the intake
(e.g. `2026-11-15 17:30-23:00 service`). Quote five names in the report and compare them
with the pattern; a deviation is a finding, not a matter of taste.

Platform references (do not duplicate them here):

| Topic | Reference |
|---|---|
| Scopes, rights, three-scope pattern | [scopes-and-permissions.md](../../telesherpa-ontology-platform/references/features/scopes-and-permissions.md) |
| Scope bridges (`result_scope_id`) | [scope-bridges.md](../../telesherpa-ontology-platform/references/features/scope-bridges.md) |
| Tool traps, prices, time, async triggers | [tool-traps.md](../../telesherpa-ontology-platform/references/features/tool-traps.md) |
| Reports, charts, CSV — what to order for the manager | [reports.md](../../telesherpa-ontology-platform/references/features/reports.md) |
| Member-agent rules (i18n, JSON mode, filters, `access.require`, placeholders, deleting) | [member-agent-rules.md](../../telesherpa-ontology-platform/references/features/member-agent-rules.md) |
| Notifications and link events (`link_removed`) | [notifications-and-link-events.md](../../telesherpa-ontology-platform/references/features/notifications-and-link-events.md) |
| Start cards and `blocks` | [start-cards.md](../../telesherpa-ontology-platform/references/features/start-cards.md) |
| Forms | [form-engine.md](../../telesherpa-ontology-platform/references/features/form-engine.md) |
| Block views (person binding, matching, rules, counters, trash) | [view-blocks.md](../../telesherpa-ontology-platform/references/features/view-blocks.md) |
| Triggers and functions | [automation-and-functions.md](../../telesherpa-ontology-platform/references/features/automation-and-functions.md) |
| Managed staff accounts, invite codes | [company-manager.md](../../telesherpa-ontology-platform/references/features/company-manager.md) |

### Confirmed, and what to confirm

- **Block views (confirmed in the browser, 2026-11-06):** the seven views My shifts,
  My week, My requests, Open shifts for me (phase 3) and Rule check, Shift lead today,
  Trash (phase 1) were rebuilt from blocks only and compared row by row with a
  running test workspace, as manager and as staff. Rows, counter values and rule
  warnings matched. The companion view "My absences" uses the same binding — confirm it
  in the browser.
- **One block list shows one object type.** "My requests" with absences, or a trash
  over several types, are two (or more) lists.
- **Placeholders in view blocks:** `{period_start}` and `{period_end}` (first and last
  day of the selected period, dates), `{period_end_dt}` (last day 23:59:59, for
  datetime comparisons), `{now}` (current time) and `{today}`. Write them bare inside
  the `wert` string, e.g. `"wert": "{now}"`; do not add quotes or a time suffix.
- **Views are rebuilt from their blocks on every page load.** After changing a
  definition, hard-reload the page before you judge the result.
- **Night shifts:** hours across midnight are calculated correctly when the end
  carries the next date (confirmed, planned and actual hours). Create actions need an
  `endDate` prompt for that (confirmed, phase 1 §4.3); without it the end lands on the
  shift date. The rule check compares real timestamps (previous end against next start),
  so a shift ending 01:00 counts against a 09:00 start; week views place a night shift
  on its **start day**. Confirm both in your workspace with one test night shift.
- **Credits for triggers and notifications (confirmed):** triggers and notification
  rules consume **no** credits; only the user-triggered writes that
  cause them do.
- **`{now}` in actions:** written into a `datetime` property or a comment it carries the
  platform timestamp and is read back unchanged (UTC). Check it once in phase 1 (P1-8) by
  reading back `publishedAt` and the comment time.

## Stop and escalate

Stop, do not improvise, and report when any of these happens. **Inventing a
workaround is forbidden** — e.g. granting yourself or staff extra rights, moving data
into another scope to "make it visible", hiding data with a view filter instead of a
scope, writing through a different tool because the intended one failed.

| Situation | What you do |
|---|---|
| HTTP **402** | The executing account has no credits. Check `onto_credit_balance` of *that* account (staff accounts pay for their own actions). Stop and ask the operator/human for credits. Do not retry. |
| HTTP **403** / scope write refused | Check rights with `ontouser_scope_index` / `ontouser_team_show`. If the design says the account must not have the right, the fix is a bridge or a gate, not a grant. If unclear: stop and ask. |
| Required object type missing from `ontouser_scope_types` / `onto_type_show` | Stop. File `ontouser_service_request` (template in [prerequisites.md](references/prerequisites.md)). Do not substitute another type silently. |
| A tool reports unknown parameters | Read the allowed keys and fix the call once. If the documented parameter is not accepted, stop and report (the skill is out of date). |
| Smoke test (phase 0) deviates from this skill | Stop before building. Report the deviation with tool, call and response. |
| MCP timeout / connection drop on a write | Read back. Only repeat if the read-back proves nothing was written. |
| 3 consecutive failed attempts at the same step (any error), or spend above the agreed budget | Stop and report (see [measurement.md](references/measurement.md)). |
| The business is not on Europe/Berlin time | Stop before phase 0 and file `ontouser_service_request`; a naive time is read in the **viewer's** zone, which defaults to Europe/Berlin. |
| Anything that would message real people outside a test | Ask the human first. |
| Intake answer missing (stations, manager, contract types, country) | Ask; do not assume restaurant defaults for a real customer. |
| **You are about to report completion or "everything is set up"** | Stop. Run the twelve checks above and quote the values. A summary without numbers, phases or checks is not a status report; it is out of contract. |
| **A link or property you need is missing from the schema** | Do not invent or repurpose one. `onto_link_index` shows `key`, `types1`, `types2`; if the pair is not there, file a service request and stop. |
| **You have built objects but no view, no action and no trigger** | That is not a phase, that is a fragment. Name the phase you are in and what is missing before reporting anything. |

Report format (to the human and, for platform faults, via `ontouser_service_request`
with `category: "bug"`): what you tried (tool + arguments without secrets), what you
expected, what came back (status + error text), what you did not do because of it.

### Report shape — use this, every time

```
Stage X of 4 (0–4).

| Check (from the twelve) | Value read back |
|---|---|
| scopes                | 3 — …_master, …_planning, …_team |
| objects per type      | person 8, shift 12, shiftTemplate 4, space 5, building 1 |
| property definitions  | 14 in …_planning, 6 in …_master |
| views / start card    | 5 views in …_team, 3 in …_planning; start card "My shifts" |
| actions               | 9, all with require_scope_write = …_planning |
| triggers              | 3 |
| acceptance steps      | 24 of 44 passed (0.1 … 4.8 incl. 3.4a–c and 4.4a–b), negative tests 6 of 18 open |

Not done yet: <bullet list, each with the stage it belongs to>
```

Two lines are forbidden in this report: "everything is set up" and "done" — they say
nothing that can be checked. The count of passed acceptance steps is the only honest answer to "are you
finished" — the scenario has **44 steps** (0.1 … 4.8, including the sub-steps 3.4a–c and 4.4a–b)
and **18 negative tests** (N1 … N18). Both counts are in the acceptance file; do not restate
them from memory.

## Agent planning loop (planned)

Not built. The goal is that an agent eventually proposes or creates the
plan. Data the workspace must hold first (Phase 5):
- **Availability** per person (absences with kind `availability`/`dayOffWish` already exist; weekly availability is missing).
- **Demand** per station and time slot (`demand` objects with quantity) and a coverage check (demand vs. staffed shifts).
- **Qualification** per person and station (exists: link `concerns` / `qualifiedFor` person → station).
- **Contract limits** (minijob cap, weekly hours) and **costs** (hourly rate exists on the staff record; cost fields per shift missing).
- Rules (rest time, youth protection) as machine-checkable conditions.
The loop itself (propose → manager approves → publish shift by shift) will be
described when Phase 5 is decided.

## Reference files

- [prerequisites.md](references/prerequisites.md) — account, rights, credits, live price list, missing types
- [intake.md](references/intake.md) — questionnaire for the business
- [phase0.md](references/phase0.md) — scopes, rights, types, properties, smoke test
- [phase1.md](references/phase1.md) — master data, templates, plan, staffing, publishing
- [phase2.md](references/phase2.md) — requests, absences, decisions
- [phase3.md](references/phase3.md) — staff view, start card, notifications
- [phase4.md](references/phase4.md) — clocking, change log, staff record, payroll CSV
- [glossary.md](references/glossary.md) — terms, keys, example labels
- [country-de.md](references/country-de.md) — Germany: minijob, minimum wage, working time, data protection
- [acceptance-scenario.md](references/acceptance-scenario.md) — end-to-end test with expected values
- [definition-of-done.md](references/definition-of-done.md) — the audit before any status report: twelve checks, phase gates, status vocabulary, failure patterns
- [measurement.md](references/measurement.md) — paid test run: budget, stop criteria, log template
- [publication-check.md](references/publication-check.md) — what must never be in this public skill
