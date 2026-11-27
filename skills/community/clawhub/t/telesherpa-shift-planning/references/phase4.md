# Phase 4 — time tracking, change log, protected staff data, payroll preparation

**Goal:** staff clock in and out **on their own shift only** through the team door
(scope bridge into planning), enter their break as its own field, managers correct
actual times with a required reason and an old → new entry in the change log, and
managers export planned vs. actual hours per person and month as a **generic CSV**
with a minijob warning. Pay and private data live in a manager-only **staff record**
in planning — never on the staff-readable master person.

**Input:** phases 0–3 passed; intake questions 10, 14, 17 and the country module
([country-de.md](country-de.md) for Germany).

**Budget (pay-per-use):** each clock-in and clock-out is an action run (20 credits)
paid by the **staff account**; corrections and record changes are paid by the
manager. Triggers and the function run of the actual-hours rule cost no credits. The
payroll view is a read.

**Platform references:**
[scope-bridges.md](../../../telesherpa-ontology-platform/references/features/scope-bridges.md) (bridge, guard, person binding) ·
[automation-and-functions.md](../../../telesherpa-ontology-platform/references/features/automation-and-functions.md) (`hours_between`, triggers) ·
[member-agent-rules.md](../../../telesherpa-ontology-platform/references/features/member-agent-rules.md) (`access.require`, `{old:…}`/`{new:…}`) ·
[scopes-and-permissions.md](../../../telesherpa-ontology-platform/references/features/scopes-and-permissions.md) (who reads what) ·
[tool-traps.md](../../../telesherpa-ontology-platform/references/features/tool-traps.md) (prices, time zones).

Placeholders as in [phase1.md](phase1.md); `<record_type_id>` = type id of the staff
record (see 1.2). View block keywords as in phase 1.

---

## 1. Objects, properties, options

### 1.1 Shift — actual time fields (created in phase 0)

| Key | Type | Values | Set by |
|---|---|---|---|
| `actualStart` | datetime | | `sp_clock_in`, `sp_actual_correct` |
| `actualEnd` | datetime | | `sp_clock_out`, `sp_actual_correct` |
| `actualBreakMinutes` | int | min 0, max 600 | `sp_clock_out`, `sp_actual_correct` — **own field**, never inside a comment text |
| `actualHours` | float | | function `sp_actual_hours` (trigger) |
| `clockStatus` | options | `clockedIn`, `clockedOut`, `corrected` | clock and correction actions |
| `actualChangedBy` | string | e-mail of the last writer | all three actions (`{user_email}`) |
| `actualChangedAt` | datetime | | all three actions (`{now}`) |

The **planned** break stays in `breakMinutes` (phase 1); planned and actual are never
mixed. Reads are UTC (plus `_local` for the viewer's zone); writes without a zone are read
in the viewer's zone, so send `Z`/an offset.

### 1.2 Decision: where protected data lives

> **Confirmed and still open.** No dedicated staff-record type was present in the
> available type catalogue. Interim `person` records in planning, table scope narrowing,
> linked pay fields, `nur`/filter on the linked contract field, cross-scope creation
> with the binding in §7, and the corrected eight-field CSV were tested. A colleague's
> record and the payroll view stayed closed to staff. Now available on the platform
> and built into this phase: a contract condition on the warning column
> (`bedingung`, §6.3), a year-dependent threshold key (`schwelle_ab_2027`, switching
> by the current date, §6.3), a clean refusal of a denied CSV export (redirect to the
> overview with a notice; JSON requests get 403), and a person-binding guard on the
> absence form (phase 2 §3.1). Comments can be deleted by their author or by a writer
> of the comment's scope (§4). Still open: own-record access and scope narrowing of
> matrix rows. Verify the new items in your own workspace (§8, §12) before relying
> on them.

Phase 1 left this open. **Decision:** pay and private data live on a **staff record**
in the **planning** scope — one record per person, readable and writable only by
managers (planning membership), linked to the master person.

| Field on the staff record | Type | Note |
|---|---|---|
| `contractType` | options `minijob`, `partTime`, `fullTime`, `fixedTerm`, `casual` | interpret the earnings warning only for `minijob` rows |
| `hourlyRate` | float (EUR) | |
| `phone` | string | private phone |
| `street`, `postalCode`, `city` | string | private address |
| `notes` | text | no health data, no diagnosis |
| link `concerns` / `staffRecordOf` → master person | | exactly one per person |

Rules:
- The staff record carries **no `email`**. Person-bound team views select by e-mail
  and therefore never hit a record.
- **Own record through the person link.** The record hangs on the master person with
  `concerns`, like an absence. The person link may therefore let the staff member
  open their **own** record by URL (worth confirming with a staff account). Seeing the own
  rate and address is usually acceptable; a colleague's record must stay closed.
  If the business wants the own record closed too, link it with a link type that is
  not `concerns` (confirm which link types open an object for the person).
- **Shift leads see and change pay.** Everyone with planning write — shift leads
  included (phase 0) — can read the staff records and the payroll view and can also
  change the records (hourly rate, contract type). This is the default of this skill;
  there is no extra gate. Mention it to the business in intake question 9. If they want pay hidden from shift leads, move the
  staff records into a separate scope that shift leads cannot read and give the
  payroll view `access.require` on that scope (confirm in the workspace before
  relying on it).
- The master person keeps only basic fields (phase 1). Remove `contractType`,
  `hourlyRate`, `phone` and address from master persons and from every master view
  and form.
- **Record type:** a dedicated object type ("staff record") is preferred; request it
  through `ontouser_service_request` (confirm: availability). **Interim:** use the
  type `person` in the planning scope (add `person` to the planning types with
  `ontouser_scope_types_set`), name it `Record <first name> <last name>`. Then narrow
  every person-based **table** to master with `"scopes": ["<company>_master"]`
  in its `table` block (staff list, next shift per person, and `sp_my_next_shift`).
  This applies to `table` blocks. The week grid uses `matrix.rows`, not `table`:
  a `scopes` key in the table block does not narrow the grid. Keep the grid's rows
  filtered by person binding and check that staff records do not appear as extra rows.
- Contract type and hourly rate never sit on the master person (data minimisation,
  [country-de.md](country-de.md) §3).

## 2. Links

| Link | Direction | Use |
|---|---|---|
| `worksShift` | person → shift | guard of the clock actions; payroll sums |
| `concerns` / `staffRecordOf` | staff record → master person | protected data of the person |

## 3. Forms

None required. Optional: a monthly summary on the person via form calc fields
(`count_of` / `sum_of` over a `linklist` with `wo`) — not needed for the export (to
verify: calc fields with a month parameter).

## 4. Actions

### 4.1 `sp_clock_in` — staff, own shift, bridge team → planning

```json
{"tool": "onto_actiondef_save", "arguments": {"key": "sp_clock_in", "label": "Clock in",
  "description": "Staff clocks in on their own shift (guard worksShift). Bridge into planning: actualStart = now, clockStatus = clockedIn, changed by/at; change-log comment with optional note. Once per shift, not on open or cancelled shifts.",
  "body": {"object_types": ["shift"], "scopes": [<planning_scope_id>, <team_scope_id>], "roles": ["member"],
    "guards": [{"type": "linked_to_user", "linktype": "worksShift", "message": "Only your own shift"}],
    "condition": {"props": [{"key": "shiftStatus", "op": "ne", "value": "open"},
                            {"key": "shiftStatus", "op": "ne", "value": "cancelled"},
                            {"key": "actualStart", "op": "empty"}],
                  "message": "Clock in only on a staffed shift and only once (already clocked in? Use 'Clock out')"},
    "prompts": [{"key": "note", "label": "Note (optional)", "type": "text", "required": false, "persist": false, "default": "no note"}],
    "action": {"type": "update", "result_scope_id": <planning_scope_id>,
      "props": {"actualStart": "{now}", "clockStatus": "clockedIn", "actualChangedBy": "{user_email}", "actualChangedAt": "{now}"},
      "effects": [{"type": "comment", "text": "Clocked in {now} by {user_email} – note: {note}"}]}}}}
```

- **Bridge:** `result_scope_id` sits inside `action`; only the keys in `action.props`
  are written into planning. The guard is the person binding (`linked_to_user` on
  `worksShift` = the caller's master person is on the shift).
- The optional prompt is required in practice: a prompt-less action opens no dialog
  in a team view.
- Keep `actualStart` first in this recipe. End-only and break-only corrections
  were nevertheless confirmed to recalculate hours; do not infer a missed update
  solely from property order.
- **No clock-in window is enforced.** Early clock-in, even for a future shift, is
  possible. A `{now}` comparison in a condition is not a verified solution. Managers
  must review differences between planned and actual times before payroll.

### 4.2 `sp_clock_out` — staff, own shift

```json
{"tool": "onto_actiondef_save", "arguments": {"key": "sp_clock_out", "label": "Clock out",
  "description": "Staff clocks out on their own shift (guard worksShift). Bridge into planning: actualEnd = now, actualBreakMinutes from the prompt, clockStatus = clockedOut, changed by/at; change-log comment. Actual hours are computed by the trigger.",
  "body": {"object_types": ["shift"], "scopes": [<planning_scope_id>, <team_scope_id>], "roles": ["member"],
    "guards": [{"type": "linked_to_user", "linktype": "worksShift", "message": "Only your own shift"}],
    "condition": {"props": [{"key": "clockStatus", "op": "eq", "value": "clockedIn"}],
                  "message": "Clock out only after clocking in (and only once)"},
    "prompts": [{"key": "break", "label": "Break in minutes (total, 0 if none)", "type": "int", "required": true, "default": "0", "persist": false}],
    "action": {"type": "update", "result_scope_id": <planning_scope_id>,
      "props": {"actualEnd": "{now}", "actualBreakMinutes": "{break}", "clockStatus": "clockedOut", "actualChangedBy": "{user_email}", "actualChangedAt": "{now}"},
      "effects": [{"type": "comment", "text": "Clocked out {now} by {user_email}, break {break} min."}]}}}}
```

`actualEnd` is the first prop: the actual-hours trigger listens for it.

### 4.3 `sp_actual_correct` — manager correction

```json
{"tool": "onto_actiondef_save", "arguments": {"key": "sp_actual_correct", "label": "Correct actual time (manager)",
  "description": "Manager corrects actual start, end and break of a shift. Reason required; the change log shows old → new per field.",
  "body": {"object_types": ["shift"], "scopes": [<planning_scope_id>], "roles": ["member"],
    "prompts": [
      {"key": "start", "label": "Actual start (YYYY-MM-DD HH:MM)", "type": "datetime", "required": true, "persist": false},
      {"key": "end", "label": "Actual end (YYYY-MM-DD HH:MM)", "type": "datetime", "required": true, "persist": false},
      {"key": "break", "label": "Actual break in minutes", "type": "int", "required": true, "default": "0", "persist": false},
      {"key": "reason", "label": "Reason for the correction (required, goes into the log)", "type": "text", "required": true, "persist": false}],
    "action": {"type": "update", "require_scope_write": <planning_scope_id>,
      "props": {"actualStart": "{start}", "actualEnd": "{end}", "actualBreakMinutes": "{break}", "clockStatus": "corrected", "actualChangedBy": "{user_email}", "actualChangedAt": "{now}"},
      "effects": [{"type": "comment", "text": "Actual time corrected {now} by {user_email}: start {old:actualStart} → {new:actualStart}, end {old:actualEnd} → {new:actualEnd}, break {old:actualBreakMinutes} → {new:actualBreakMinutes} min. – reason: {reason}"}]}}}}
```

- `require_scope_write` refuses execution without planning write. A button may
  still be visible; visibility alone does not prove permission to execute it.
- Correction also covers "forgot to clock in/out": the manager enters both times.
- `{old:…}` shows an empty value when the field was empty; datetimes appear with
  seconds (cosmetic).

### 4.4 Change log

The change log of a shift is the sum of:

1. **Comments** written by the three actions (author, time, old → new, reason/note) —
   visible on the shift detail (`panels` → `comments`) for managers;
2. `actualChangedBy` / `actualChangedAt` — last writer at a glance;
3. the platform's object history (who changed which field when).

**Operating rule:** never edit or delete these comments; correct mistakes with a
new reason. Comments are technically deletable, so this is **not an immutable audit
log**. A comment can be deleted by its author or by a scope member with write access to the
comment's scope; nobody else can delete another person's comment.
Keep write access to the planning scope with managers only. Keep periodic payroll
exports as supporting evidence and restrict access; apply retention from the country
module. An export alone does not make the workspace history tamper-proof.

## 5. Functions and triggers

```json
{"tool": "onto_function_create", "arguments": {"scope_id": <planning_scope_id>, "key": "sp_actual_hours", "name": "Actual hours of a shift", "label": "Actual hours (end − start − break)",
  "description": "hours_between(actualStart, actualEnd, actualBreakMinutes) → actualHours.",
  "body": {"inputs": [{"key": "object", "type": "object", "required": true}],
           "body": {"hours_between": [{"field": ["actualStart"]}, {"field": ["actualEnd"]}, {"field": ["actualBreakMinutes"]}]},
           "effects": [{"type": "set_property", "props": {"actualHours": "{result}"}}],
           "timeout_ms": 3000, "scopes": [<planning_scope_id>]}}}
```

```json
{"tool": "onto_trigger_create", "arguments": {"scope_id": <planning_scope_id>, "key": "sp_actual_hours_update", "name": "Actual hours on change",
  "body": {"on": "insert,update", "object_types": ["shift"], "enabled": true,
    "condition": {"changed": ["actualStart", "actualEnd", "actualBreakMinutes"],
                  "props": [{"key": "actualStart", "op": "notempty"}, {"key": "actualEnd", "op": "notempty"}]},
    "effects": [{"type": "run_function", "function": "sp_actual_hours", "inputs": {"object": "{object_udid}"}}]}}}
```

Asynchronous: `actualHours` appears 1–5 minutes after clock-out or correction. A
shift that ends after midnight is handled by `hours_between` (confirmed: 18:00–01:00
with a 30-minute break gives 6.5 hours). End-only and break-only corrections were
confirmed to recalculate the result without changing the start.

No notification in this phase. Optional manager hint "clocked in but not out after
the shift end" as a scheduled rule writing a `planNote` (confirm).

## 6. Views

### 6.1 Staff (team scope)

Clock in / Clock out appear as row buttons in "My shifts" ([phase3.md](phase3.md)
§7.2). Each button still checks guard and condition; a click on a colleague's shift is
refused with "Only your own shift".

### 6.2 `sp_actual_times` — manager check of a week (planning)

The block view was tested; use an explicit datetime format on both actual-time
fields so that human-facing values are local rather than raw UTC. Recheck the
formatted rendering in the customer workspace. The week period uses
`param`/`span` with a `zeitraum` on the day column:

```json
{"elements": ["filter", "table"],
 "table": {"from": "objects", "type": "shift", "status": "active", "param": "woche", "span": 7,
  "zeitraum": {"key": "day", "von": "{period_start}", "bis": "{period_end}"},
  "columns": [
    {"key": "udid", "system": "udid", "hidden": true},
    {"key": "day", "prop": "shiftStart", "format": "wochentag_datum", "label": "Day"},
    {"key": "planned", "prop": "shiftStart", "bis": "shiftEnd", "format": "zeitspanne", "label": "Planned"},
    {"key": "staff", "link": "worksShift", "richtung": "rueckwaerts", "type": "person", "system": "name", "label": "Staff"},
    {"key": "actualStart", "prop": "actualStart", "format": "wochentag_datum_zeit", "label": "Actual start"},
    {"key": "actualEnd", "prop": "actualEnd", "format": "wochentag_datum_zeit", "label": "Actual end"},
    {"key": "actualBreak", "prop": "actualBreakMinutes", "format": "zahl", "label": "Break (min)"},
    {"key": "actualHours", "prop": "actualHours", "format": "zahl", "stellen": 2, "label": "Actual hours"},
    {"key": "clock", "prop": "clockStatus", "label": "Clock status", "werte": {"clockedIn": "clocked in", "clockedOut": "clocked out", "corrected": "corrected"}}],
  "filter": ["clock"],
  "sort": {"key": "day", "dir": "asc"},
  "row_actions": [{"action": "sp_actual_correct", "label": "Correct"}]},
 "access": {"require": "write"}}
```

### 6.3 `sp_payroll_prep` — payroll preparation (planning read, shift leads included)

Rows: master persons with a staff record. Columns in export order. The **CSV header
uses the column labels**, so the labels of the five required columns are the generic
names.

```json
{
  "elements": [
    "filter",
    "table"
  ],
  "table": {
    "from": "objects",
    "type": "person",
    "scopes": [
      "<company>_master"
    ],
    "links": {
      "record": {
        "link": "concerns",
        "richtung": "rueckwaerts",
        "linkvalue": "staffRecordOf",
        "type": "person"
      }
    },
    "columns": [
      {
        "key": "person",
        "system": "name",
        "label": "person"
      },
      {
        "key": "month",
        "format": "monat",
        "label": "month"
      },
      {
        "key": "contractType",
        "link": "record",
        "prop": "contractType",
        "label": "contractType",
        "werte": {
          "minijob": "minijob",
          "partTime": "partTime",
          "fullTime": "fullTime",
          "fixedTerm": "fixedTerm",
          "casual": "casual"
        }
      },
      {
        "key": "hourlyRate",
        "link": "record",
        "prop": "hourlyRate",
        "format": "waehrung",
        "label": "hourlyRate"
      },
      {
        "key": "shiftsInMonth",
        "agg": "count",
        "link": "worksShift",
        "richtung": "vorwaerts",
        "label": "shiftsInMonth",
        "ziel": {
          "wo": [
            {
              "prop": "shiftStart",
              "op": ">=",
              "wert": "{monat_start}"
            },
            {
              "prop": "shiftStart",
              "op": "<",
              "wert": "{monat_ende}"
            },
            {
              "prop": "shiftStatus",
              "op": "!=",
              "wert": "cancelled"
            }
          ]
        }
      },
      {
        "key": "plannedHours",
        "agg": "sum",
        "link": "worksShift",
        "richtung": "vorwaerts",
        "prop": "plannedHours",
        "format": "zahl",
        "stellen": 2,
        "label": "plannedHours",
        "ziel": {
          "wo": [
            {
              "prop": "shiftStart",
              "op": ">=",
              "wert": "{monat_start}"
            },
            {
              "prop": "shiftStart",
              "op": "<",
              "wert": "{monat_ende}"
            },
            {
              "prop": "shiftStatus",
              "op": "!=",
              "wert": "cancelled"
            }
          ]
        }
      },
      {
        "key": "actualHours",
        "agg": "sum",
        "link": "worksShift",
        "richtung": "vorwaerts",
        "prop": "actualHours",
        "format": "zahl",
        "stellen": 2,
        "label": "actualHours",
        "ziel": {
          "wo": [
            {
              "prop": "shiftStart",
              "op": ">=",
              "wert": "{monat_start}"
            },
            {
              "prop": "shiftStart",
              "op": "<",
              "wert": "{monat_ende}"
            },
            {
              "prop": "shiftStatus",
              "op": "!=",
              "wert": "cancelled"
            }
          ]
        }
      },
      {
        "key": "miniJobWarning",
        "format": "warnung",
        "wert": "actualHours",
        "stundenlohn": "hourlyRate",
        "schwelle": <monthly limit from the country module for the current year>,
        "schwelle_ab_2027": <monthly limit from 1 January 2027, country module>,
        "bedingung": [{"spalte": "contractType", "op": "=", "wert": "minijob"}],
        "text": "YES, {betrag} EUR – check with payroll",
        "label": "miniJobWarning"
      }
    ],
    "filter": [
      "contractType"
    ],
    "nur": [
      "contractType"
    ],
    "sort": {
      "key": "person",
      "dir": "asc"
    }
  },
  "access": {
    "require": <planning_scope_id>
  }
}
```

```json
{"tool": "onto_interface_create_def", "arguments": {"name": "sp_payroll_prep", "label": "Payroll preparation (planned/actual per person)",
  "scope_id": <planning_scope_id>, "roles": ["member"], "object_type_ids": [<person_type_id>],
  "description": "Per person and month: planned and actual hours of their shifts (cancelled excluded), minijob warning (actual × hourly rate above the country limit). Month via ?monat=YYYY-MM, default current month. Everyone with planning read.",
  "view_config": "<JSON string above>"}}
```

- **Month:** `?monat=YYYY-MM`; without parameter the current month. `{monat_start}` /
  `{monat_ende}` are the month bounds; `month` shows the selected month.
- **CSV:** `ontouser/interface/export/sp_payroll_prep?monat=YYYY-MM`. Header = labels
  in the actual column order:
  `person;month;contractType;hourlyRate;shiftsInMonth;plannedHours;actualHours;miniJobWarning`.
  `hourlyRate` must precede `miniJobWarning`; the warning requires an earlier wage
  column. The linked rate is required for this warning, even if other extra fields
  are omitted. Header labels and the corrected eight-field export were confirmed.
  Separator, decimal mark, encoding and line endings follow the country module.
- **Threshold:** `schwelle` is the limit up to 31 December 2026, `schwelle_ab_2027`
  the limit from 1 January 2027 (values from the country module). **Caveat:** the
  year is taken from the **current date when the view is rendered**, not from the
  selected month. A month of 2027 viewed in 2026 is still checked against
  `schwelle`; a December export produced in January is checked against
  `schwelle_ab_2027`. Prepare each month's payroll within that month's year, or
  check rows close to the limit by hand against the limit of their own month. Later
  limit changes still need a manual update of the view.
- **Contract condition:** `bedingung` restricts the warning to rows whose other
  column matches: `[{"spalte": "<column key>", "op": "=", "wert": "<stored value>"}]`.
  `spalte` names the **column key of this view** (here `contractType`), `wert` the
  stored option value (`minijob`). Several entries are combined with AND; operators
  `= != > < >= <=`. Without `bedingung` the warning applies to every row. If the
  named column is missing, the warning stays empty (fail-closed), so a typo hides all
  warnings: test with one minijob row above the limit and one non-minijob row above
  it (P4-13).
- `nur: ["contractType"]`, the contract filter and `stundenlohn` referencing the
  earlier linked `hourlyRate` column were confirmed with staff-record test data.
- Name without a month: one view for all months.

## 7. Recipe (tool order with example arguments)

```json
[
  {"tool": "ontouser_scope_types_set", "arguments": {"scope_id": <planning_scope_id>, "types": ["...phase 0 list...", "person"]}},
  {"tool": "onto_property_def_create", "arguments": {"scope_id": <planning_scope_id>, "type_ids": [<record_type_id>], "key": "contractType", "value_type": "options", "label": "Contract type",
     "options": "[{\"value\":\"minijob\",\"label\":\"Minijob\"},{\"value\":\"partTime\",\"label\":\"Part-time\"},{\"value\":\"fullTime\",\"label\":\"Full-time\"},{\"value\":\"fixedTerm\",\"label\":\"Fixed-term\"},{\"value\":\"casual\",\"label\":\"Casual\"}]"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_staff_record_create", "label": "Create staff record (manager)",
     "body": {"object_types": ["person"], "scopes": [<master_scope_id>], "roles": ["member"],
       "prompts": [
         {"key": "recordName", "label": "Staff record name", "type": "text", "required": true, "persist": false},
         {"key": "contract", "label": "Contract type", "type": "select", "required": true, "persist": false, "options": ["minijob", "partTime", "fullTime", "fixedTerm", "casual"]},
         {"key": "rate", "label": "Hourly rate (EUR)", "type": "float", "required": true, "persist": false},
         {"key": "phone", "label": "Private phone", "type": "text", "required": false, "persist": false, "default": "-"}],
       "action": {"type": "create", "object_type": "person", "result_scope_id": <planning_scope_id>, "require_scope_write": <planning_scope_id>,
         "name": "{recordName}", "status": "active",
         "props": {"contractType": "{contract}", "hourlyRate": "{rate}", "phone": "{phone}", "description": "Created by {current_user_email}"},
         "links": [{"type": "concerns", "to": "{object_udid}", "linkvalue": "staffRecordOf"}]}}}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_clock_in", "...": "see 4.1"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_clock_out", "...": "see 4.2"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_actual_correct", "...": "see 4.3"}},
  {"tool": "onto_function_create", "arguments": {"key": "sp_actual_hours", "...": "see 5"}},
  {"tool": "onto_trigger_create", "arguments": {"key": "sp_actual_hours_update", "...": "see 5"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_actual_times", "...": "see 6.2"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_payroll_prep", "...": "see 6.3"}},
  {"tool": "onto_interface_show", "arguments": {"name": "sp_payroll_prep"}}
]
```

- `sp_staff_record_create` runs on the master person and writes into planning; the
  cross-scope create path was confirmed with `result_scope_id`, the gate inside
  `action`, and the actor binding in `action.props.description` using
  `{current_user_email}`; `{user_email}` is accepted as the binding as well.
  `{object_name}` is **not available in action names**: the new object does not exist
  yet when the name is set, so the placeholder would stay literal. Enter the record
  name explicitly through a prompt such as `recordName`. Check that no record exists
  for the person before creating one: no duplicate guard is provided. A record editor
  `sp_staff_record_update` (update on the record, planning, gate) follows the same
  pattern.
- The planning types list must be the full list (set, not add).

## 8. Smoke tests

| # | Call / check | Expected |
|---|---|---|
| P4-1 | staff: `sp_clock_in` on own published shift | `actualStart` set, `clockStatus = clockedIn`, comment with author; staff balance −20 |
| P4-2 | staff: `sp_clock_in` again on the same shift | refused with the condition message |
| P4-3 | staff: `sp_clock_in` on a colleague's shift | refused: "Only your own shift" |
| P4-4 | staff: `sp_clock_in` on an open or cancelled shift | refused |
| P4-5 | staff: `sp_clock_out` with break 30 | `actualEnd`, `actualBreakMinutes = 30`, `clockedOut`; after ≤ 5 min `actualHours` = (end − start − 30 min) in hours |
| P4-6 | staff: `sp_clock_out` without clock-in | refused |
| P4-7 | staff: `sp_actual_correct` | button absent; direct run execution refused (gate; the button may still be visible) |
| P4-8 | manager: `sp_actual_correct` with reason; repeat once changing **only end**, then once changing **only break**, keeping all other time inputs identical | `clockStatus = corrected`; comment shows old → new and reason; `actualHours` recomputed after each correction without a manual function run |
| P4-9 | manager: `sp_actual_correct` without reason | refused (required prompt) |
| P4-10 | `onto_object_show` master person | no `contractType`, `hourlyRate`, private phone or address |
| P4-11 | `onto_object_show` staff record | protected fields present; link `staffRecordOf` → master person |
| P4-12 | `onto_interface_show sp_payroll_prep` | planning scope, `access.require` planning, definition uses blocks only |
| P4-13 | browser `sp_payroll_prep?monat=YYYY-MM` for the test month | expected sums of the acceptance scenario; warning only on `minijob` rows above the limit; a non-minijob row above the limit shows no warning (`bedingung`) |
| P4-14 | CSV export | header `person;month;contractType;hourlyRate;shiftsInMonth;plannedHours;actualHours;miniJobWarning`; conventions from the country module |
| P4-15 | staff: payroll view or CSV URL | refused: redirect to the overview with a notice, no file |
| P4-16 | an account that is neither author nor planning writer deletes a change-log comment | refused |

## 9. Browser checks

| Role | Check | Expected |
|---|---|---|
| staff | "My shifts" → Clock in on own shift → note | dialog opens, value saved, button now "Clock out" |
| staff | Clock out → break 30 | saved; actual hours appear within minutes |
| staff | Clock in on a colleague's shift (button or URL) | "Only your own shift" |
| staff | open payroll, actual-times view, a staff record | refused |
| manager | shift detail → Correct | dialog with four fields; comment in the change log |
| manager | payroll view, month switch, CSV download | values match; CSV opens in a spreadsheet with correct umlauts and decimals |

## 10. Failure patterns

| Symptom | Cause | Fix |
|---|---|---|
| staff click on Clock in does nothing | prompt-less action, or no credits (402) | add the optional prompt; top up the staff account |
| "not permitted" for staff on own shift | bridge missing (`result_scope_id` not inside `action`), or staff has no `worksShift` link | fix the body; staff the shift |
| clock-in writes, but into the wrong scope | `result_scope_id` outside `action` | move it inside `action` |
| `actualHours` empty | trigger missing `actualEnd` in `changed`; or function not in planning | fix trigger/function; wait 5 min |
| `actualHours` never recalculated after correction | trigger, function or required actual time missing | inspect the definition and values, wait for the trigger, test end-only and break-only changes |
| times off by one or two hours | a naive local time was read in the viewer's zone and stored as UTC, or a value was hand-converted | send `Z`/an offset; compare against the `_local` field, never against a hand-converted value |
| payroll counts cancelled shifts | `ziel.wo` without the status filter | add `shiftStatus != cancelled` |
| payroll lists record rows twice | `person` base set without `scopes` narrowing | add `"scopes": ["<company>_master"]` |
| CSV header translated / wrong | labels used as header | set the labels to the generic field names in the documented eight-field order |
| minijob warning empty on every row | `bedingung` names a missing column key or a display label instead of the stored value | use the column key and the stored option value |
| minijob warning on part-time rows | `bedingung` missing | add it (§6.3) |
| month near the limit warned with the wrong year's limit | threshold year follows the current date, not the month | prepare payroll within the month's year or check by hand (§6.3) |
| staff sees hourly rate | protected fields still on the master person | move to the staff record (1.2) |

## 11. Phase 5 — later / out of scope

Not part of this skill: DATEV or other payroll-system formats (DATEV is an outlook
only), payroll calculation, surcharges and public holidays, multiple sites with shared
staff, automated plan generation beyond the agent planning loop, and any device-based
time clock. They need their own skill and a separate intake.

## 12. Boundaries of this skill

- **Staff records live on `person`.** Narrow the master table to your own scope, and
  keep the row label (`lastName`) mandatory — a row without it has no label.
- **The warning column works with `bedingung`.** Prove it once with one minijob row
  and one non-minijob row above the limit (P4-13).
- **`schwelle_ab_2027` follows the current date, not the selected month** (§6.3).
  Until 1 January 2027 the `schwelle` value applies.
- **CSV header and order follow the country module** and use the customer's language
  setting. A denied export shows a notice instead of a blank page (P4-15).
- **Cross-midnight hours, end-only and break-only corrections are supported.**
- **Create across scopes with the person binding of §7** (`{current_user_email}` or
  `{user_email}`). `{object_name}` is not available in action names — ask for the name.
- **A staff member reaches their own staff record** through the person link; a
  colleague's record is refused. Comments may be deleted by the author or a scope
  writer (§4).
