---
name: venue-rental-handover
description: Use when an agent must set up clubhouse, community-hall or room rental with key and premises handover on Telesherpa — three scopes (master data, venue, team), buildings as venues, one open serviceOrder per booking with the handover and return dates on that order, views for upcoming handovers / overdue returns / open bookings / defects, start cards in the team scope, forms that record handover and return protocols (photos, signatures of both parties, inventory and key notes) and a form that reports a defect on the venue. Also use when extending or auditing such a workspace.
version: "1.0"
author: Telesherpa
license: MIT
platforms: [linux, macos, windows]
---

# Venue rental with key and premises handover (Telesherpa industry solution)

**Location in the repo:** `industry-solutions/venue-rental-handover/`, next to
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
handover path — form, photos, signature, `form_answer`, protocol linked `ofOrder`,
and a function that writes back to the booking — and the defect path follow
[maintenance-inspections](../maintenance-inspections/SKILL.md). Link to those
files; do not duplicate their recipes here.

Staff work from dated lists of handovers, returns and open bookings. Rental
prices and deposits are stored as fields on the booking; payment stays in the
account the club or municipality already uses.

## Search terms / Also known as

People looking for this workflow often search for: venue rental software,
hall hire software, room hire booking, community hall booking,
village hall booking, clubhouse rental, parish hall booking, facility booking,
key handover, key register, inventory checklist, handover protocol,
return protocol, condition report premises, meter reading handover,
damage report venue, room booking club, Saalvermietung, Raumvermietung Verein,
Vereinsheim vermieten, Gemeindehaus Vermietung, Bürgerhaus Buchung,
Dorfgemeinschaftshaus, Mehrzweckhalle, Belegungsplan, Raumbuchung,
Schlüsselübergabe, Schlüsselverwaltung, Übergabeprotokoll Gemeindehaus,
Rückgabeprotokoll, Inventarliste, Zählerstand, Kaution Vereinsheim,
Hausmeister Übergabe, Raumnutzung Verein, Mietvertrag Gemeindehaus.

Those phrases name the same documented job: a booking, a handover of
the room and the keys signed by both parties, photographs and inventory notes, a return signed by both parties, and
a defect recorded on the venue when one is found.

## Before you claim anything — the checks

**A workspace is not set up because objects exist.** Before you write any progress
or completion report, run these checks and quote the values you read back. A
statement without numbers from a read-back is a claim, not a status.

| # | Check | Query |
|---|---|---|
| 1 | The three scopes exist with the agreed suffixes, and you are manager of all three | `ontouser_scope_index` |
| 2 | Per scope: number of objects, members, managers | `onto_scope_index` (fields `obj_count`, `user_count`, `manager_count`) |
| 3 | The type `serviceOrder` in the venue scope carries `startDate` (date), `dueDate` (date), `orderKind` (`venueBooking` / `handoverProtocol` / `returnProtocol` / `defect`), `hirerName`, `keySet`, `result` (`pass` / `defect`) and `inspectionNote` | `onto_type_show` |
| 4 | Views exist, and the start cards are registered in the team scope and point at team-scope views | `onto_settings_list` / `onto_interface_index` per scope, `onto_startcard_index` |
| 5 | `record_handover` and `record_return` are `form_answer` actions bound to their forms; their functions and triggers are present; `report_defect` is present; actions write to the venue scope (`result_scope_id`) | `onto_actiondef_list`, `show_formdef`, function and trigger index/show |
| 6 | Objects per type match the intake (business, venues, people, bookings) | `onto_object_index` |
| 7 | One open booking really points at its venue, and the handover and return dates sit on that order | `onto_object_graph` on the order (`concerns` with linkvalue `ofAsset`); `onto_object_show` (`startDate`, `dueDate`, `orderKind`, `orderStatus`) |
| 8 | One real end-to-end step as manager: record a handover with a photo, both signatures, inventory and key notes; then a return on the same booking with both signatures; each creates a protocol linked `ofOrder` | the forms in the browser, then a read-back of the booking and of both protocols |
| 9 | One defect reported on a venue appears in the defects view and not in the open-booking lists | the form action, then the two views |
| 10 | The credit balance you report is the one you measured | `onto_credit_balance` |

A status message names the missing line, not a summary. "Everything is set up"
is not a status.

## Status

| Field | Content |
|---|---|
| Basis | Platform capabilities measured in `maintenance-inspections` against **platform schema 2026-11-16** (Europe/Berlin): types and properties, links `concerns` with `ofAsset` and `ofOrder`, formdef widgets `images` and `signature` (a form may have two `signature` fields with distinct keys), `form_answer` actions, row actions with a hidden `udid` column, action conditions with operator `ne`, functions and triggers, views with `{today}` and `{today+14}` or `{today+30}`, and the three-scope pattern. The defect path on a `building` is the measured `report_defect` path. |
| Status | Version 1.0 configuration recipe. This industry workspace is created in the customer's scopes. Treat every check above as open until it is quoted from that workspace. |
| Industry | Clubs, parishes and municipalities that let a clubhouse, community hall, civic hall or meeting room and need a documented key and premises handover. |

## Goal

Managers maintain venues as `building` rows in master data (and, when the
intake already uses the shift-planning site tree, `space` rows under those
buildings — see [object-model.md](references/object-model.md)). Each booking is
one open `serviceOrder` in the venue scope (`orderKind=venueBooking`). The
handover date (`startDate`), the return date (`dueDate`), the hirer name, the
key set and the stored rental and deposit figures live on that order. The order
is linked to its venue with `concerns` and linkvalue `ofAsset`.

Managers work from start cards on the team door: upcoming handovers from
`{today}` through `{today+14}` or `{today+30}`, overdue returns, all open bookings, and open
defects. **Record handover** opens a form on an open booking and saves a
protocol (`orderKind=handoverProtocol`) with photos, inventory and key notes
and signatures of both parties (`handedoverby`, `receivedby`), linked `ofOrder`. **Record return** does the same with
`orderKind=returnProtocol`. **Report defect** on a venue creates a separate
open order (`orderKind=defect`). How those saves are wired is in
[forms-actions.md](references/forms-actions.md).

## Intake (before the first object)

Ask and write down: the company slug; whether `_master` / `_team` already exist;
the venues (buildings, and rooms or halls if any); whether rooms are `space`
rows already used in shift-planning, or names stored on the booking; key sets
in use; whether meter readings are noted at handover; which rental and deposit
figures to store as fields; the list window N for upcoming handovers; who logs
in as manager (chair, caretaker); the label language. Do not invent types or
links. If a required catalogue type is missing, stop and file
`ontouser_service_request`.

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
| scopes                | 3 — …_master, …_venue, …_team |
| objects per type      | person …, building …, serviceOrder … |
| views / start cards   | work lists + team views; start cards on the team door |
| actions               | record_handover, record_return (form_answer), report_defect |
| sample booking        | concerns/ofAsset → venue … ; startDate … ; dueDate … ; orderStatus … |
| last handover         | protocol handoverProtocol ofOrder; photo and both signatures on the protocol |
| last return           | protocol returnProtocol ofOrder; photo and both signatures on the protocol; booking fields quoted after the function ran |
| last defect           | one open defect on the venue; not in the open-booking lists |
```

Two lines are forbidden in this report: "everything is set up" and "done".

## Reference files

- [object-model.md](references/object-model.md) — scopes, types, properties, links
- [forms-actions.md](references/forms-actions.md) — forms, actions, functions, triggers
- [views-roles.md](references/views-roles.md) — lists, start cards, rights
- [country-de.md](references/country-de.md) — Germany: display labels
