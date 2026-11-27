# Phase 0 — scopes, rights, object types, properties

**Goal:** three empty scopes with the right types activated, the scope-specific
properties created, the rights of every account written down and set, and a smoke
test that proves the **definitions** are in place as this skill expects (scopes,
types, fields, option values, link types, rights). The smoke test only reads; the
behaviour of bridges, guards and views is proven by the tests of phases 1–4. No
business data yet (that is phase 1).

**Input:** answered [intake](intake.md) (questions 1, 8, 9, 13, 19, 21) and the checks
from [prerequisites](prerequisites.md).

**Budget (pay-per-use):** 260 credits for the three scopes (100 + 80 + 80 — the price per scope
falls with the number of own scopes; there is no upper limit), plus reads. Definition
calls (types, properties) have no own price key — log what is booked.

Placeholders used below: `<company>` (scope slug from intake 21),
`<master_scope_id>`, `<planning_scope_id>`, `<team_scope_id>` (numbers returned by
`ontouser_scope_create`), `<shift_type_id>`, `<changeRequest_type_id>`,
`<shiftTemplate_type_id>` (from
`onto_type_show` → `type.id`), `<staff_profile_id>`, `<lead_profile_id>` (from
`ontouser_team_index`).

---

## 1. Definitions

### 1.1 Scopes

| Scope name | Purpose | Holds | Who works here |
|---|---|---|---|
| `<company>_master` | master data | business, sites, stations, people (**basic** fields), shift templates, qualification files | managers write; staff read |
| `<company>_planning` | planning | shifts, absences, change requests, demands, plan periods, manager notes, comments; **all triggers, functions and manager views** | managers (and shift leads) |
| `<company>_team` | team door | staff views ("my shifts", "my requests"), staff-facing forms; actions shared with planning | staff |

Rules:
- Names: `a-z0-9_`, max 30 characters. Check the longest one (`<company>_planning`).
- The scope is the lock. Never rely on a view filter to hide data; put the data in the right scope.
- Write all three names and returned ids into your run log.
- **Links cross scopes.** A link may join objects of different scopes: `worksShift`
  runs from a person in master to a shift in planning, `qualifiedFor` from a person in
  master to a station in master, `station` from a shift in planning to a station in
  master. The manager creates them (write on both scopes). Staff resolve the master
  end (person and station names) because they read master.

### 1.2 Rights matrix

Read / Write / Manage per account. `–` = no grant at all.

| Account | `<company>_master` | `<company>_planning` | `<company>_team` |
|---|---|---|---|
| Manager / owner (builds the workspace) | R W M | R W M | R W M |
| Shift lead (optional, intake 9) | R – – | R W – | R W – |
| Staff member | **R – –** | **– – –** | R W – |

Notes:
- **Staff: no membership on planning** (neither read nor write). A planning object
  opens for a staff member **only through the person link** — a shift linked to their
  master person by `worksShift`, an absence or request linked to that person by
  `concerns`. A colleague's shift, absence or request stays closed and answers as if
  it did not exist. Team views such as "My shifts" take shifts as their base set with
  the `person` block via `worksShift`; request/absence views bind via `concerns`;
  `passt` selects matching open shifts. The views list what the person link reaches;
  they do not filter a readable scope. The write door is the **scope bridge**
  (`result_scope_id`): staff change planning data only through team-scope actions
  that open a one-shot write; buttons on own rows carry a guard on that person.
- **The person link opens the whole object.** Anything stored on a shift, absence or
  request of a person is visible to that person. Put no manager-only remarks there;
  manager notes are separate `serviceOrder` notes (phase 1) that are not linked to a
  person.
- **Staff: read on master, no write.** Needed so team views can resolve the bound
  person and station names from master. Do **not** put protected data on those shared
  master objects (see E2 below).
- **E2 — basic data for all, protected data for managers only.** On staff-readable
  master `person` objects keep only basic fields (e.g. `firstName`, `lastName`,
  `email`, station/qualification links). Pay (`hourlyRate`), health-related notes,
  private phone/address and similar must live in the **planning** scope (manager-only
  objects or fields read by gated payroll/person views) — not on master persons every
  staff member can read via the API.
- Staff need write on the team scope because their forms and requests are submitted
  from there.
- Manage does not imply read or write. Set all three switches explicitly.
- `ontouser_team_set_scope_rights` works only for **managed** accounts (managed by one
  of your scopes). It refuses manage on the managing scope itself (403).
- Owner rights: the creator of a scope manages it. Confirm read and write for yourself
  with `ontouser_scope_index` after creation; never assume.
- Do **not** grant planning read to staff "so views work". Master read + person links +
  the team door are enough; planning membership would expose foreign objects.
- **Shift leads** hold planning read, so they see every planning object, including
  the staff records with pay (phase 4 §1.2). If shift leads must not see pay, decide
  this with the business at intake 9 before phase 4.

### 1.3 Object types per scope

Activation (`ontouser_scope_types_set`) only fills the suggestion list of the object
dialog. **It is not access control** — rights come from the scope. The list you send
**replaces** the previous one; read it first with `ontouser_scope_types`.

| Type | master | planning | team |
|---|---|---|---|
| `organisation` | ✔ | | |
| `building` | ✔ | | |
| `space` | ✔ | | |
| `person` | ✔ | phase 4 staff records only | |
| `shiftTemplate` | ✔ | | |
| `file` | ✔ | ✔ | |
| `comment` | ✔ | ✔ | |
| `shift` | | ✔ | |
| `absence` | | ✔ | |
| `changeRequest` | | ✔ | |
| `demand` | | ✔ | |
| `serviceOrder` | | ✔ | |

Team scope: activate nothing. It holds views, forms and actions, not business objects.

`changeRequest` did not appear in the activation list of `ontouser_scope_types` on
2026-11-06 but objects of that type were created in the planning scope by actions
without problems. If `ontouser_scope_types_set` rejects it, leave it out and continue;
check in phase 2 that requests land in planning.

### 1.4 Platform properties you use (verify; override options in the customer scope)

Read with `onto_type_show` and compare. Non-option fields (datetimes, ints, floats,
strings) you use as they are. **Option values are plain strings with no i18n** — there
is no translation layer for the value list. Members **may** create **scope-specific**
property definitions (pass `scope_id`) that override the option list for that scope.
**Do that in this skill:** put **English** option values on the customer scopes. The
platform's German default values stay as they are — do not build the customer
workspace on them.

Recommended English option sets for this skill (create as scope-specific defs in
planning and, where needed, master):

**`shift`** (keys exist on the platform type; override options where listed)

| Key | Type | Scope-own English values / default | Purpose |
|---|---|---|---|
| `shiftStart` | datetime | | planned start |
| `shiftEnd` | datetime | | planned end (may be after midnight) |
| `breakMinutes` | int | default `0` | planned break |
| `plannedHours` | float | | computed by function (phase 1) |
| `shiftKind` | options | `early`, `late`, `split`, `night` | |
| `station` | options | from intake (e.g. `kitchen`, `service`, `bar`, `dishwashing`, `shiftLead`) | |
| `shiftStatus` | options | `open` (default), `planned`, `published`, `swapped`, `cancelled` | |
| `publishedAt` | datetime | | set when published |
| `onCall` | options | `yes`, `no` | on-call work |
| `actualStart` | datetime | | clock-in time (phase 4) |

The platform shift type also carries an older first-publication field with a German
key and German values. Do not use it; this skill creates its own English marker
`firstNoticeStatus` (section 1.5).

**`person` (master — basic, staff-readable):** `firstName`, `lastName`, `email`
(string — **required in practice**: binds the login to the person), `birthYear`
(datetime; write `YYYY-01-01`, show it with the view format `jahr`; only if
youth-protection checks need it). Colleagues can read these fields (login e-mail,
birth year); ask the business with intake question 13a before you record them. Station eligibility via qualification links, not
free text.

**Protected (managers only — store in planning, not on the shared master person):**
`hourlyRate` (float, EUR), private `phone` / address fields, health-related notes.
`contractType` (scope-own options e.g. `minijob`, `partTime`, `fullTime`, `fixedTerm`,
`casual` — keep `minijob` if the DE country module needs that exact token) is used by
payroll and limit checks: keep it on a manager-readable planning-side record (or a
manager-gated view over planning), not on the staff-readable master person. Phase 4
payroll view stays in planning with `access.require`.

**`shiftTemplate`**: `templateName` (string), `startTime` / `endTime` (string `HH:MM`),
`breakMinutes` (int), `weekdays` (string of ISO weekday numbers, `1` = Monday …
`7` = Sunday, e.g. `2,3,4,5,6` = Tuesday to Saturday), `station` (same English
options as on shift), `validFrom` (date).

**`absence`**: `absenceKind` (scope-own: `vacation`, `sick`, `dayOffWish`, `training`,
`availability`), `absenceStart` / `absenceEnd` (datetime), `halfDay` (`no`,
`firstHalf`, `secondHalf`), `absenceNote` (string — **no diagnosis**),
`absenceStatus` (`requested` default, `approved`, `rejected`).

**`changeRequest`**: `text` (string), `proposedKey` (string), `changeStatus` (options
`proposed`, `accepted`, `rejected` — already English on the platform).

**`demand`**: `demandKind` (`staff`, `material`, `service`, `capacity`),
`demandStart` / `demandEnd`, `demandQuantity` (float), `demandUnit` (`persons`,
`hours`, `pieces`, `units`), `demandStatus` (`open` default, `planned`, `covered`,
`dropped`).

#### Option overrides — the complete list

Every option field below gets a **scope-specific definition with the same key** as
the platform field, created with `onto_property_def_create` (`scope_id`, `type_ids`,
`key`, `value_type: "options"`, `label`, `options` as JSON string, optional
`default_value`). Inside that scope it replaces the platform's German option list;
other scopes are not affected. Fields marked "new" have no platform definition and
are created in section 1.5.

| Type | Key | Scope | English values (first = default where marked) | Default |
|---|---|---|---|---|
| shift | `shiftStatus` | planning | `open`, `planned`, `published`, `swapped`, `cancelled` | `open` |
| shift | `shiftKind` | planning | `early`, `late`, `split`, `night` | – |
| shift | `station` | planning | stations from intake 3, e.g. `kitchen`, `service`, `bar`, `dishwashing`, `shiftLead` | – |
| shift | `onCall` | planning | `yes`, `no` | `no` |
| shiftTemplate | `station` | master | the same station values as on shift | – |
| absence | `absenceKind` | planning | `vacation`, `sick`, `dayOffWish`, `training`, `availability` | – |
| absence | `absenceStatus` | planning | `requested`, `approved`, `rejected` | `requested` |
| absence | `halfDay` | planning | `no`, `firstHalf`, `secondHalf` | `no` |
| demand | `demandKind` | planning | `staff`, `material`, `service`, `capacity` | – |
| demand | `demandStatus` | planning | `open`, `planned`, `covered`, `dropped` | `open` |
| demand | `demandUnit` | planning | `persons`, `hours`, `pieces`, `units` | – |
| changeRequest | `requestKind` (new) | planning | `swap`, `takeover`, `handover`, `shiftRequest` | – |
| shift | `clockStatus` (new) | planning | `clockedIn`, `clockedOut`, `corrected` | – |
| shift | `firstNoticeStatus` (new) | planning | `open`, `sent` | `open` |
| staff record | `contractType` | planning | from intake 11, e.g. `minijob`, `partTime`, `fullTime`, `fixedTerm`, `casual` | – (phase 4) |

No override is needed for `changeRequest.changeStatus`, `serviceOrder.orderStatus`
and `serviceOrder.priority` — their platform values are already English. Do not
override `contractType` in master: contract data does not belong on the master
person (E2).

**Turning intake answers into values:** one value per answer, English, camelCase,
ASCII letters only, starting lower case, no spaces (e.g. "Front desk" →
`frontDesk`, "Shift lead" → `shiftLead`). The business-language name becomes the
option **label**, never the value. Write the value list into the run log before you
create the definition.

**Adding a value later** (a new station): `onto_property_def_update` on the scope
definition with `def_id`, `label` (required on every update) and the **complete**
`options` list — the list you send replaces the old one. Existing objects keep their
stored value; a value you drop is shown raw. Also create the new `space` object and
its qualification links (phase 1). Read back with `onto_type_show`.

Where station values also appear (update each, otherwise the new station shows raw):
- action prompts with station options: `sp_template_create`, `sp_shift_from_template`,
  `sp_open_shift_create`;
- the `werte` maps of every view that shows the station column (phase 1, 2, 3 views);
- the weekday triggers of the week generator (phase 1 §4.7);
- the station labels in the label language (intake 19).

**`serviceOrder`**: `task` (string; exactly `planPeriod` for a plan period or
`planNote` for a manager note — the two uses are told apart only by this value),
`orderStatus` (`open`, `inProgress`, `done` — already English on the platform),
`description`, `priority` (`low`, `medium`, `high` — already English), `startedAt`,
`completedAt`.

**`space`**: `description`, `capacity`, `areaSqm`, `occupancy` — the station name is the object name.

### 1.5 Scope-specific properties you create (planning scope)

Created with `onto_property_def_create` **with** `scope_id = <planning_scope_id>` (needs
manage on that scope). Without `scope_id` the call is refused for a member account —
always pass it.

| Type | Key | value_type | Options / limits | Label (example, EN) | Used in |
|---|---|---|---|---|---|
| shift | `actualEnd` | datetime | | Actual end | phase 4 |
| shift | `actualBreakMinutes` | int | min 0, max 600 | Actual break (minutes) | phase 4 |
| shift | `actualHours` | float | | Actual hours (computed) | phase 4 |
| shift | `clockStatus` | options | `clockedIn`, `clockedOut`, `corrected` | Clock status | phase 4 |
| shift | `actualChangedBy` | string | | Actual time last changed by | phase 4 |
| shift | `actualChangedAt` | datetime | | Actual time last changed at | phase 4 |
| shift | `firstNoticeStatus` | options | `open` (default), `sent` | First notice | phase 3 |
| changeRequest | `requestKind` | options | `swap`, `takeover`, `handover`, `shiftRequest` | Request kind | phase 2 |

Keys in section 1.5 are the **public English names**. Phases 1–4 of this skill use
these English keys and the English option values from 1.4 — do not mix with platform
German defaults.

Labels: write them in the label language from intake 19. Labels with the prefix `mo.`
are reserved for the platform — do not use it. Labels and option values are plain
strings in the workspace language; they are not translated per viewer.

### 1.6 Link types (platform, verify only)

| Key | From → To | Verb (display) | Use |
|---|---|---|---|
| `bestehtAus` | organisation → building → space | consists of / is part of | business tree |
| `worksShift` | person → shift | works / is staffed by | staffing; core of "my shifts" and of the guard |
| `derivedFrom` | shift → shiftTemplate | derived from / template for | shift made from template |
| `concerns` | any → any, with a **link value** naming the role | concerns | see roles below |
| `hasfile` | any → file | has file | qualification document |
| `performs` | person → serviceVisit | performs | legacy actual-time path; not used in this skill |

`concerns` link values (the role is the `linkvalue` string you set; use these exact
English values in all phases):

| From → To | `linkvalue` | Meaning |
|---|---|---|
| shift → space | `station` | shift belongs to station |
| shift / serviceOrder → building | `takesPlaceAt` | site |
| shift → serviceOrder | `periodShift` | shift belongs to plan period |
| shiftTemplate → space | `station` | template belongs to station |
| person → space | `qualifiedFor` | person may work at station |
| person → building | `employedAt` | person works at this site (phase 1) |
| changeRequest → shift | `shiftRequest` / `shiftSwap` / `counterShift` | request is about this shift (phase 2) |
| changeRequest → person | `requestedBy` / `takingOver` | requester / partner (phase 2) |
| absence → person | `concernsPerson` | absence of this person |
| staff record → person | `staffRecordOf` | protected record of this person (phase 4) |
| serviceOrder (note) → object | `followUpOf` | manager note caused by object |

Link values are case-sensitive strings. Placeholders such as
`{linked:concerns:shiftRequest:name}` in phase 3 depend on them.

**Station: option and link, two jobs.** Every shift carries the station twice, and
both are set by the same create action (phase 1 §4.3) and the week generator:
- the **option** `station` is what views **show and filter** (columns, filter bar,
  `regeln`);
- the **link** `concerns` / `station` → `space` is what **qualification matching**
  uses (`options_filter` of the staffing and swap pickers, `passt` of "Open shifts
  for me").
Keep them identical. A shift with only the option has an empty staffing picker; a
shift with only the link shows an empty station column.

---

## 2. Complete example (tool calls in order)

Replace placeholders; run one call at a time and read the response before the next.

```json
[
  {"tool": "ontouser_scope_create", "arguments": {"name": "trattoria_master",   "description": "Shift planning: master data (managers write; staff read basic)"}},
  {"tool": "ontouser_scope_create", "arguments": {"name": "trattoria_planning", "description": "Shift planning: shifts, requests, rules (managers only)"}},
  {"tool": "ontouser_scope_create", "arguments": {"name": "trattoria_team",     "description": "Shift planning: staff door (my shifts, requests, clocking)"}},

  {"tool": "ontouser_scope_index",  "arguments": {}},

  {"tool": "ontouser_scope_types",     "arguments": {"scope_id": "<master_scope_id>"}},
  {"tool": "ontouser_scope_types_set", "arguments": {"scope_id": "<master_scope_id>",
     "types": ["organisation", "building", "space", "person", "shiftTemplate", "file", "comment"]}},
  {"tool": "ontouser_scope_types",     "arguments": {"scope_id": "<planning_scope_id>"}},
  {"tool": "ontouser_scope_types_set", "arguments": {"scope_id": "<planning_scope_id>",
     "types": ["shift", "absence", "changeRequest", "demand", "serviceOrder", "file", "comment"]}},

  {"tool": "onto_type_show", "arguments": {"name": "shift",         "scope_id": "<planning_scope_id>", "limit": 1}},
  {"tool": "onto_type_show", "arguments": {"name": "changeRequest", "scope_id": "<planning_scope_id>", "limit": 1}},

  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<planning_scope_id>", "type_ids": ["<shift_type_id>"],
     "key": "actualEnd", "value_type": "datetime", "label": "Actual end"}},
  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<planning_scope_id>", "type_ids": ["<shift_type_id>"],
     "key": "actualBreakMinutes", "value_type": "int", "label": "Actual break (minutes)", "min_value": "0", "max_value": "600"}},
  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<planning_scope_id>", "type_ids": ["<shift_type_id>"],
     "key": "actualHours", "value_type": "float", "label": "Actual hours"}},
  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<planning_scope_id>", "type_ids": ["<shift_type_id>"],
     "key": "clockStatus", "value_type": "options", "label": "Clock status",
     "options": "[{\"value\":\"clockedIn\",\"label\":\"Clocked in\"},{\"value\":\"clockedOut\",\"label\":\"Clocked out\"},{\"value\":\"corrected\",\"label\":\"Corrected (manager)\"}]"}},
  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<planning_scope_id>", "type_ids": ["<shift_type_id>"],
     "key": "actualChangedBy", "value_type": "string", "label": "Actual time last changed by"}},
  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<planning_scope_id>", "type_ids": ["<shift_type_id>"],
     "key": "actualChangedAt", "value_type": "datetime", "label": "Actual time last changed at"}},
  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<planning_scope_id>", "type_ids": ["<shift_type_id>"],
     "key": "firstNoticeStatus", "value_type": "options", "label": "First notice", "default_value": "open",
     "options": "[{\"value\":\"open\",\"label\":\"Not yet notified\"},{\"value\":\"sent\",\"label\":\"Notified\"}]"}},
  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<planning_scope_id>", "type_ids": ["<changeRequest_type_id>"],
     "key": "requestKind", "value_type": "options", "label": "Request kind",
     "options": "[{\"value\":\"swap\",\"label\":\"Swap\"},{\"value\":\"takeover\",\"label\":\"Takeover\"},{\"value\":\"handover\",\"label\":\"Handover\"},{\"value\":\"shiftRequest\",\"label\":\"Shift request\"}]"}},

  {"tool": "onto_link_index", "arguments": {"limit": 200}},

  {"tool": "ontouser_team_index", "arguments": {}},
  {"tool": "ontouser_team_set_scope_rights", "arguments": {"profile_id": "<staff_profile_id>", "scope_id": "<master_scope_id>",
     "can_read": 1, "can_write": 0, "can_manage_scope": 0}},
  {"tool": "ontouser_team_set_scope_rights", "arguments": {"profile_id": "<staff_profile_id>", "scope_id": "<team_scope_id>",
     "can_read": 1, "can_write": 1, "can_manage_scope": 0}},
  {"tool": "ontouser_team_show", "arguments": {"profile_id": "<staff_profile_id>"}}
]
```

Notes on the example:
- `scope_id`, `profile_id` and `type_ids` are integers; they are quoted here only because they are placeholders.
- `options` is a **JSON string**, not an array.
- After the new keys in 1.5, create the **option overrides** of the table in 1.4
  ("Option overrides — the complete list"), one call per row, with the same pattern.
  Complete example for the shift station in planning and for the template station in
  master:

```json
[
  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<planning_scope_id>", "type_ids": ["<shift_type_id>"],
     "key": "station", "value_type": "options", "label": "Station",
     "options": "[{\"value\":\"kitchen\",\"label\":\"Kitchen\"},{\"value\":\"service\",\"label\":\"Service\"},{\"value\":\"bar\",\"label\":\"Bar\"},{\"value\":\"dishwashing\",\"label\":\"Dishwashing\"},{\"value\":\"shiftLead\",\"label\":\"Shift lead\"}]"}},
  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<master_scope_id>", "type_ids": ["<shiftTemplate_type_id>"],
     "key": "station", "value_type": "options", "label": "Station",
     "options": "<same JSON string>"}},
  {"tool": "onto_property_def_create", "arguments": {"scope_id": "<planning_scope_id>", "type_ids": ["<shift_type_id>"],
     "key": "shiftStatus", "value_type": "options", "label": "Shift status", "default_value": "open",
     "options": "[{\"value\":\"open\",\"label\":\"Open\"},{\"value\":\"planned\",\"label\":\"Planned\"},{\"value\":\"published\",\"label\":\"Published\"},{\"value\":\"swapped\",\"label\":\"Swapped\"},{\"value\":\"cancelled\",\"label\":\"Cancelled\"}]"}},
  {"tool": "onto_type_show", "arguments": {"name": "shift", "scope_id": "<planning_scope_id>", "limit": 1}}
]
```

  Labels follow the label language of intake 19 (German example labels:
  [country-de.md](country-de.md) §5).
- Staff rights are set only once a staff account exists (phase 3). In phase 0 you write
  the matrix down and set the rights of accounts that already exist. Staff: master =
  **read only**, planning = **no membership**, team = read+write. Shift lead (if any):
  planning = read+write, team = read+write, master = read (see matrix 1.2).
  Do **not** call `ontouser_team_set_scope_rights` for planning with all zeros "to be
  safe" on an account that has no membership there — it simply must not appear.
  Do **not** grant staff `can_read` on planning.
- If a call reports unknown parameters, read the allowed-parameter list and correct once.

---

## 3. Checks via MCP (smoke test)

Run after section 2. Every line must match; on any deviation stop and report
(SKILL.md, "Stop and escalate").

| # | Call | Expected |
|---|---|---|
| S1 | `GET https://mcp.telesherpa.com/health` (or, without raw HTTP, any read tool answering normally) | `status: ok` |
| S2 | `ontouser_scope_index` | three scopes with your names; you hold read, write and manage on each |
| S3 | `ontouser_scope_types` (master, planning, team) | enabled exactly for the phase-appropriate types in 1.3; add interim `person` in planning in phase 4; `changeRequest` may be missing from the selection list (1.3) |
| S4 | `onto_type_show` `shift` with planning scope | the platform keys of 1.4 **plus** the seven shift keys of 1.5 |
| S5 | `onto_type_show` `shift` with team scope | the platform keys **without** the seven new shift keys (proves they are scope-specific) |
| S6 | `onto_type_show` `changeRequest` with planning scope | `requestKind` with `swap`, `takeover`, `handover`, `shiftRequest` |
| S7 | `onto_type_show` `shift`, `absence`, `demand` with planning scope; `shiftTemplate` with master scope | every option field of the override table in 1.4 shows exactly the English values and defaults listed there |
| S8 | `onto_link_index` | `worksShift` person → shift; `bestehtAus`, `derivedFrom`, `concerns`, `hasfile` present |
| S9 | `onto_credit_balance` | spend so far ≈ 260 (100 + 80 + 80) + reads; log it |
| S10 | `ontouser_team_show` (each existing managed account) | memberships exactly as in matrix 1.2; staff = master **read**, **no** planning membership, team read+write |
| S11 | Browser as staff (once an account exists): open team "my …" views; try a manager/planning view URL | team views show **only own** rows; direct open of a manager view is **refused** |

## 4. Checks in the browser

| Role | Check | Expected |
|---|---|---|
| manager | log in, open each scope's object list | three scopes visible, empty |
| staff (if an account exists already) | log in | team scope writable; master readable (basic); **no** planning membership; team views show only own rows (documented `person` or `passt` binding); opening a manager/payroll view is refused; no write buttons that require planning write; protected fields (pay, health, private contacts) not visible on master persons |

## 5. Acceptance

- [ ] S1–S11 pass and are logged with timestamps
- [ ] rights matrix written in the run log for every account, including "no grant"
- [ ] intake stations recorded as scope-own English option values (section 1.4)
- [ ] spend logged against budget

## 6. Typical errors

| Symptom | Cause | Fix |
|---|---|---|
| `ontouser_scope_create` refused | name has upper case, `-` or is longer than 30 characters | use `a-z0-9_` |
| HTTP 402 on scope creation | not enough credits for the **next** scope — the number of scopes is **not** limited | stop; top up. Do not retry, do not shrink the plan |
| a type disappears from the dialog | `ontouser_scope_types_set` replaced the list | always send the full list |
| `types_set` refuses to remove a type | objects of that type still exist in the scope | leave it active |
| new property not visible on shift | created without `scope_id`, or `type_ids` wrong | read `type.id` again; recreate with `scope_id` |
| options field stays empty | `options` passed as array instead of JSON string | pass a string |
| rights call 403 | account is not managed by your scope, or manage on the managing scope requested | see company-manager reference |
| staff sees colleagues' shifts in a team view | person binding missing or wrong, or planning read granted | fix the `person` block (phase 3 §7) and the `linked_to_user` guard; remove planning membership; do **not** grant planning read |
| staff can open a manager view or a foreign planning object | planning membership granted by mistake, or manager view missing `access.require` | remove planning membership; set `view_config.access.require` on every manager view |

## 7. Cost and language

**Definition calls are not charged.** Creating or changing types, properties, link
types, actions, views, triggers and start cards books no credits. The platform charges
scope creation, object reads and writes, stored files and completed form answers. The
build itself is therefore cheap; what costs money is the staffed test week.

**Property labels are plain strings.** The platform renders a label exactly as stored
in your scope — only the platform's own interface text is translated. Write labels in
the language your staff reads (intake 19): one workspace, one label language. Option
values are plain strings as well (1.4).
