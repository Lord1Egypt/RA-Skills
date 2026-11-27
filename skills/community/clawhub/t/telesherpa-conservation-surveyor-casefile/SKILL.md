---
name: conservation-surveyor-casefile
description: Use when an agent must set up a slim conservation or surveyor case file on Telesherpa — three scopes (master data, cases, team), objects as assets, one open serviceOrder per case with the deadline on that order, views for overdue cases / due in a window from {today} to {today+30} / all open cases, start cards in the team scope, and a form that records a condition survey or site visit (findings, photos, signature, optional client confirmation signature, date, optional next due date) and updates the same open case. Also use when extending or auditing such a workspace.
version: "1.0"
author: Telesherpa
license: MIT
platforms: [linux, macos, windows]
---

# Conservation and surveyor case file (Telesherpa industry solution)

**Location in the repo:** `industry-solutions/conservation-surveyor-casefile/`, next to
`telesherpa-ontology-platform/` and `industry-solutions/maintenance-inspections/`.
Load the platform skill first (`telesherpa-ontology-platform/SKILL.md`); this skill
assumes you can register, authenticate and call MCP tools.

**Language:** this file is English because agents read it. Answer the customer in
their language. Keep tool names and JSON keys verbatim. **Option values** are plain
English strings with no translation layer. The placeholders `{today}` and `{today+14}` or `{today+30}`
(the window agreed at intake; store the number, not the letter N) are platform values — do not replace them with a fixed date. Labels shown to the
customer's staff are set in the label language agreed at intake.
**Tool responses and error texts may use the platform language.** Read the returned
allowed keys and error meaning; never translate keys or option values back into a call.

**Reuse, do not copy.** People, sites (`organisation`, `building`) and the
three-scope pattern already live in
[shift-planning](../shift-planning/SKILL.md). If that workspace exists for the same
business, reuse its master data (and, if the intake says so, its team door). The
survey path — form, photos, signature, `form_answer`, protocol linked `ofOrder`,
and a function that writes the next due date back to the same open case — follows
[maintenance-inspections](../maintenance-inspections/SKILL.md). Link to those
files; do not duplicate their recipes here.

This skill is a slim case file: the object, the case, written findings,
photographs, a signature, optional client confirmation and a deadline. Specialist drawing on a photo or plan
stays in the tool the studio already uses for that work.

## Search terms / Also known as

People looking for this workflow often search for: conservation documentation,
restoration documentation, condition survey, condition assessment,
conservation report, treatment documentation, photographic documentation,
photo documentation, object documentation, case file software,
surveyor software, expert report software, heritage documentation,
conservator studio software, condition report conservation,
Restaurierungsdokumentation, Restaurierungsakte, Fallakte, Befunddokumentation,
Zustandsdokumentation, Fotodokumentation, Gutachten Fotodokumentation,
Sachverständigen Software, Sachverständigensoftware, Untersuchungsbericht,
Schadensdokumentation, Denkmalpflege Dokumentation, restauratorische Dokumentation,
öffentlicher Sachverständiger, Gutachtenakte.

Those phrases name the same documented job: a case on an object, a dated
survey with findings and photographs, and a deadline or follow-up date.

## Before you claim anything — the checks

**A workspace is not set up because objects exist.** Before you write any progress
or completion report, run these checks and quote the values you read back. A
statement without numbers from a read-back is a claim, not a status.

| # | Check | Query |
|---|---|---|
| 1 | The three scopes exist with the agreed suffixes, and you are manager of all three | `ontouser_scope_index` |
| 2 | Per scope: number of objects, members, managers | `onto_scope_index` (fields `obj_count`, `user_count`, `manager_count`) |
| 3 | The type `serviceOrder` in the cases scope carries `dueDate` (date), `intervalDays` (int), `lastDone` (date), `caseKind` (`conservation` / `survey`), `orderKind` (`caseFile` / `surveyProtocol`), `result` (`pass` / `defect`) and `inspectionNote` | `onto_type_show` |
| 4 | Views exist, and the start cards are registered in the team scope and point at team-scope views | `onto_settings_list` / `onto_interface_index` per scope, `onto_startcard_index` |
| 5 | `record_survey` is a `form_answer` action bound to its form; `apply_survey` and its insert and update triggers are present; the action writes to the cases scope (`result_scope_id`) | `onto_actiondef_list`, `show_formdef`, function and trigger index/show |
| 6 | Objects per type match the intake (business, sites, people, objects, cases) | `onto_object_index` |
| 7 | One open case really points at its object, and the due date sits on that order | `onto_object_graph` on the order (`concerns` with linkvalue `ofAsset`); `onto_object_show` (`dueDate`, `caseKind`, `orderKind`, `orderStatus`) |
| 8 | One real end-to-end step as manager: record a survey with findings, a photo, a signature, optional client confirmation and a date; the same case stays `open` and its next due date is either the date typed or, if that field was left empty and `intervalDays` is set, the survey date plus the interval | the form in the browser, then a read-back of the case and of the protocol (`orderKind=surveyProtocol`, `concerns` / `ofOrder`) |
| 9 | The credit balance you report is the one you measured | `onto_credit_balance` |

A status message names the missing line, not a summary. "Everything is set up"
is not a status.

## Status

| Field | Content |
|---|---|
| Basis | Platform capabilities measured in `maintenance-inspections` against **platform schema 2026-11-16** (Europe/Berlin): types and properties, links `concerns` with `ofAsset` and `ofOrder`, formdef widgets `images` and `signature` (a form may have two `signature` fields with distinct keys), `form_answer` actions, row actions with a hidden `udid` column, action conditions with operator `ne`, functions and triggers with `date_add` for a next due date, views with `{today}` and `{today+14}` or `{today+30}`, and the three-scope pattern. |
| Status | Version 1.0 configuration recipe. This industry workspace is created in the customer's scopes. Treat every check above as open until it is quoted from that workspace. |
| Industry | Conservators, restorers and surveyors (including publicly appointed experts) who keep a slim case file with photographic documentation and deadlines. |

## Goal

Managers maintain clients as text fields or as `organisation` / `person` rows
in master data, sites as `building` rows, and the objects under study as
`device` or `building` rows — the intake names which (see
[object-model.md](references/object-model.md)). Each case is one open
`serviceOrder` in the cases scope (`orderKind=caseFile`). The due date, the
optional interval and the case kind live on that order. The order is linked to
its object with `concerns` and linkvalue `ofAsset`.

Managers work from start cards on the team door: overdue cases, cases due from
`{today}` through `{today+14}` or `{today+30}`, and all open cases. **Record survey** opens a
form on an open or in-progress case. Saving it creates a protocol
(`orderKind=surveyProtocol`) linked `ofOrder`, stores the findings, photos, the surveyor's signature and, when used, the
client confirmation on that protocol, and writes `result`, `lastDone` and the next
`dueDate` back to the case. If the next due date is left empty and
`intervalDays` is set, it becomes the survey date plus `intervalDays`; if a
date is entered, that date is used. The case stays open, so the same row
returns to the lists when it is due again. How that save is wired is in
[forms-actions.md](references/forms-actions.md).

## Intake (before the first object)

Ask and write down: the company slug; whether `_master` / `_team` already exist;
whether cases concern movable objects (`device`), buildings, or both; client and
object fields to keep; case kinds in use (conservation, expert survey, or both);
whether follow-up intervals are used, and the interval the business already
works with; the list window N; who logs in as manager; the label language. Do
not invent types or links. If a required catalogue type is missing, stop and
file `ontouser_service_request`.

## Stop rules

| Condition | Action |
|---|---|
| 3 consecutive failed attempts at the same step | Stop and report: what you tried (tool + arguments without secrets), what you expected, what came back, what you did not do because of it. |
| A required type or a `concerns` pair is missing | Stop and file `ontouser_service_request`. Do not substitute a neighbouring type. Do not invent a link or a linkvalue. |
| The business is not on Europe/Berlin time | Stop and file `ontouser_service_request`. |
| Anything that would message real people | Ask the human first. |
| Intake answer missing | Ask; do not assume defaults for a real customer. |
| **You are about to report completion** | Stop. Run the checks above and quote the values. |

### Report shape — use this, every time

```
| Check | Value read back |
|---|---|
| scopes                | 3 — …_master, …_cases, …_team |
| objects per type      | person …, building …, device …, serviceOrder … |
| views / start cards   | work lists + team views; start cards on the team door |
| actions               | record_survey (form_answer, case stays open), apply_survey |
| sample case           | concerns/ofAsset → object … ; dueDate … ; caseKind … ; orderStatus open |
| last survey           | result / lastDone / dueDate quoted (typed or computed); protocol ofOrder; signature and, when used, client confirmation on the protocol |
```

Two lines are forbidden in this report: "everything is set up" and "done".

## Reference files

- [object-model.md](references/object-model.md) — scopes, types, properties, links
- [forms-actions.md](references/forms-actions.md) — form, action, function, triggers
- [views-roles.md](references/views-roles.md) — lists, start cards, rights
- [country-de.md](references/country-de.md) — Germany: display labels
