# Phase 1 — basic planning: shifts, demand, staffing, publishing, week plan

**Goal:** a manager can build a week of shifts (from templates or as open shifts),
staff them (with qualified people only when staffed through `sp_shift_staff`; the
template picker is not filtered, see §4.3), publish them **shift by shift**, cancel or
release them, and see the week as a list and as a person × day grid. Planned hours
compute automatically. Staff do nothing yet (their door is phase 2/3).

**Input:** phase 0 passed (S1–S11), answered [intake](intake.md) questions 2–5, 7, 10,
12, 19, 20. Staff rights stay as in phase 0 (master **R**, planning **no membership**,
team **RW**).

**Budget (pay-per-use):** the build itself is mostly definition calls (actions, views,
triggers, functions), which have no own price key (see
[prerequisites](prerequisites.md) §4). Business data: about 10 credits per object
(`create_object`), 5 per link, 20 per action run. A test week of 25 shifts staffed and
published by action costs roughly 25 × (20 + 20) = 1,000 credits plus reads (confirm in the first paid run; log what is booked).

Placeholders used below (in addition to phase 0): `<business_udid>`, `<site_udid>`,
`<station_udid_kitchen>` (one per station), `<template_udid_kitchen_early>` (one per
template), `<period_udid>`, `<shift_udid>`, `<person_udid>`, `<demand_udid>`,
`<space_type_id>`, `<person_type_id>`, `<serviceOrder_type_id>` (from `onto_type_show`
→ `type.id`).

**Vocabulary of view definitions.** Block fields of views are platform keywords and
stay exactly as written, even where they are German words: `from`, `type`, `status`
(`active`, `deleted`, `any`), `columns`, `prop`, `system`, `link`, `richtung`
(`vorwaerts` / `rueckwaerts`), `linkvalue`, `werte`, `format` (`text`, `datum`,
`zeit`, `jahr`, `wochentag_datum`, `wochentag_datum_zeit`, `kalenderwoche`,
`zeitspanne`, `zahl`, `waehrung`, `monat`, `warnung`), `bis`, `hidden`, `wo` (`prop`,
`op`, `wert`; `op` `leer` / `nicht_leer` without `wert`), `nur`, `nur_mit`,
`linktyp`, `bruecke`, `zeitfeld`, `trenner`, `zeitraum` (`von`, `bis`), `param`
(e.g. `woche`, `tag`), `span`, `basis` (`woche`, `heute`, `monat`), `days`,
`person`, `ohne_link`, `passt` (`mein_value`, `objekt_value`), `regeln` (`feld`,
`art: pause`), `personenregeln` (`art`: `u18`, `tagessumme`, `ruhezeit`; `datum`,
`zeit_ab`, `zeit_feld`), `nur_treffer`, `counters` (`zaehler`, `filter`, `scopes`),
`row_actions`. Only **your** keys, labels and option values are English.
Placeholders in `wert`: `{period_start}`, `{period_end}`, `{period_end_dt}`,
`{today}`, `{now}`, written bare.

**Views are built from blocks.** Every view and subform in this skill is built from
blocks (base set, filters, columns, placeholders). Matching, rule checks, counters and deleted lists use the blocks
in [view-blocks.md](../../../telesherpa-ontology-platform/references/features/view-blocks.md).
Those block views are confirmed in the browser (§6.4).

**Platform references** (read them; this file does not repeat them):
[member-agent-rules.md](../../../telesherpa-ontology-platform/references/features/member-agent-rules.md) (placeholders, `access.require`, deleting) ·
[tool-traps.md](../../../telesherpa-ontology-platform/references/features/tool-traps.md) (time, async triggers, prices) ·
[automation-and-functions.md](../../../telesherpa-ontology-platform/references/features/automation-and-functions.md) (functions, triggers) ·
[form-engine.md](../../../telesherpa-ontology-platform/references/features/form-engine.md) (forms) ·
[scopes-and-permissions.md](../../../telesherpa-ontology-platform/references/features/scopes-and-permissions.md) (three-scope pattern) ·
[notifications-and-link-events.md](../../../telesherpa-ontology-platform/references/features/notifications-and-link-events.md) (phase-3 rules, `link_removed`).

---

## 1. Objects, properties, options

All option values are the **scope-own English values** created in phase 0 (§1.4). The
shift type keys below are platform keys; options are overridden in the planning scope.

### 1.1 Objects of this phase

| Object | Type | Scope | Created by | Name pattern (intake 20) |
|---|---|---|---|---|
| business | `organisation` | master | `onto_object_create` (once) | legal short name |
| site | `building` | master | `sp_site_create` on the business | site name |
| station | `space` | master | `sp_station_create` on the site | `Kitchen`, `Service`, … |
| staff member | `person` | master | `sp_staff_create` on the site | `{firstName} {lastName}` |
| shift template | `shiftTemplate` | master | `sp_template_create` on the station | `Template {templateName}` |
| plan period | `serviceOrder`, `task = planPeriod` | planning | `sp_period_create` on the site | `Plan {from} – {to}` |
| shift | `shift` | planning | `sp_shift_from_template`, `sp_open_shift_create`, week generator | `Shift {date} {start}-{end}` / `Open shift {date} {start}-{end}` |
| demand (optional) | `demand` | planning | `sp_demand_report` (form) | `Demand {now}` |
| manager note | `serviceOrder`, `task = planNote` | planning | triggers | `Note: …` |

### 1.2 Properties used (planning scope unless stated)

| Type | Key | value_type | English values / default | Set by |
|---|---|---|---|---|
| shift | `shiftStart`, `shiftEnd` | datetime | | create actions, generator |
| shift | `breakMinutes` | int | default `0` | create actions |
| shift | `plannedHours` | float | | function `sp_planned_hours` |
| shift | `shiftKind` | options | `early`, `late`, `split`, `night` | create actions |
| shift | `station` | options | from intake 3, e.g. `kitchen`, `service`, `bar`, `dishwashing`, `shiftLead` | generator; create actions (see 4.3). Views show and filter this option; qualification matching uses the `station` **link** — set both (phase 0 §1.6) |
| shift | `shiftStatus` | options | `open` (default), `planned`, `published`, `swapped`, `cancelled` | actions |
| shift | `publishedAt` | datetime | | `sp_shift_publish` |
| shift | `onCall` | options | `yes`, `no` | create actions (`no`) |
| shift | `description` | string | `created by {current_user_email}` | create actions |
| shiftTemplate (master) | `templateName`, `startTime`, `endTime` (`HH:MM`), `breakMinutes`, `weekdays` (`1`=Mon … `7`=Sun, e.g. `2,3,4,5,6`), `station`, `validFrom` (date) | | station = same English set as shift | `sp_template_create` |
| space (master) | `description`, `capacity` (= minimum staffing) | | | `sp_station_create` |
| person (master, **basic only**) | `firstName`, `lastName`, `email`, `birthYear` (stored as `YYYY-01-01`) | | | `sp_staff_create` |
| serviceOrder | `task` | string | `planPeriod` or `planNote` | create actions, triggers |
| serviceOrder | `orderStatus` | options | `open` (draft), `inProgress` (published), `done` (closed) | period actions |
| serviceOrder | `priority` | options | `low`, `medium`, `high` | `medium` on periods |
| serviceOrder | `startedAt`, `completedAt` | datetime | | period / note actions |
| demand | `demandKind` | options | `staff`, `material`, `service`, `capacity` | form |
| demand | `demandStart`, `demandEnd` | datetime | | form |
| demand | `demandQuantity` | float | | form |
| demand | `demandUnit` | options | `persons`, `hours`, `pieces`, `units` | form |
| demand | `demandStatus` | options | `open` (default), `planned`, `covered`, `dropped` | form, `sp_demand_status` |

**New scope-specific properties of this phase** (create with `onto_property_def_create`
and `scope_id = <planning_scope_id>`, `type_ids = [<serviceOrder_type_id>]`), needed only
for the week generator (4.7):

| Key | value_type | Label (example) | Purpose |
|---|---|---|---|
| `weekRequest` | string | Week requested | written by `sp_week_request`, blocks a second request |
| `planDay1` … `planDay7` | string (`YYYY-MM-DD`) | Plan day Mon … Sun | written by the agent, fires the day trigger |
| `generatedDay1` … `generatedDay7` | string | Generated day Mon … Sun | set by the day trigger, blocks a second run |

The tested build used these keys without explicit definitions (confirm whether
undeclared keys are enough; declaring them is the safe choice).

**Protected data (E2).** `sp_staff_create` writes only basic fields to the master
person. Private phone, address, `hourlyRate` and `contractType` are **not** written
here; they belong to the manager-only planning side (phase 4). Do not write
`phone` on the master person. Decided in
[phase4.md](phase4.md) §1.2: a manager-only **staff record** in planning, linked
`concerns` / `staffRecordOf` to the master person.

## 2. Links

Platform link types from phase 0 §1.6; `concerns` link values are the exact English
strings below (case-sensitive).

| From → To | Link type | `linkvalue` | Created by |
|---|---|---|---|
| business → site | `bestehtAus` | – | `sp_site_create` |
| site → station | `bestehtAus` | – | `sp_station_create` |
| person → site | `concerns` | `employedAt` | `sp_staff_create` |
| person → station | `concerns` | `qualifiedFor` | `sp_staff_create`, `sp_qualify_for_station` |
| shiftTemplate → station | `concerns` | `station` | `sp_template_create` |
| plan period → site | `concerns` | `takesPlaceAt` | `sp_period_create` |
| shift → shiftTemplate | `derivedFrom` | – | `sp_shift_from_template`, generator |
| person → shift | `worksShift` | – | `sp_shift_from_template`, `sp_shift_staff` |
| shift → plan period | `concerns` | `periodShift` | shift create actions, generator |
| shift → site | `concerns` | `takesPlaceAt` | shift create actions, generator |
| shift → station | `concerns` | `station` | shift create actions, generator |
| shift → demand | `concerns` | `coversDemand` | `sp_demand_cover` |
| manager note → object | `concerns` | `followUpOf` | triggers |

`employedAt` and `coversDemand` are new in this phase (phase 0 lists the others). English
values are the convention of this skill.

## 3. Forms

| Form | Answer type | Lives in | Opened by | Fields (key · widget · required) |
|---|---|---|---|---|
| `sp_demand_report` (optional) | `demand` | planning | action `sp_demand_report` on a station | `demandKind` select* (`staff`, `material`, `service`, `capacity`) · `demandStart` datepicker datetime* · `demandEnd` datepicker datetime* · `demandQuantity` float* · `demandUnit` select* (`persons`, `hours`, `pieces`, `units`) · `demandStatus` select* (only `open`) |

Create with `onto_formdef_create` (scope planning), then `onto_formdef_save` with the
full definition (see recipe). Saving a form definition needs a form-writer right
(confirm for your account). Note: actions of type `form_answer` ignore `condition`;
put restrictions into the gate instead.

## 4. Actions

Every action is saved with `onto_actiondef_save` (`key`, `label`, `body` as a JSON
**string**). Common rules:
- `body.scopes` = scopes where the button appears; `roles: ["member"]`.
- **Management gate** on every manager action: `require_scope_write` inside `action`
  — `<master_scope_id>` for master-data writes, `<planning_scope_id>` for planning
  writes. Staff can read master, so an ungated master action would show "Create staff
  member" to staff.
- Creating into planning from a master object needs `action.result_scope_id =
  <planning_scope_id>`.
- `condition.props` ops: `eq`, `ne`, `in`, `empty`, `notempty`; always give a `message`.
- `prompts`: `type` one of `text`, `int`, `float`, `date`, `time`, `datetime`, `select`,
  `switch`; object pickers are `text` with `object_types`. Always `persist: false`.
  `time` needs two digits (`07:30`).
- `{<prompt>_name}` (e.g. `{staff_name}`) resolves in `effects` only, not in `name` or
  `props`.
- An optional prompt that stays empty skips a comment effect — give it a `default`.

### 4.1 Overview

| Key | Label (example) | On type | Scopes | Gate | Effect |
|---|---|---|---|---|---|
| `sp_site_create` | Create site | organisation | master | master | create building, `bestehtAus` from business |
| `sp_station_create` | Create station | building | master | master | create space, `bestehtAus` from site |
| `sp_staff_create` | Create staff member | building | master | master | create person (basic), `employedAt`, `qualifiedFor` |
| `sp_qualify_for_station` | Qualified for station | person | master | master | add `qualifiedFor` link(s) |
| `sp_revoke_qualification` | Revoke qualification | person | master | master | remove link, `remove: "pair"` |
| `sp_template_create` | Create shift template | space | master | master | create shiftTemplate, link `station` |
| `sp_period_create` | Create plan period | building | master | planning | create period in planning |
| `sp_week_request` | Request week from templates | serviceOrder | planning | planning | write `weekRequest` + comment |
| `sp_shift_from_template` | Shift from template | shiftTemplate | master | planning | create staffed shift (`planned`) in planning |
| `sp_open_shift_create` | Create open shift | building | master | planning | create `open` shift in planning |
| `sp_shift_staff` | Staff shift | shift | planning | planning | `worksShift` from a **qualified** person, `planned` |
| `sp_shift_publish` | Publish shift | shift | planning | planning | `published`, `publishedAt = {now}` |
| `sp_shift_cancel` | Cancel shift | shift | planning | planning | `cancelled` + comment |
| `sp_shift_release` | Reopen shift (drop-out) | shift | planning | planning | remove `worksShift` pair, `open` |
| `sp_period_publish` | Mark plan period published | serviceOrder | planning | planning | `orderStatus = inProgress` (does **not** publish shifts) |
| `sp_period_close` | Close plan period | serviceOrder | planning | planning | `done`, `completedAt` |
| `sp_period_reactivate` | Reactivate plan period | serviceOrder | planning | planning | object status back to `active` |
| `sp_note_done` | Note done | serviceOrder | planning | planning | `done` + comment |
| `sp_demand_report` | Report demand | space | master | planning | form answer → demand |
| `sp_demand_status` | Set demand status | demand | planning | planning | `demandStatus` |
| `sp_demand_cover` / `sp_demand_uncover` | Covers demand / remove | shift | planning | planning | link `coversDemand` / remove pair |
| `sp_restore` | Restore | serviceOrder, shift, absence, shiftTemplate, demand | planning | planning | object status `active` |
| `sp_delete_for_good` | Delete for good | same | planning | planning | `purge` |

**No bulk publish.** There is deliberately no action that publishes all shifts of a
period. `sp_period_publish` only marks the period; each shift is published with
`sp_shift_publish`. The first message to all staff is phase 3.

### 4.2 Master data (pattern: create at parent)

```json
{"key": "sp_site_create", "label": "Create site", "body": {
  "object_types": ["organisation"], "scopes": [<master_scope_id>], "roles": ["member"],
  "prompts": [
    {"key": "siteName", "label": "Site name", "type": "text", "required": true, "persist": false},
    {"key": "street", "label": "Street", "type": "text", "required": false, "persist": false},
    {"key": "postalCode", "label": "Postal code", "type": "text", "required": false, "persist": false},
    {"key": "city", "label": "City", "type": "text", "required": false, "persist": false},
    {"key": "notes", "label": "Opening hours / notes", "type": "text", "required": false, "persist": false}],
  "action": {"type": "create", "object_type": "building", "name": "{siteName}", "status": "active",
    "props": {"street": "{street}", "postalCode": "{postalCode}", "city": "{city}", "description": "{notes}"},
    "links": [{"type": "bestehtAus", "from": "{object_udid}"}],
    "require_scope_write": <master_scope_id>}}}
```

`sp_station_create` (on `building`): prompts `stationName` text*, `minStaff` int*,
`notes` text; creates `space` named `{stationName}` with `description = {notes}`,
`capacity = {minStaff}`; link `{"type": "bestehtAus", "from": "{object_udid}"}`; gate master.

```json
{"key": "sp_staff_create", "label": "Create staff member", "body": {
  "object_types": ["building"], "scopes": [<master_scope_id>], "roles": ["member"],
  "prompts": [
    {"key": "firstName", "label": "First name", "type": "text", "required": true, "persist": false},
    {"key": "lastName", "label": "Last name", "type": "text", "required": true, "persist": false},
    {"key": "email", "label": "Login e-mail", "type": "text", "required": false, "persist": false},
    {"key": "birthYear", "label": "Year of birth (YYYY, youth protection)", "type": "int", "required": true, "persist": false},
    {"key": "station", "label": "Qualified for station", "type": "text", "object_types": ["space"], "required": true, "persist": false}],
  "action": {"type": "create", "object_type": "person", "name": "{firstName} {lastName}", "status": "active",
    "props": {"firstName": "{firstName}", "lastName": "{lastName}", "email": "{email}", "birthYear": "{birthYear}-01-01"},
    "links": [
      {"type": "concerns", "to": "{object_udid}", "linkvalue": "employedAt"},
      {"type": "concerns", "to": "{station}", "linkvalue": "qualifiedFor"}],
    "require_scope_write": <master_scope_id>}}}
```

- `email` is optional in the dialog but **required in practice**: it binds the login
  (phase 3). Ask for it in intake 10.
- `birthYear` (and the login e-mail) are readable by colleagues — intake 13a.
  `birthYear`: make it optional if intake 10 or 13a says
  youth protection does not matter (confirm: `int` prompt with `required: false` and
  an empty value then writes `-01-01`; test before relying on it).

```json
{"key": "sp_qualify_for_station", "label": "Qualified for station", "body": {
  "object_types": ["person"], "scopes": [<master_scope_id>], "roles": ["member"],
  "prompts": [{"key": "station", "label": "Station", "type": "text", "object_types": ["space"], "required": true, "persist": false, "multiple": true}],
  "action": {"type": "update", "props": {},
    "links": [{"type": "concerns", "from": "{object_udid}", "to": "{station}", "linkvalue": "qualifiedFor",
               "require": "absent", "text": "Already qualified for this station"}],
    "require_scope_write": <master_scope_id>}}}
```

`sp_revoke_qualification`: same frame, single `station` picker, link
`{"type": "concerns", "from": "{object_udid}", "to": "{station}", "remove": "pair"}`.
Removing the pair without naming the link value works (confirm whether
adding `"linkvalue": "qualifiedFor"` is accepted with `remove: "pair"`).

`sp_template_create` (on `space`): prompts `templateName` text*, `start` time*, `end`
time*, `break` int*, `weekdays` text* (`1`=Mon … `7`=Sun), `station` select* with the
English station values, `validFrom` date*; creates `shiftTemplate` named
`Template {templateName}` with `templateName`, `startTime`, `endTime`,
`breakMinutes`, `weekdays`, `station`, `validFrom`; link
`{"type": "concerns", "to": "{object_udid}", "linkvalue": "station"}`; gate master.

### 4.3 Plan period and shifts

```json
{"key": "sp_period_create", "label": "Create plan period", "body": {
  "object_types": ["building"], "scopes": [<master_scope_id>], "roles": ["member"],
  "prompts": [
    {"key": "from", "label": "Period from (YYYY-MM-DD)", "type": "date", "required": true, "persist": false},
    {"key": "to", "label": "Period to (YYYY-MM-DD)", "type": "date", "required": true, "persist": false}],
  "action": {"type": "create", "object_type": "serviceOrder", "name": "Plan {from} – {to}", "status": "active",
    "props": {"task": "planPeriod", "orderStatus": "open", "priority": "medium",
              "description": "Plan period {from} – {to}. Status: draft. Created by {current_user_email}."},
    "links": [{"type": "concerns", "to": "{object_udid}", "linkvalue": "takesPlaceAt"}],
    "result_scope_id": <planning_scope_id>,
    "external_id": "SP-{object_slug}-{from}-{random:6}",
    "require_scope_write": <planning_scope_id>}}}
```

The `external_id` makes each period identifiable (site, start date, random suffix).
It does **not** prevent a second period for the same site and start — the random part
differs every time. Before `sp_period_create`, list the periods of the site
(`onto_object_index`, type `serviceOrder`, `task = planPeriod`) and do not create a
duplicate.

```json
{"key": "sp_shift_from_template", "label": "Shift from template", "body": {
  "object_types": ["shiftTemplate"], "scopes": [<master_scope_id>], "roles": ["member"],
  "prompts": [
    {"key": "date", "label": "Shift date (YYYY-MM-DD)", "type": "date", "required": true, "persist": false},
    {"key": "start", "label": "Start HH:MM (as template)", "type": "time", "required": true, "persist": false},
    {"key": "end", "label": "End HH:MM (as template)", "type": "time", "required": true, "persist": false},
    {"key": "break", "label": "Break minutes (as template)", "type": "int", "required": true, "persist": false},
    {"key": "kind", "label": "Shift kind", "type": "select", "required": true, "persist": false, "options": ["early", "late", "split", "night"]},
    {"key": "stationValue", "label": "Station (field)", "type": "select", "required": true, "persist": false, "options": ["kitchen", "service", "bar", "dishwashing", "shiftLead"]},
    {"key": "staff", "label": "Staff member", "type": "text", "object_types": ["person"], "required": true, "persist": false},
    {"key": "period", "label": "Plan period", "type": "text", "object_types": ["serviceOrder"], "required": true, "persist": false},
    {"key": "site", "label": "Site", "type": "text", "object_types": ["building"], "required": true, "persist": false},
    {"key": "stationObj", "label": "Station", "type": "text", "object_types": ["space"], "required": true, "persist": false}],
  "action": {"type": "create", "object_type": "shift", "name": "Shift {date} {start}-{end}", "status": "active",
    "props": {"shiftStart": "{date} {start}", "shiftEnd": "{date} {end}", "breakMinutes": "{break}",
              "shiftKind": "{kind}", "station": "{stationValue}", "shiftStatus": "planned", "onCall": "no",
              "description": "created by {current_user_email}"},
    "links": [
      {"type": "derivedFrom", "to": "{object_udid}"},
      {"type": "worksShift", "from": "{staff}"},
      {"type": "concerns", "to": "{period}", "linkvalue": "periodShift"},
      {"type": "concerns", "to": "{site}", "linkvalue": "takesPlaceAt"},
      {"type": "concerns", "to": "{stationObj}", "linkvalue": "station"}],
    "result_scope_id": <planning_scope_id>,
    "require_scope_write": <planning_scope_id>}}}
```

Notes:
- Start, end and break are typed again; the action does not read them from the
  template (confirm whether prompt defaults can read template fields).
- `stationValue` sets the `station` option that the views show and filter on;
  `stationObj` sets the `station` link that the staffing picker and "Open shifts for
  me" match on. Always set both to the same station (phase 0 §1.6). The reference
  build did not set the option in this action (only the generator did), so its views
  showed an empty station for such shifts.
- The staff picker here is **not** limited to qualified people. Prefer
  `sp_open_shift_create` + `sp_shift_staff` when qualification matters, or add the
  `options_filter` of 4.4 (worth confirming on a template target).
- Shifts over midnight: `{date} {end}` is on the same day. The hour calculation
  itself handles midnight once `shiftEnd` carries the next date (confirmed: 18:00–01:00
  with a 30-minute break gives 6.5 planned hours; phase 4 §5 for actual hours). What
  is missing is the end date in the create actions: add a second prompt
  `{"key": "endDate", "label": "End date (next day for a night shift)", "type": "date", "required": true, "persist": false}`
  and set `shiftEnd = {endDate} {end}` (confirmed: start D 18:00, end D+1 01:00,
  break 30 → end stored on D+1, 6.5 planned hours). For a day shift the end date
  equals the shift date. Apply the same to `sp_open_shift_create`. The weekly
  generator still creates no shifts over midnight. Confirm in the browser:
  the week views list the shift on its start day, and the rule check (`shortRest`,
  `dailyHours`) treats it as intended (§11 open point 2).

`sp_open_shift_create` (on `building`, scopes master): prompts `date`, `start`, `end`,
`break`, `kind`, `stationValue`, `period`, `stationObj` as above (no staff, no site —
the site is the object); name `Open shift {date} {start}-{end}`; props as above with
`shiftStatus: "open"`; links `takesPlaceAt` → `{object_udid}`, `periodShift` →
`{period}`, `station` → `{stationObj}`; `result_scope_id` and gate planning.

### 4.4 Staffing, publishing, cancelling, releasing

```json
{"key": "sp_shift_staff", "label": "Staff shift", "body": {
  "object_types": ["shift"], "scopes": [<planning_scope_id>], "roles": ["member"],
  "condition": {"props": [{"key": "shiftStatus", "op": "eq", "value": "open"}], "message": "Only open shifts can be staffed"},
  "prompts": [{"key": "staff", "label": "Staff member", "type": "text", "object_types": ["person"], "required": true, "persist": false,
    "options_filter": {"link_to": "{linked:concerns:space:station}", "linktype": "concerns", "linkvalue": "qualifiedFor", "direction": "from", "min": 1}}],
  "action": {"type": "update", "props": {"shiftStatus": "planned"},
    "links": [{"type": "worksShift", "from": "{staff}", "to": "{object_udid}", "require": "absent",
               "text": "This person is already on this shift"}],
    "effects": [{"type": "comment", "text": "Staffed {now} by {user_email}: {staff_name}"}],
    "require_scope_write": <planning_scope_id>}}}
```

`options_filter` limits the picker to persons that have a `concerns`/`qualifiedFor`
link (`direction: "from"` the person) to the station linked to this shift
(`{linked:concerns:space:station}`). A shift without a station link shows an empty
picker.

```json
{"key": "sp_shift_publish", "label": "Publish shift", "body": {
  "object_types": ["shift"], "scopes": [<planning_scope_id>], "roles": ["member"],
  "condition": {"props": [{"key": "shiftStatus", "op": "in", "value": ["planned", "swapped"]}],
                "message": "Only planned or swapped shifts can be published"},
  "action": {"type": "update", "props": {"shiftStatus": "published", "publishedAt": "{now}"},
    "require_scope_write": <planning_scope_id>}}}
```

```json
{"key": "sp_shift_cancel", "label": "Cancel shift", "body": {
  "object_types": ["shift"], "scopes": [<planning_scope_id>], "roles": ["member"],
  "condition": {"props": [{"key": "shiftStatus", "op": "ne", "value": "cancelled"}], "message": "Shift is already cancelled"},
  "action": {"type": "update", "props": {"shiftStatus": "cancelled"},
    "effects": [{"type": "comment", "text": "Shift cancelled {now} by {user_email}"}],
    "require_scope_write": <planning_scope_id>}}}
```

A cancelled shift stays visible (marked) in all manager views; it is not deleted.
The `worksShift` link stays, so the affected person can be notified (phase 3).

```json
{"key": "sp_shift_release", "label": "Reopen shift (drop-out)", "body": {
  "object_types": ["shift"], "scopes": [<planning_scope_id>], "roles": ["member"],
  "condition": {"props": [{"key": "shiftStatus", "op": "in", "value": ["planned", "published", "swapped"]}], "message": "Shift is not staffed"},
  "prompts": [{"key": "staff", "label": "Person dropping out (removed from the shift)", "type": "text", "object_types": ["person"], "required": true, "persist": false}],
  "action": {"type": "update", "props": {"shiftStatus": "open"},
    "links": [{"type": "worksShift", "remove": "pair", "from": "{staff}", "to": "{object_udid}"}],
    "require_scope_write": <planning_scope_id>}}}
```

Always `remove: "pair"` — never `remove: true` (which would drop every `worksShift`
link of the shift).

### 4.5 Period actions and notes

| Key | Condition (`props`) | `action` |
|---|---|---|
| `sp_period_publish` | `orderStatus eq open`, `task eq planPeriod` — "Only draft periods can be marked published" | `{"type": "update", "props": {"orderStatus": "inProgress", "startedAt": "{now}"}, "require_scope_write": <planning_scope_id>}` |
| `sp_period_close` | `orderStatus eq inProgress`, `task eq planPeriod` | `{"type": "update", "props": {"orderStatus": "done", "completedAt": "{now}"}, "require_scope_write": …}` |
| `sp_period_reactivate` | `task eq planPeriod`; prompt `confirm` select `yes`/`no` "I checked that this period is needed again" | `{"type": "update", "status": "active", "props": {}, "require_scope_write": …}` |
| `sp_note_done` | `task eq planNote`, `orderStatus eq open`; prompt `note` text, default `no note` | `{"type": "update", "props": {"orderStatus": "done", "completedAt": "{now}"}, "effects": [{"type": "comment", "text": "Done {now} by {user_email}: {note}"}], "require_scope_write": …}` |

Gate these four even though they live only in planning, which staff cannot see — a future shift lead with planning read must not
close periods. An action update raises a trigger event only for the first declared
property (`orderStatus`), not for `startedAt` / `completedAt`; hang triggers on
`orderStatus`.

### 4.6 Demand (optional)

- `sp_demand_report` on `space`, scopes master:
  `{"type": "form_answer", "name": "Demand {now}", "form": "<demand_form_udid>", "result_scope_id": <planning_scope_id>, "require_scope_write": <planning_scope_id>}`.
  (Without `result_scope_id` demand objects land in master; set it. To confirm that
  the answer is created in planning.)
- `sp_demand_status` on `demand`, planning: prompt `demandStatus` select
  (`open`, `planned`, `covered`, `dropped`); `props: {"demandStatus": "{demandStatus}"}`; gate planning.
- `sp_demand_cover` on `shift`, planning: condition `shiftStatus ne cancelled`; prompt
  `demand` (`object_types: ["demand"]`); link `{"type": "concerns", "from": "{object_udid}", "to": "{demand}", "linkvalue": "coversDemand", "require": "absent", "text": "This shift already covers this demand"}`; gate.
- `sp_demand_uncover`: same prompt; link with `"remove": "pair"` and the same `linkvalue`; gate.

A coverage view (demand vs. staffed shifts) is Phase 5 and not part of this skill.

### 4.7 Week generator (request + day triggers)

The generator creates one week of **open** shifts from the templates. It has two
parts because an action update does not raise trigger events for these keys, and
form answers do not either; a direct property write by the agent does.

1. Manager clicks `sp_week_request` on a draft period:

```json
{"key": "sp_week_request", "label": "Request week from templates", "body": {
  "object_types": ["serviceOrder"], "scopes": [<planning_scope_id>], "roles": ["member"],
  "condition": {"props": [
     {"key": "task", "op": "eq", "value": "planPeriod"},
     {"key": "orderStatus", "op": "eq", "value": "open"},
     {"key": "weekRequest", "op": "empty"}],
   "message": "Only for draft periods and only once: the week was already requested"},
  "prompts": [
    {"key": "day1", "label": "Monday of the week (YYYY-MM-DD)", "type": "date", "required": true, "persist": false},
    {"key": "day2", "label": "Tuesday (YYYY-MM-DD)", "type": "date", "required": true, "persist": false},
    {"key": "day3", "label": "Wednesday (YYYY-MM-DD)", "type": "date", "required": true, "persist": false},
    {"key": "day4", "label": "Thursday (YYYY-MM-DD)", "type": "date", "required": true, "persist": false},
    {"key": "day5", "label": "Friday (YYYY-MM-DD)", "type": "date", "required": true, "persist": false},
    {"key": "day6", "label": "Saturday (YYYY-MM-DD)", "type": "date", "required": true, "persist": false},
    {"key": "day7", "label": "Sunday (YYYY-MM-DD)", "type": "date", "required": true, "persist": false}],
  "action": {"type": "update",
    "props": {"weekRequest": "Mon {day1}, Tue {day2}, Wed {day3}, Thu {day4}, Fri {day5}, Sat {day6}, Sun {day7}"},
    "effects": [{"type": "comment", "text": "Week from templates requested {now} by {user_email}: Mon {day1} … Sun {day7} – shifts are created by the agent"}],
    "require_scope_write": <planning_scope_id>}}}
```

2. The agent reads `weekRequest` and writes, for every **opening day** (intake 4), the
   date into `planDay<N>` with `onto_object_set_property` — one call per day.
3. One trigger per opening weekday (section 5.2) creates the shifts of that weekday
   from the template list and sets `generatedDay<N>` so it never runs twice.

Known limits: templates and station objects are fixed in the
trigger (changing a template means updating the trigger); no check that the seven
dates form a Monday–Sunday week; no shifts over midnight; "copy last week" is not
buildable (no loop over links, no date arithmetic).

## 5. Triggers, functions, notifications

### 5.1 Functions

Create with `onto_function_create` (`name`, `key`, `label`, `scope_id`, `body`). All
read the fields of the input object directly.

| Key | Scope | Expression (`body.body`) | Effect |
|---|---|---|---|
| `sp_planned_hours` | planning | `{"hours_between": [{"field": ["shiftStart"]}, {"field": ["shiftEnd"]}, {"field": ["breakMinutes"]}]}` | `set_property` `plannedHours = {result}` |
| `sp_staffing_count` | planning | `{"count_of": [{"linklist": {"type": "worksShift", "dir": "in"}}]}` | none (0 = unstaffed, >1 = double) |
| `sp_person_hours` | master | `{"sum_of": [{"linklist": {"type": "worksShift", "dir": "out", "prop": "plannedHours"}}]}` | none |
| `sp_hours_limit_check` | master | `{"if": [{">": [<sum_of as above>, {"field": ["limit"]}]}, {"cat": ["check: ", <sum_of>, " h > limit ", {"field": ["limit"]}, " h"]}, "ok"]}` | none; extra input `limit` (float) |

```json
{"tool": "onto_function_create", "arguments": {"scope_id": <planning_scope_id>, "name": "Planned hours of a shift",
  "key": "sp_planned_hours", "label": "Planned hours (end − start − break)",
  "body": {"inputs": [{"key": "object", "type": "object", "required": true}],
           "body": {"hours_between": [{"field": ["shiftStart"]}, {"field": ["shiftEnd"]}, {"field": ["breakMinutes"]}]},
           "effects": [{"type": "set_property", "props": {"plannedHours": "{result}"}}],
           "timeout_ms": 3000}}}
```

Notes: `sp_person_hours` sums **all** shifts of a person, not a month — monthly sums
are phase 4. An empty `sum_of` stays empty (not `0`). Name the
input `objekt` (confirm whether the input key is free or must be that word; test
`sp_planned_hours` once with `onto_function_run` before wiring the trigger).

### 5.2 Triggers

Create with `onto_trigger_create` (`name`, `key`, `scope_id = <planning_scope_id>`,
`body`). Triggers run asynchronously (1–5 min); never resend a write because nothing
happened yet. Trigger placeholders: only `{object_udid}`, `{object_name}`,
`{value_new}`, `{value_old}` — an unknown placeholder drops the effect silently.

| Key | `on` | Type | Condition | Effect |
|---|---|---|---|---|
| `sp_planned_hours_update` | `insert,update` | shift | `changed: [shiftStart, shiftEnd, breakMinutes]` | `run_function sp_planned_hours` |
| `sp_cancelled_shift_note` | `update` | shift | `changed: [shiftStatus]`, `shiftStatus eq cancelled` | `create_object` manager note |
| `sp_week_day<N>` (one per opening weekday) | `update` | serviceOrder | `changed: [planDay<N>]`, `task eq planPeriod`, `planDay<N> notempty`, `generatedDay<N> empty` | one `create_object` per template of that weekday + `set_property generatedDay<N> = {value_new}` |

```json
{"tool": "onto_trigger_create", "arguments": {"scope_id": <planning_scope_id>, "name": "Planned hours", "key": "sp_planned_hours_update",
  "body": {"on": "insert,update", "object_types": ["shift"], "enabled": true,
           "condition": {"changed": ["shiftStart", "shiftEnd", "breakMinutes"]},
           "effects": [{"type": "run_function", "function": "sp_planned_hours"}]}}}
```

```json
{"tool": "onto_trigger_create", "arguments": {"scope_id": <planning_scope_id>, "name": "Cancelled shift → note", "key": "sp_cancelled_shift_note",
  "body": {"on": "update", "object_types": ["shift"], "enabled": true,
           "condition": {"changed": ["shiftStatus"], "props": [{"key": "shiftStatus", "op": "eq", "value": "cancelled"}]},
           "effects": [{"type": "create_object", "object_type": "serviceOrder",
                        "name": "Note: shift cancelled – check replacement/demand ({object_name})",
                        "props": {"task": "planNote", "orderStatus": "open"},
                        "links": [{"linktype": "concerns", "to": "{object_udid}", "linkvalue": "followUpOf"}]}]}}}
```

Day trigger (example Tuesday, one template; repeat the `create_object` block for every
template whose `weekdays` contains `2`):

```json
{"tool": "onto_trigger_create", "arguments": {"scope_id": <planning_scope_id>, "name": "Week from templates – Tuesday", "key": "sp_week_day2",
  "body": {"on": "update", "object_types": ["serviceOrder"], "enabled": true,
    "condition": {"changed": ["planDay2"], "props": [
      {"key": "task", "op": "eq", "value": "planPeriod"},
      {"key": "planDay2", "op": "notempty"},
      {"key": "generatedDay2", "op": "empty"}]},
    "effects": [
      {"type": "create_object", "object_type": "shift", "name": "Shift {value_new} 09:00-15:30 kitchen",
       "props": {"shiftStart": "{value_new} 09:00", "shiftEnd": "{value_new} 15:30", "breakMinutes": "30",
                 "plannedHours": "6", "station": "kitchen", "shiftKind": "early", "shiftStatus": "open", "onCall": "no"},
       "links": [
         {"linktype": "derivedFrom", "to": "<template_udid_kitchen_early>"},
         {"linktype": "concerns", "to": "{object_udid}", "linkvalue": "periodShift"},
         {"linktype": "concerns", "to": "<station_udid_kitchen>", "linkvalue": "station"},
         {"linktype": "concerns", "to": "<site_udid>", "linkvalue": "takesPlaceAt"}]},
      {"type": "set_property", "props": {"generatedDay2": "{value_new}"}}]}}}
```

- In triggers the link key is `linktype` (in actions it is `type`).
- The values (`09:00`, `15:30`, `30`, `6`, `kitchen`, `early`) are copied from the
  template; `plannedHours` is written directly (confirm whether objects created by a
  trigger fire `sp_planned_hours_update`; until verified, write it).
- The condition is checked against the current state: never reset `planDay<N>` to an
  empty string and set it again in one go — that produces shifts without a date.
- The shifts are **open**; staff them with `sp_shift_staff`.

### 5.3 Notifications (configured in phase 3)

Phase 1 creates the events; the rules that message people are phase 3 (e-mail/push off
until the phase-3 acceptance). For orientation:

| Event | Who is told |
|---|---|
| first publication of a shift (`published`, marker `firstNoticeStatus` ≠ `sent`) | persons on `worksShift`; then marker `sent` |
| published shift cancelled | persons on `worksShift` |
| already announced shift staffed again (`published` after a change) | persons on `worksShift` |
| `worksShift` link removed (`link_removed`) | the removed person |

## 6. Views

Create with `onto_interface_create_def` (`name`, `label`, `description`,
`scope_id = <planning_scope_id>`, `roles: ["member"]`, `object_type_ids`,
`view_config` as JSON **string**). All phase-1 views are manager views:
`view_config.access.require = "write"` (write on the planning scope). The reference
build had not yet set the gate on these views (confirm after setting: staff are
refused, phase 0 S11). The person rows come from master; the manager reads both
scopes, staff never open these views. Views are paginated (10 rows per page by default,
200 at most) — a period filter is still the cheaper design.

### 6.1 `sp_week_list` — week list (manager)

Base set: shifts; parameter `woche` (any date of the week, 7 days); filter status and
station; cancelled shifts stay visible with a marker.

```json
{"elements": ["filter", "table"],
 "access": {"require": "write"},
 "table": {"from": "objects", "type": "shift", "param": "woche", "span": 7,
  "columns": [
    {"key": "day", "prop": "shiftStart", "format": "wochentag_datum", "label": "Day"},
    {"key": "week", "prop": "shiftStart", "format": "kalenderwoche", "label": "Week"},
    {"key": "time", "prop": "shiftStart", "bis": "shiftEnd", "format": "zeitspanne", "label": "Time"},
    {"key": "station", "prop": "station", "label": "Station",
     "werte": {"kitchen": "Kitchen", "service": "Service", "bar": "Bar", "dishwashing": "Dishwashing", "shiftLead": "Shift lead"}},
    {"key": "staff", "link": "worksShift", "richtung": "rueckwaerts", "type": "person", "prop": ["firstName", "lastName"], "label": "Staffed"},
    {"key": "kind", "prop": "shiftKind", "label": "Kind",
     "werte": {"early": "Early", "late": "Late", "split": "Split", "night": "Night"}},
    {"key": "status", "prop": "shiftStatus", "label": "Status",
     "werte": {"open": "open", "planned": "planned", "published": "published", "cancelled": "cancelled – does not take place", "swapped": "swapped"}}],
  "filter": ["status", "station"],
  "sort": {"key": "day", "dir": "asc"},
  "zeitraum": {"key": "day", "von": "{period_start}", "bis": "{period_end}"}}}
```

`werte` maps a stored value to a display label (label language from intake 19). The
`filter` and `zeitraum` entries name **column keys**, not property keys.

### 6.2 `sp_week_grid` — person × day grid (manager)

Rows: persons with at least one `worksShift` in the week; cells: their shifts placed by
`shiftStart`; several shifts of one person on one day join in one cell with ` · `;
cancelled shifts are marked, not hidden.

```json
{"elements": ["matrix"],
 "access": {"require": "write"},
 "matrix": {"title": "Week plan (people × days)", "param": "woche", "days": 7,
  "rows": {"from": "objects", "type": "person", "label": "lastName",
           "nur_mit": {"linktyp": "worksShift", "type": "shift"}},
  "cells": {"from": "objects", "type": "shift",
            "bruecke": {"linktyp": "worksShift", "type": "person"},
            "zeitfeld": "shiftStart",
            "text": [
              {"prop": "shiftStatus", "werte": {"cancelled": "cancelled", "_": ""}},
              {"prop": "shiftStart", "bis": "shiftEnd", "format": "zeitspanne"},
              {"prop": "station", "werte": {"kitchen": "Kitchen", "service": "Service", "bar": "Bar", "dishwashing": "Dishwashing", "shiftLead": "Shift lead"}}],
            "trenner": " · "}}}
```

`"_": ""` = every other value shows nothing; so only cancelled shifts carry the word.
To hide cancelled shifts instead, add `"wo": [{"prop": "shiftStatus", "op": "!=", "wert": "cancelled"}]`
to `cells`. Open shifts have no person and do not appear in the grid — use the week
list for them.

### 6.3 `sp_next_shift_per_staff` — next shift per person (manager)

One row per person with an upcoming shift (from today, Europe/Berlin), cancelled
shifts ignored; persons without an upcoming shift drop out (`nur`).

```json
{"elements": ["table"],
 "access": {"require": "write"},
 "links": {"next": {"link": "worksShift", "richtung": "vorwaerts", "type": "shift",
                    "sort": {"prop": "shiftStart", "dir": "asc"},
                    "wo": [{"prop": "shiftStatus", "op": "!=", "wert": "cancelled"},
                           {"prop": "shiftStart", "op": ">=", "wert": "{today}"}]}},
 "table": {"from": "objects", "type": "person", "scopes": ["<company>_master"],
  "columns": [
    {"key": "staff", "prop": ["firstName", "lastName"], "label": "Staff member"},
    {"key": "day", "link": "next", "prop": "shiftStart", "format": "wochentag_datum", "label": "Day"},
    {"key": "time", "link": "next", "prop": "shiftStart", "bis": "shiftEnd", "format": "zeitspanne", "label": "Time"},
    {"key": "station", "link": "next", "prop": "station", "label": "Station", "werte": {"kitchen": "Kitchen", "service": "Service", "bar": "Bar", "dishwashing": "Dishwashing", "shiftLead": "Shift lead"}},
    {"key": "status", "link": "next", "prop": "shiftStatus", "label": "Status"}],
  "nur": ["day"],
  "sort": {"key": "day", "dir": "asc"}}}
```

All columns with `"link": "next"` read the **same** shift (the link group is chosen
once). One copy of the `links` block at the top level is the documented form; a
second copy inside `table` also occurs (confirm which one the renderer needs).

### 6.4 Rule check, shift-lead dashboard and trash — block views

Reference: [view-blocks.md](../../../telesherpa-ontology-platform/references/features/view-blocks.md).
All three views below use blocks in planning with `access.require: write`; create them like `sp_week_list`,
using the respective name, label and definition. The three definitions are confirmed
in the browser against a running test workspace (same rows, same counter
values, same warnings). No separate service request is needed. After saving or
changing a view, hard-reload the page: the view is rebuilt from its blocks on every
page load.

#### `sp_rule_check` — "Rule check"

Shows **only the shifts that trip at least one rule** (`nur_treffer: true`), over all
active, not cancelled shifts. Each rule is a warning column: it shows its text when
the condition holds and stays empty otherwise. The person is resolved through the
shift's `worksShift` link.

```json
{"elements": ["filter", "table"],
 "access": {"require": "write"},
 "table": {"from": "objects", "type": "shift", "status": "active",
  "wo": [{"prop": "shiftStatus", "op": "!=", "wert": "cancelled"}],
  "columns": [
    {"key": "day", "prop": "shiftStart", "format": "wochentag_datum", "label": "Day"},
    {"key": "time", "prop": "shiftStart", "bis": "shiftEnd", "format": "zeitspanne", "label": "Time"},
    {"key": "staff", "link": "worksShift", "richtung": "rueckwaerts", "type": "person", "prop": ["firstName", "lastName"], "label": "Staff"},
    {"key": "station", "prop": "station", "label": "Station"}],
  "regeln": [
    {"key": "longShift", "feld": "plannedHours", "op": ">", "wert": 10, "text": "Over 10 planned hours"},
    {"key": "breakCheck", "art": "pause", "text": "Break too short"}],
  "personenregeln": [
    {"key": "minorLate", "art": "u18", "datum": "shiftStart", "zeit_ab": "22:00", "text": "Minor after 22:00"},
    {"key": "dailyHours", "art": "tagessumme", "wert": 10, "datum": "shiftStart", "text": "Over 10 hours that day"},
    {"key": "shortRest", "art": "ruhezeit", "wert": 11, "datum": "shiftStart", "text": "Less than 11 hours rest"}],
  "filter": ["station"],
  "sort": {"key": "day", "dir": "asc"},
  "nur_treffer": true}}
```

What each rule does (confirmed behaviour):

| Key | Block | Fires when |
|---|---|---|
| `longShift` | `regeln`, `feld`/`op`/`wert` | `plannedHours` > 10. `op` is one of `=`, `!=`, `>`, `<`, `>=`, `<=`; `wert` is a number |
| `breakCheck` | `regeln`, `art: "pause"` (no `feld`/`wert`) | the shift (start to end) lasts more than 6 h and `breakMinutes` < 30, or more than 9 h and `breakMinutes` < 45 |
| `minorLate` | `personenregeln`, `art: "u18"` | the person on the shift is under 18 **and** the shift **ends** after `zeit_ab`. Age = current year − year of `birthYear` (birthdays inside the year are not considered). `zeit_feld` switches the compared time (default `shiftEnd`) |
| `dailyHours` | `personenregeln`, `art: "tagessumme"` | the planned hours of the same person on that day add up to more than `wert`. Only shifts **with** a person count; cancelled shifts do not count |
| `shortRest` | `personenregeln`, `art: "ruhezeit"` | the gap between the end of the same person's previous shift and this start is below `wert` hours. A shift without a previous shift never fires |

- Each rule `key` is a column key: unique in the view, never equal to another column.
- Thresholds illustrate the DE country module ([country-de.md](country-de.md) §2);
  adapt them per country. The rules are **review flags**, not a legal verdict; the
  youth flag does not replace all youth-protection checks.
- An unstaffed shift can still fire `longShift` and `breakCheck` (they look at the
  shift only), never the person rules.
- Optional week window: add `"param": "woche", "span": 7` and
  `"zeitraum": {"key": "day", "von": "{period_start}", "bis": "{period_end}"}` to the
  table, as in `sp_week_list`. Without it the view checks every active shift; with
  `nur_treffer` it stays short.
- Test data matters: two test shifts of the same person on one day are added up by
  `dailyHours`. Before you report a wrong warning, open the flagged shifts and check
  who is staffed on them.

#### `sp_shift_lead_today` — "Shift lead today"

Opens on **today** (`basis: "heute"`, one day) and shows three counters above the
day's shift table. The counter items are the confirmed definitions of the reference
workspace:

| Counter | Counts |
|---|---|
| Open shifts today | shifts of the selected day without any `worksShift` person (`ohne_link`), from `{period_start}` to `{period_end_dt}` (last day 23:59:59) |
| Started without actual time | shifts of **any** date whose start lies before `{now}` and whose `actualStart` is empty (`op: "leer"`, no `wert`) |
| Open requests | `changeRequest` objects with `changeStatus = proposed` in the planning scope only (`scopes`); all request kinds, all dates |

```json
{"elements": ["counters", "table"],
 "access": {"require": "write"},
 "counters": {"from": "objects", "zaehler": [
   {"type": "shift", "label": "Open shifts today",
    "ohne_link": {"link": "worksShift", "richtung": "rueckwaerts"},
    "filter": [{"feld": "shiftStart", "op": ">=", "wert": "{period_start}"},
               {"feld": "shiftStart", "op": "<=", "wert": "{period_end_dt}"}]},
   {"type": "shift", "label": "Started without actual time",
    "filter": [{"feld": "actualStart", "op": "leer"},
               {"feld": "shiftStart", "op": "<", "wert": "{now}"}]},
   {"type": "changeRequest", "label": "Open requests",
    "filter": [{"feld": "changeStatus", "op": "=", "wert": "proposed"}],
    "scopes": [<planning_scope_id>]}]},
 "table": {"from": "objects", "type": "shift", "status": "active",
  "param": "tag", "span": 1, "basis": "heute",
  "zeitraum": {"key": "day", "von": "{period_start}", "bis": "{period_end}"},
  "columns": [
    {"key": "day", "prop": "shiftStart", "format": "wochentag_datum", "hidden": true},
    {"key": "time", "prop": "shiftStart", "bis": "shiftEnd", "format": "zeitspanne", "label": "Time"},
    {"key": "station", "prop": "station", "label": "Station"},
    {"key": "staff", "link": "worksShift", "richtung": "rueckwaerts", "type": "person", "prop": ["firstName", "lastName"], "label": "Staff"},
    {"key": "actualStart", "prop": "actualStart", "format": "zeit", "label": "Actual start"},
    {"key": "status", "prop": "shiftStatus", "label": "Status"}],
  "sort": {"key": "day", "dir": "asc"},
  "row_actions": [{"action": "sp_actual_correct", "label": "Correct actual time", "icon": "time"}]}}
```

Rules for counters (all confirmed):
- `counters.from` must be `"objects"`; without it no counter appears and no error is shown.
- Each item needs `type` and `label`. A `filter` entry with `op` `=`, `!=`, `>`, `<`,
  `>=`, `<=` needs a `wert`; `leer` / `nicht_leer` take none. A filter without a
  needed `wert` is refused on save.
- Placeholders are written bare inside `wert` (`"{now}"`, `"{period_start}"`,
  `"{period_end_dt}"`). For a datetime field use `<= {period_end_dt}`, not
  `< {period_end}` — `{period_end}` is a date and `<` would drop the last day.
- Counter time filters refer to the period of the table (`param`/`span`/`basis`).
- `ohne_link` works in a counter item exactly as on a table.
- `scopes: [<planning_scope_id>]` on an item restricts it to that scope; without it a
  counter counts in every scope the reader can read.
- "Started without actual time" deliberately looks at all dates, so a forgotten
  clock-in stays visible until the manager corrects it. Cancelled and unstaffed past
  shifts count as well. To count only today, add the two `{period_start}` /
  `{period_end_dt}` filters of the first counter.

The table is the source of truth; `sp_request_inbox` (phase 2) lists the requests
behind the third counter.

#### `sp_recycle_bin` — "Trash"

`status: "deleted"` selects deleted objects; `active` is the default and `any`
selects both. A block list shows **one object type**, so the trash is one view per
type. Start with deleted shifts:

```json
{"elements": ["table"],
 "access": {"require": "write"},
 "table": {"from": "objects", "type": "shift", "status": "deleted",
  "columns": [
    {"key": "udid", "system": "udid", "hidden": true},
    {"key": "name", "system": "name", "label": "Shift"},
    {"key": "day", "prop": "shiftStart", "format": "wochentag_datum", "label": "Day"},
    {"key": "time", "prop": "shiftStart", "bis": "shiftEnd", "format": "zeitspanne", "label": "Time"},
    {"key": "modified", "system": "modified", "format": "wochentag_datum_zeit", "label": "Deleted / changed"}],
  "sort": {"key": "modified", "dir": "desc"},
  "row_actions": [
    {"action": "sp_restore", "label": "Restore", "icon": "refresh"},
    {"action": "sp_delete_for_good", "label": "Delete for good", "icon": "trash"}]}}
```

For the other deletable types use sibling views (`sp_recycle_bin_notes` for
`serviceOrder`, `sp_recycle_bin_absences` for `absence`, `sp_recycle_bin_templates`
for `shiftTemplate` in master, `sp_recycle_bin_demands` for `demand`). Copy the
definition, change `type`, and keep only the system columns `udid`, `name`,
`modified`; a field of another type is refused. Keep `status: "deleted"`, both row
actions and the write gate. A `type` is required — a list without one is refused.

#### `sp_notes_open` — "Open manager notes"

Use `serviceOrder` with `wo` filters `task = planNote`, `orderStatus = open`, and
row action `sp_note_done` (confirm in the browser). No counter is needed to use the
filtered table. Do not widen rights or copy data to make any view work.

## 7. Recipe (tool order with example arguments)

Example business: `Trattoria Example` (scope slug `trattoria`, see phase 0). Run one
call at a time, read back after each write, log ids.

```json
[
  {"tool": "onto_object_create", "arguments": {"type": "organisation", "name": "Trattoria Example", "scope_id": <master_scope_id>, "external_id": "TEST-1-BUSINESS"}},

  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_site_create", "label": "Create site", "body": "<JSON string of 4.2>"}},
  {"tool": "onto_actiondef_list", "arguments": {"limit": 200}},
  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_site_create", "udid": "<business_udid>",
     "prompts": {"siteName": "TEST-1 Trattoria Example", "street": "Example Street 1", "postalCode": "12345", "city": "Example City", "notes": "Tue–Sun 11:30–14:30, 17:30–23:00"}}},

  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_station_create", "label": "Create station", "body": "<JSON string>"}},
  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_station_create", "udid": "<site_udid>",
     "prompts": {"stationName": "Kitchen", "minStaff": 2, "notes": "TEST-1"}}},

  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_staff_create", "label": "Create staff member", "body": "<JSON string of 4.2>"}},
  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_staff_create", "udid": "<site_udid>",
     "prompts": {"firstName": "Test", "lastName": "Cook", "email": "test.cook@example.com", "birthYear": 1990, "station": "<station_udid_kitchen>"}}},

  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_template_create", "label": "Create shift template", "body": "<JSON string>"}},
  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_template_create", "udid": "<station_udid_kitchen>",
     "prompts": {"templateName": "Kitchen early", "start": "09:00", "end": "15:30", "break": 30, "weekdays": "2,3,4,5,6,7", "station": "kitchen", "validFrom": "2026-11-16"}}},

  {"tool": "onto_function_create", "arguments": {"scope_id": <planning_scope_id>, "key": "sp_planned_hours", "name": "Planned hours of a shift", "body": {"...": "see 5.1"}}},
  {"tool": "onto_trigger_create",  "arguments": {"scope_id": <planning_scope_id>, "key": "sp_planned_hours_update", "name": "Planned hours", "body": {"...": "see 5.2"}}},
  {"tool": "onto_trigger_create",  "arguments": {"scope_id": <planning_scope_id>, "key": "sp_cancelled_shift_note", "name": "Cancelled shift → note", "body": {"...": "see 5.2"}}},

  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_period_create", "label": "Create plan period", "body": "<JSON string of 4.3>"}},
  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_period_create", "udid": "<site_udid>",
     "prompts": {"from": "2026-11-16", "to": "2026-11-22"}}},

  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_open_shift_create", "label": "Create open shift", "body": "<JSON string>"}},
  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_open_shift_create", "udid": "<site_udid>",
     "prompts": {"date": "2026-11-17", "start": "09:00", "end": "15:30", "break": 30, "kind": "early", "stationValue": "kitchen", "period": "<period_udid>", "stationObj": "<station_udid_kitchen>"}}},

  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_shift_staff", "label": "Staff shift", "body": "<JSON string of 4.4>"}},
  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_shift_staff", "udid": "<shift_udid>", "prompts": {"staff": "<person_udid>"}}},

  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_shift_publish", "label": "Publish shift", "body": "<JSON string of 4.4>"}},
  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_shift_publish", "udid": "<shift_udid>"}},

  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_week_list", "label": "Week plan (managers)", "scope_id": <planning_scope_id>,
     "roles": ["member"], "object_type_ids": [<shift_type_id>], "description": "All shifts of a week with staffing; managers only.",
     "view_config": "<JSON string of 6.1>"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_week_grid", "label": "Week grid", "scope_id": <planning_scope_id>,
     "roles": ["member"], "object_type_ids": [], "description": "People × days; managers only.", "view_config": "<JSON string of 6.2>"}},
  {"tool": "onto_interface_show", "arguments": {"name": "sp_week_list"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_rule_check", "label": "Rule check", "scope_id": <planning_scope_id>, "roles": ["member"], "object_type_ids": [<shift_type_id>], "view_config": "<JSON string of 6.4 rule check>"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_shift_lead_today", "label": "Shift lead today", "scope_id": <planning_scope_id>, "roles": ["member"], "object_type_ids": [<shift_type_id>], "view_config": "<JSON string of 6.4 dashboard>"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_recycle_bin", "label": "Trash", "scope_id": <planning_scope_id>, "roles": ["member"], "object_type_ids": [<shift_type_id>], "view_config": "<JSON string of 6.4 trash>"}},

  {"tool": "onto_property_def_create", "arguments": {"scope_id": <planning_scope_id>, "type_ids": [<serviceOrder_type_id>], "key": "weekRequest", "value_type": "string", "label": "Week requested"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_week_request", "label": "Request week from templates", "body": "<JSON string of 4.7>"}},
  {"tool": "onto_trigger_create", "arguments": {"scope_id": <planning_scope_id>, "key": "sp_week_day2", "name": "Week from templates – Tuesday", "body": {"...": "see 5.2"}}},
  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_week_request", "udid": "<period_udid>",
     "prompts": {"day1": "2026-11-16", "day2": "2026-11-17", "day3": "2026-11-18", "day4": "2026-11-19", "day5": "2026-11-20", "day6": "2026-11-21", "day7": "2026-11-22"}}},
  {"tool": "onto_object_set_property", "arguments": {"udid": "<period_udid>", "key": "planDay2", "value": "2026-11-17", "scope_id": <planning_scope_id>}}
]
```

Order of definitions: master-data actions → functions and triggers (before the first
shift exists, because triggers hang on insert) → period and shift actions → views →
generator. Define each action, list it, run it once on a `TEST-1-` object, read back.

## 8. Smoke tests (MCP)

| # | Call | Expected |
|---|---|---|
| P1-1 | `onto_actiondef_list` | every action of 4.1 present, each manager action with `require_scope_write` |
| P1-2 | `sp_staff_create` → `onto_object_show` person | only basic fields; links `employedAt` → site, `qualifiedFor` → station; no phone/pay |
| P1-3 | `sp_open_shift_create` → read shift after ≤ 5 min | `shiftStatus open`, `station` option set, links `periodShift`, `station`, `takesPlaceAt`; `plannedHours` = 6.0 for 09:00–15:30 with 30 min |
| P1-4 | read `shiftStart` | returned as UTC (09:00 Berlin in winter = `08:00:00`) |
| P1-5 | `sp_shift_staff` with a person **not** qualified for the station | person not offered / call refused |
| P1-6 | `sp_shift_staff` qualified person, then again with the same person | first: `planned` + comment; second: refused ("already on this shift") |
| P1-7 | `sp_shift_publish` on an `open` shift | refused with the condition message |
| P1-8 | `sp_shift_publish` on the planned shift | `published`, `publishedAt` set; read back the `{now}` value and the comment time (SKILL.md, "`{now}` in actions"): same moment, returned as UTC |
| P1-9 | `sp_shift_cancel` → after ≤ 5 min `onto_object_index` serviceOrder | one manager note `task planNote`, `followUpOf` → shift |
| P1-10 | `sp_shift_release` with the staffed person | `open`, exactly that `worksShift` link gone, other links untouched |
| P1-11 | `sp_week_request` twice | first ok (`weekRequest` + comment), second refused |
| P1-12 | `onto_object_set_property planDay2`, wait ≤ 5 min, list shifts of the period | one open shift per Tuesday template; `generatedDay2` set; writing `planDay2` again creates nothing |
| P1-13 | `onto_interface_show sp_week_list` | `access.require` = `write`; definition uses blocks only |
| P1-14 | `onto_credit_balance` | spend logged against the phase budget |
| P1-15 | read `sp_rule_check`, `sp_shift_lead_today`, `sp_recycle_bin` | definitions as in §6.4 (`regeln` with `art: pause`, `personenregeln`, `nur_treffer`, three counter items, `basis: heute`, `status: deleted`), write gates present |
| P1-16 | browser: counters against the day table and the inbox, rule columns against the test shifts, trash with a deleted probe | numbers and rows as in §9; restore removes the probe from the trash |

## 9. Browser checks

| Role | Check | Expected |
|---|---|---|
| manager | open the site → buttons | Create station / staff member / open shift / plan period visible |
| manager | open `sp_week_list?woche=<a date of the week>` | 7 days, filters status and station work, cancelled shift shows "cancelled – does not take place", time as `09:00 - 15:30` in Europe/Berlin |
| manager | open `sp_week_grid?woche=…` | one row per staffed person, cells `time · station`, two shifts on one day in one cell, cancelled marked |
| manager | "Staff shift" dialog | picker lists only persons qualified for the shift's station |
| manager | "Create open shift" with time `7:30` | refused (two digits needed) |
| staff (test account, once it exists) | open the site in master | **no** create/staff/publish buttons (master gate) |
| staff | open `sp_week_list` / `sp_week_grid` / `sp_rule_check` / `sp_shift_lead_today` / `sp_recycle_bin` by URL | refused (`access.require`) |
| manager | rule check | only rows with a warning; an 8-hour shift with 0 min break shows "Break too short"; a minor's shift ending 23:00 shows "Minor after 22:00"; a shift starting less than 11 h after the same person's previous shift shows "Less than 11 hours rest"; an unstaffed shift never shows a person rule |
| manager | shift lead today | opens on today's date (period picker today–today); "Open shifts today" = rows of the day without a person; "Started without actual time" = all past shifts without actual start; "Open requests" = proposed rows in `sp_request_inbox` |
| manager | trash: deleted TEST probe, restore | only deleted probe shown; restored probe disappears from the trash and is back in the week list |

## 10. Failure patterns

| Symptom | Cause | Fix |
|---|---|---|
| staff see "Create staff member" on the site | master action without `require_scope_write: <master_scope_id>` | add the gate |
| shift created but `plannedHours` empty | trigger created after the shift, or trigger condition missing a key | create triggers first; set start/end once more by action |
| `plannedHours` negative or wrong for a night shift | end on the same date as start | end-date prompt (confirm it, 4.3) |
| station column empty in the week list | `station` option not set by the create action | set `stationValue` (4.3) |
| staffing picker empty | shift has no `station` link, or persons lack `qualifiedFor` | link the station; qualify the person |
| release removed every person | `remove: true` used | always `remove: "pair"` |
| generator created shifts without a date | `planDay<N>` reset and set in one step | never reset; one write per day |
| generator created nothing | written by action or form (no trigger event), or `generatedDay<N>` already set | write with `onto_object_set_property`; check the lock |
| comment shows no text | optional prompt empty → effect skipped | give the prompt a `default` |
| `{staff_name}` stays literal in a name | `{<prompt>_name}` works only in effects | use it in comments only |
| view refuses to save | placeholder or `werte` key wrong, or a filter names a property instead of a column key | use column keys in `filter`/`sort`/`zeitraum` |
| only ten rows visible | page size default | raise `limit` (max 200) or add a period filter |
| staff open a manager view | `access.require` missing | set it; never grant planning read instead |

## 11. Before you leave phase 1

**Costs.** Definition calls book no credits (phase 0, section 7). The staffed test week
is what you pay for — read every account's balance before and after it.

**Night shifts.** A shift that runs past midnight keeps its start day in the week
views, and the end-date prompt and 6.5 planned hours are confirmed (§4.3). Prove it
once with a TEST night shift D 18:00 – D+1 01:00 and a TEST shift of the same person
on D+1 09:00: the week views show the night shift on D, the rule check flags
`shortRest` (8 hours) on D+1 and no `dailyHours`. Delete both test shifts afterwards.

**Two design rules of this skill.** A station is either an option value or a station
link, never both — views read from one source. And every manager view carries
`access.require` (phase 0, S11): staff get a refusal, not a read.
