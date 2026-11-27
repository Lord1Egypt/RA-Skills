---
name: art-exhibition-transport
description: Use when an agent must set up art and exhibition transport documentation on Telesherpa — three scopes (master data, transport, team), packed items and crates as assets, one open serviceOrder per item as the transport job with the delivery date on that order, views for overdue deliveries / due in a window from {today} to {today+30} / all open jobs, start cards in the team scope, a form that records a collection condition report (photos, notes, signatures of both parties, date) and a form that records a delivery condition report and handover with the same two signatures, each creating a protocol linked to the same job. Also use when extending or auditing such a workspace.
version: "1.0"
author: Telesherpa
license: MIT
platforms: [linux, macos, windows]
---

# Art and exhibition transport — condition and handover reports (Telesherpa industry solution)

**Location in the repo:** `industry-solutions/art-exhibition-transport/`, next to
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
condition-report path — form, photos, signature, `form_answer`, protocol linked
`ofOrder`, and a function that writes back to the open job — follows
[maintenance-inspections](../maintenance-inspections/SKILL.md). Link to those
files; do not duplicate their recipes here.

## Search terms / Also known as

People looking for this workflow often search for: condition report software,
art condition report, fine art logistics software, art handling software,
art transportation software, art shipping software, exhibition transport,
exhibition logistics, fine art shipping, artwork loan, museum loan transport,
crate packing list, packing and crating, chain of custody, handover protocol,
delivery receipt, collection report, transit documentation, art courier,
gallery logistics, registrar condition report, Zustandsprotokoll,
Kunsttransport Software, Messelogistik, Ausstellungstransport, Kunstspedition,
Kunsthandling, Transportkiste, Verpackungsprotokoll, Kunstleihe, Leihverkehr,
Galerielogistik, Übergabeprotokoll Kunst, Transportprotokoll, Zustandsdokumentation.

Those phrases name the same documented job: an item, a tour or delivery date,
photographs of condition at collection and at delivery, and signatures of both parties at each handover.

## Before you claim anything — the checks

**A workspace is not set up because objects exist.** Before you write any progress
or completion report, run these checks and quote the values you read back. A
statement without numbers from a read-back is a claim, not a status.

| # | Check | Query |
|---|---|---|
| 1 | The three scopes exist with the agreed suffixes, and you are manager of all three | `ontouser_scope_index` |
| 2 | Per scope: number of objects, members, managers | `onto_scope_index` (fields `obj_count`, `user_count`, `manager_count`) |
| 3 | The type `serviceOrder` in the transport scope carries `dueDate` (date), `lastDone` (date), `tourCode` (string), `crateCode` (string), `orderKind` (`transportJob` / `collectionReport` / `deliveryReport`), `result` (`pass` / `defect`) and `inspectionNote` | `onto_type_show` |
| 4 | Views exist, and the start cards are registered in the team scope and point at team-scope views | `onto_settings_list` / `onto_interface_index` per scope, `onto_startcard_index` |
| 5 | `record_collection` and `record_delivery` are `form_answer` actions bound to their forms; their functions and insert and update triggers are present; both actions write to the transport scope (`result_scope_id`) | `onto_actiondef_list`, `show_formdef`, function and trigger index/show |
| 6 | Objects per type match the intake (business, sites, people, items, transport jobs) | `onto_object_index` |
| 7 | One open transport job really points at its item, and the delivery date sits on that order | `onto_object_graph` on the order (`concerns` with linkvalue `ofAsset`); `onto_object_show` (`dueDate`, `orderKind`, `orderStatus`, `tourCode`) |
| 8 | One real end-to-end step as manager: record a collection report with a photo, both signatures and a date; then a delivery report on the same job with both signatures; each creates a protocol linked `ofOrder` | the forms in the browser, then a read-back of the job and of both protocols |
| 9 | The credit balance you report is the one you measured | `onto_credit_balance` |

A status message names the missing line, not a summary. "Everything is set up"
is not a status.

## Status

| Field | Content |
|---|---|
| Basis | Platform capabilities measured in `maintenance-inspections` against **platform schema 2026-11-16** (Europe/Berlin): types and properties, links `concerns` with `ofAsset` and `ofOrder`, formdef widgets `images` and `signature` (a form may have two `signature` fields with distinct keys), `form_answer` actions, row actions with a hidden `udid` column, action conditions with operator `ne`, functions and triggers, `date_add` where an interval is used, views with `{today}` and `{today+14}` or `{today+30}`, and the three-scope pattern. |
| Status | Version 1.0 configuration recipe. This industry workspace is created in the customer's scopes. Treat every check above as open until it is quoted from that workspace. |
| Industry | Small art, gallery, exhibition and trade-fair transport teams that record condition at collection and at delivery and a handover signed by both parties. Customs, dispatch planning and invoicing stay in the tools the business already uses. |

## Goal

Managers maintain clients as text fields or as `organisation` / `person` rows
in master data, sites as `building` rows, and packed items and crates as `device`
rows (see [object-model.md](references/object-model.md)). Each item that moves
has one open `serviceOrder` in the transport scope (`orderKind=transportJob`).
The delivery date, the tour code and the crate code live on that order. The order
is linked to its item with `concerns` and linkvalue `ofAsset`.

Managers work from start cards on the team door: overdue deliveries, deliveries
due from `{today}` through `{today+14}` or `{today+30}`, all open jobs, and jobs in progress.
**Record collection** opens a form on an open job and saves a protocol
(`orderKind=collectionReport`) with photos, notes and signatures of both parties (`handedoverby`, `receivedby`), linked
`ofOrder`. **Record delivery** does the same with `orderKind=deliveryReport`
and is the handover at the destination. How those saves update the job is in
[forms-actions.md](references/forms-actions.md).

## Intake (before the first object)

Ask and write down: the company slug; whether `_master` / `_team` already exist;
sites used as collection or delivery addresses; how items and crates are named;
which fields to keep on an item (title, artist, dimensions, declared value as
a stored property); the list window N for upcoming deliveries; who logs in as
manager; the label language. Do not invent types or links. If a required
catalogue type is missing, stop and file `ontouser_service_request`.

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
| scopes                | 3 — …_master, …_transport, …_team |
| objects per type      | person …, building …, device …, serviceOrder … |
| views / start cards   | work lists + team views; start cards on the team door |
| actions               | record_collection, record_delivery (form_answer) |
| sample job            | concerns/ofAsset → item … ; dueDate … ; tourCode … ; orderStatus … |
| last collection       | protocol collectionReport ofOrder; photo and both signatures on the protocol |
| last delivery         | protocol deliveryReport ofOrder; photo and both signatures on the protocol; job fields quoted after the function ran |
```

Two lines are forbidden in this report: "everything is set up" and "done".

## Reference files

- [object-model.md](references/object-model.md) — scopes, types, properties, links
- [forms-actions.md](references/forms-actions.md) — forms, actions, functions, triggers
- [views-roles.md](references/views-roles.md) — lists, start cards, rights
- [country-de.md](references/country-de.md) — Germany: display labels
