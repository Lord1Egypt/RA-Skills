# Phase 2 — requests through the team door, decisions in planning, staff detail

**Goal:** staff file their requests from the team door — swap, takeover and handover
of their own shift, a request for an open shift (all as `changeRequest` with
`requestKind`), and absences including a **day-off wish** (as `absence` with
`absenceKind`). The objects land in the planning scope. Managers decide in one request
inbox whose row buttons depend on `requestKind`; an approved swap moves the
`worksShift` links exactly. Managers also get a staff list and a staff detail page
built from blocks with subforms.

**Input:** phase 1 passed (P1-1 … P1-16), intake questions 14 (which requests, who
decides) and 12 (qualification documents). Staff rights stay as in phase 0 (master
**R**, planning **no membership**, team **RW**). Staff reach a planning object only
through the person link (their shift via `worksShift`, their absence or request via
`concerns`); the requests they create are linked to them at creation, so they can
see them afterwards in "My requests" (phase 3).

**Budget (pay-per-use):** each request is one action run by the staff account (20
credits from *their* balance) plus the created object; each decision is one action run
by the manager (20). A test set of six requests with decisions costs about
6 × (20 + 10 + 20) = 300 credits plus reads. Links, comment effects and link moves
are not in this figure: a request with four links adds about 20, a swap decision that
moves two links (remove 20 + create 5 each) about 50 — see the cost table in
[measurement.md](measurement.md) §3 (estimates; your statement is the truth).

Placeholders (in addition to phases 0–1): `<absence_form_udid>`,
`<qualification_form_udid>`, `<request_udid>`, `<absence_udid>`,
`<changeRequest_type_id>`, `<absence_type_id>`.

**Platform references:**
[scope-bridges.md](../../../telesherpa-ontology-platform/references/features/scope-bridges.md) (`result_scope_id`, guards, person binding) ·
[form-engine.md](../../../telesherpa-ontology-platform/references/features/form-engine.md) (forms, `form_answer`) ·
[member-agent-rules.md](../../../telesherpa-ontology-platform/references/features/member-agent-rules.md) (placeholders, `access.require`) ·
[notifications-and-link-events.md](../../../telesherpa-ontology-platform/references/features/notifications-and-link-events.md) (decision messages, phase 3) ·
[tool-traps.md](../../../telesherpa-ontology-platform/references/features/tool-traps.md) (credits of staff accounts, async triggers).

View block fields (`richtung`, `werte`, `wo`, `via`, `objekt`, `dateien`, …) are
platform keywords; see the vocabulary note in [phase1.md](phase1.md). Every view and
subform in this file is built from blocks; where a wanted effect is not yet proven
with blocks it says "(confirm: block-only equivalent)".

---

## 1. Objects, properties, options

### 1.1 Objects of this phase

| Object | Type | Created in | Created by | Name |
|---|---|---|---|---|
| swap request | `changeRequest`, `requestKind = swap` | planning | staff, `sp_swap_request` on own shift | `Swap request {now}` |
| takeover request | `changeRequest`, `requestKind = takeover` | planning | staff, `sp_takeover_request` | `Takeover request {now}` |
| handover request | `changeRequest`, `requestKind = handover` | planning | staff, `sp_handover_request` | `Handover request {now}` |
| shift request | `changeRequest`, `requestKind = shiftRequest` | planning | staff, `sp_shift_request` on an open shift | `Shift request {now}` |
| absence / day-off wish | `absence` (`absenceKind`) | planning | staff, `sp_absence_request` (form) on own person | `Absence {now}` |
| qualification certificate | `file` | planning | manager, `sp_qualification_upload` (form) on a person | `Certificate {now}` |
| manager note | `serviceOrder`, `task = planNote` | planning | precheck on absence approval | `Note: shift {name} released – person absent` |

Meaning of the four request kinds:

| `requestKind` | Who asks | About | Partner | Decision moves |
|---|---|---|---|---|
| `swap` | person on the shift | own shift ↔ partner's counter shift | required (qualified for the station) + counter shift | own shift → partner; counter shift → requester |
| `takeover` | person on the shift | own shift, partner takes it | required (qualified) | own shift → partner |
| `handover` | person on the shift | own shift, nobody named | none — the manager picks | own shift → person picked by the manager |
| `shiftRequest` | anyone qualified | an **open** shift | – | nothing automatic: manager accepts, then runs `sp_shift_staff` (phase 1) |

**Design decision — no partner consent.** On a swap or takeover the shift lead's
(manager's) approval is enough; the named partner is not asked to confirm. The
manager is expected to agree it with the partner outside the workspace. Build
`sp_swap_decide` (4.5) without a confirmation step.

### 1.2 Properties (planning scope; English scope-own values from phase 0)

| Type | Key | value_type | Values / default | Set by |
|---|---|---|---|---|
| changeRequest | `requestKind` | options | `swap`, `takeover`, `handover`, `shiftRequest` (scope-specific, phase 0 §1.5) | request actions, **at creation** |
| changeRequest | `changeStatus` | options | `proposed`, `accepted`, `rejected` | creation `proposed`; decisions |
| changeRequest | `text` | string | `<kind>: {message}` | request actions |
| changeRequest | `description` | string | `created by {current_user_email}` | request actions |
| changeRequest | `proposedKey` | string | legacy; not used by any gate or button | optional (see 4.6) |
| absence | `absenceKind` | options | `vacation`, `sick`, `dayOffWish`, `training`, `availability` | form |
| absence | `absenceStart`, `absenceEnd` | datetime | | form |
| absence | `halfDay` | options | `no` (default), `firstHalf`, `secondHalf` | form |
| absence | `absenceNote` | string | label "(no diagnosis)" | form |
| absence | `absenceStatus` | options | `requested` (default), `approved`, `rejected` | form `requested`; decisions |
| file | `description` | string | `<kind>; valid until YYYY-MM-DD` | qualification form |

`requestKind` must be set **in the create action**: notification rules hang on insert
and on the decision update, and the inbox buttons read it. Never patch it later.

A **day-off wish** is an `absence` with `absenceKind = dayOffWish`, not a change
request. It goes through the same form, the same approve/reject actions and the same
notifications as every absence.

## 2. Links

All `concerns` link values are exact, case-sensitive English strings. New in this
phase: `requestedBy`, `takingOver`, `counterShift`.

| From → To | Link type | `linkvalue` | Created by | Read by |
|---|---|---|---|---|
| changeRequest → shift | `concerns` | `shiftSwap` | swap, takeover, handover request | `sp_swap_decide` (`{linked:concerns:shift:shiftSwap}`), inbox |
| changeRequest → shift | `concerns` | `shiftRequest` | shift request | inbox, notification text |
| changeRequest → person | `concerns` | `requestedBy` | all four requests | `sp_swap_decide` (counter shift goes to this person), notifications |
| changeRequest → person | `concerns` | `takingOver` | swap, takeover | manager reads it for the decision prompt |
| changeRequest → shift | `concerns` | `counterShift` | swap | `sp_swap_decide` |
| absence → person | `concerns` | `concernsPerson` | absence form (link to the object the form ran on) | precheck, staff detail, notifications |
| file ↔ person | form-answer link | – | qualification form | staff detail panel "Files" (confirm: shown via `hasfile`) |
| person → shift | `worksShift` | – | phase 1; **moved** by decisions | guards, views |
| manager note → shift | `concerns` | `followUpOf` | approval precheck | notes |

## 3. Forms

Create with `onto_formdef_create` in the **team** scope (staff open it there), then
`onto_formdef_save`. Saving needs a form-writer right (confirm for your account).

### 3.1 `sp_absence_request` — Request absence (answer type `absence`)

| Key | Widget | Label (example) | Required | Options / notes |
|---|---|---|---|---|
| `notice` | `label` | "Please do not enter health data or diagnoses. Status starts as 'requested'." | – | |
| `absenceKind` | `select` | Kind of absence | yes | `vacation`, `sick`, `dayOffWish`, `training`, `availability` |
| `absenceStart` | `datepicker` (`mode: datetime`, `default: now`) | Absent from | yes | |
| `absenceEnd` | `datepicker` (`mode: datetime`) | Absent until | yes | |
| `halfDay` | `select` | Half day | no | `no`, `firstHalf`, `secondHalf` |
| `absenceNote` | `text` | Note (no diagnosis) | no | |
| `absenceStatus` | `select` | Status | yes | only `requested` |

```json
{"tool": "onto_formdef_save", "arguments": {"udid": "<absence_form_udid>", "name": "sp_absence_request", "formdef": {
  "version": 1, "title": "Request absence", "answer_type": "absence",
  "description": "Vacation, day-off wish, training, availability or sick leave. No diagnosis.",
  "fields": [
    {"key": "notice", "widget": "label", "label": "Please do not enter health data or diagnoses. Status starts as 'requested'."},
    {"key": "absenceKind", "widget": "select", "label": "Kind of absence", "required": true, "options": ["vacation", "sick", "dayOffWish", "training", "availability"]},
    {"key": "absenceStart", "widget": "datepicker", "label": "Absent from", "required": true, "datepicker": {"mode": "datetime", "default": "now"}},
    {"key": "absenceEnd", "widget": "datepicker", "label": "Absent until", "required": true, "datepicker": {"mode": "datetime"}},
    {"key": "halfDay", "widget": "select", "label": "Half day", "required": false, "options": ["no", "firstHalf", "secondHalf"]},
    {"key": "absenceNote", "widget": "text", "label": "Note (no diagnosis)", "required": false},
    {"key": "absenceStatus", "widget": "select", "label": "Status", "required": true, "options": ["requested"]}],
  "guards": [{"type": "linked_to_user", "linktype": "concerns"}]}}}
```

**Person binding (required):** `guards` in the form definition checks, before
anything is saved, that the person the answer `concerns` is the signed-in person
(the master person whose `email` equals the login). Submitting for anyone else is
refused with "This form does not concern your person"; nothing is written. Saving
on the own person works (confirmed in the browser with a staff account, as was the
refusal on a colleague). Without this guard a staff member can submit a complete
absence request for any colleague they can read. Accounts without a matching master
person cannot submit at all (fail-closed).

Do not try to express "own person only" as an action `condition` comparing a field
with a user placeholder (for example `email eq {current_user_email}`): whether
condition values substitute user placeholders is **worth confirming before use**; if they do
not, the condition never matches and the button disappears for everyone.

Sick leave stores only the kind and the period (country module, e.g.
[country-de.md](country-de.md) §3). The form does not check a collision with the
person's own shifts; the manager sees it at approval (precheck, 4.3).

### 3.2 `sp_qualification_certificate` — Upload qualification certificate (answer type `file`)

| Key | Widget | Label (example) | Required | Validation |
|---|---|---|---|---|
| `description` | `text` | Kind + valid until (e.g. `hygieneFollowUp; valid until 2027-03-15`) | yes | pattern `^(hygieneInitial|hygieneFollowUp|haccp|youthProtection|barLicence|firstAid|other); valid until \d{4}-\d{2}-\d{2}$`, message "Format: <kind>; valid until YYYY-MM-DD" |
| `certificate` | `documents` | Certificate (PDF/photo) | no | |

Take the list of kinds from intake 12. The validation pattern was **not** enforced on
a submit through MCP in the tested build — check the value after every MCP submit.

## 4. Actions

Saved with `onto_actiondef_save` (`body` as JSON string). Rules from phase 1 §4 apply.
Additionally:
- **Staff actions** list both scopes, `"scopes": [<planning_scope_id>, <team_scope_id>]`,
  so the button appears in team views; they write into planning only through
  `action.result_scope_id = <planning_scope_id>` (scope bridge) and must bind the
  acting person (`{user_person}`, `{user_email}` or `{current_user_email}`).
- **Manager actions** list only the planning scope and carry
  `require_scope_write: <planning_scope_id>`.
- `condition` is evaluated before the guard; both run before anything is written.
- **Guard yes or no** (column "Guard" below): actions on the staff member's **own
  shift** (swap, takeover, handover; clock in/out in phase 4) carry the
  `linked_to_user` / `worksShift` guard. `sp_shift_request` cannot: the open shift has
  no person yet. It is harmless without a guard because it only creates a request
  object bound to the signed-in person and changes nothing on the shift; the manager
  decides. `sp_absence_request` is a form answer: its person binding is a guard on
  the **form** (`guards` in the form definition, 3.1), not on the action.

### 4.1 Overview

| Key | Label (example) | On | Scopes | Bridge / gate | Guard | Effect |
|---|---|---|---|---|---|---|
| `sp_swap_request` | Request swap | shift | planning, team | `result_scope_id` planning | `linked_to_user` `worksShift` | create `swap` request |
| `sp_takeover_request` | Request takeover | shift | planning, team | bridge | same | create `takeover` request |
| `sp_handover_request` | Request handover | shift | planning, team | bridge | same | create `handover` request |
| `sp_shift_request` | Request shift | shift | planning, team | bridge | – (open shift has no person) | create `shiftRequest` |
| `sp_absence_request` | Request absence | person | master, team | `form_answer`, result planning | form guard `linked_to_user` `concerns` (3.1) | create absence draft |
| `sp_qualification_upload` | Upload certificate | person | master | `form_answer`, result planning; gate master | – | create file |
| `sp_swap_decide` | Approve swap / takeover / handover | changeRequest | planning | gate planning | – | `accepted` + move `worksShift` |
| `sp_swap_reject` | Reject swap / takeover / handover | changeRequest | planning | gate | – | `rejected` |
| `sp_shift_request_accept` | Accept shift request | changeRequest | planning | gate | – | `accepted` (staffing is a second step) |
| `sp_shift_request_reject` | Reject shift request | changeRequest | planning | gate | – | `rejected` + reason |
| `sp_swap_execute` | Execute swap on the shift | shift | planning | gate | – | manual move of one shift |
| `sp_absence_approve` | Approve absence | absence | planning | gate | – | `approved`, overlap precheck |
| `sp_absence_reject` | Reject absence | absence | planning | gate | – | `rejected` |

### 4.2 Staff requests

```json
{"key": "sp_swap_request", "label": "Request swap", "body": {
  "object_types": ["shift"], "scopes": [<planning_scope_id>, <team_scope_id>], "roles": ["member"],
  "guards": [{"type": "linked_to_user", "linktype": "worksShift", "message": "Only your own shift"}],
  "condition": {"props": [{"key": "shiftStatus", "op": "in", "value": ["planned", "published", "swapped"]}],
                "message": "Only for staffed shifts (for open shifts: 'Request shift')"},
  "prompts": [
    {"key": "partner", "label": "Swap partner (takes this shift)", "type": "text", "object_types": ["person"], "required": true, "persist": false,
     "options_filter": {"link_to": "{linked:concerns:space:station}", "linktype": "concerns", "linkvalue": "qualifiedFor", "direction": "from", "min": 1}},
    {"key": "counterShift", "label": "Counter shift (the one I take in return)", "type": "text", "object_types": ["shift"], "required": true, "persist": false,
     "future": true, "depends_on": "partner"},
    {"key": "message", "label": "Message (visible to your swap partner and the shift lead)", "type": "text", "required": false, "persist": false, "default": "no message"}],
  "action": {"type": "create", "object_type": "changeRequest", "name": "Swap request {now}", "status": "active",
    "props": {"requestKind": "swap", "changeStatus": "proposed", "text": "swap: {message}",
              "description": "created by {current_user_email}"},
    "links": [
      {"type": "concerns", "to": "{object_udid}", "linkvalue": "shiftSwap"},
      {"type": "concerns", "to": "{user_person}", "linkvalue": "requestedBy"},
      {"type": "concerns", "to": "{partner}", "linkvalue": "takingOver"},
      {"type": "concerns", "to": "{counterShift}", "linkvalue": "counterShift"}],
    "result_scope_id": <planning_scope_id>}}}
```

- `options_filter` offers only colleagues qualified for the station of **this** shift.
- `depends_on: "partner"` with `future: true` offers only future shifts of the chosen
  partner as counter shift.
- `{user_person}` is the master person whose `email` equals the caller's login. A staff
  member without such a person gets an empty `requestedBy` link (phase 3 checks it).
- **The partner reads the request.** The `takingOver` link opens the whole request to
  the partner (core rule 1; "My requests" lists it for them): the message text and
  the `description` "created by <login e-mail>" included. The login e-mail is basic
  data colleagues can read anyway; the message is not private. Label the prompt so
  staff know (as above) and do not ask for private reasons here (worth confirming with two
  staff accounts, phase 3).
- **Guard:** staff reach only their own shifts through the team views; add the guard
  as shown anyway — it
  blocks a request on a colleague's shift opened by URL (worth confirming with a staff
  account in phase 3).

`sp_takeover_request`: same body without the `counterShift` prompt and link; name
`Takeover request {now}`; `requestKind: "takeover"`; `text: "takeover: {message}"`;
prompt `partner` labelled "Person taking over"; `message` labelled "Message (visible to
the person taking over and the shift lead)".

`sp_handover_request`: same guard and condition; only the `message` prompt; name
`Handover request {now}`; `requestKind: "handover"`; `text: "handover: {message}"`;
links `shiftSwap` → `{object_udid}` and `requestedBy` → `{user_person}`.

```json
{"key": "sp_shift_request", "label": "Request shift", "body": {
  "object_types": ["shift"], "scopes": [<planning_scope_id>, <team_scope_id>], "roles": ["member"],
  "condition": {"props": [{"key": "shiftStatus", "op": "eq", "value": "open"}],
                "message": "Only open shifts can be requested (the shift is staffed or cancelled)"},
  "prompts": [
    {"key": "person", "label": "Who is asking? (person)", "type": "text", "object_types": ["person"], "required": true, "persist": false},
    {"key": "message", "label": "Message to the shift lead", "type": "text", "required": false, "persist": false, "default": "no message"}],
  "action": {"type": "create", "object_type": "changeRequest", "name": "Shift request {now}", "status": "active",
    "props": {"requestKind": "shiftRequest", "changeStatus": "proposed", "text": "shift request: {message}",
              "description": "created by {current_user_email}"},
    "links": [
      {"type": "concerns", "to": "{object_udid}", "linkvalue": "shiftRequest"},
      {"type": "concerns", "to": "{person}", "linkvalue": "requestedBy"}],
    "result_scope_id": <planning_scope_id>}}}
```

A `person` prompt lets the caller pick any person. For staff use, replace the
`person` prompt by `"to": "{user_person}"` so nobody can ask in a colleague's name
(confirm: keep the prompt only if a manager files requests for others).

**No comment effect on the shift.** Do not add a comment such as "Shift request by
{person_name}" to this action. The shift is open, so every qualified colleague can
list it, and whoever is staffed on it later reaches the whole shift including its
comments — other people's applications would become visible. The request itself
already records who asked, when, and the message; the manager sees it in the inbox.
(Confirmed: the effect comment of a create action lands on the object the button
runs on — here the open shift — not on the new request; `{person_name}` is the
person picked in the prompt.)

**Open shift not yet linked to the person.** The row reaches the staff member through
`passt` in "Open shifts for me" (phase 3 §7.5, confirmed). The button then runs on a
shift that does not hang on that person. Test this in phase 3 with a staff account
(P3-13): the request must be created, the shift itself must stay unchanged, and a
shift of a station the person is not qualified for must not be offered — confirm
with a staff account.

```json
{"key": "sp_absence_request", "label": "Request absence", "body": {
  "object_types": ["person"], "scopes": [<master_scope_id>, <team_scope_id>], "roles": ["member"],
  "action": {"type": "form_answer", "name": "Absence {now}", "form": "<absence_form_udid>",
    "result_scope_id": <planning_scope_id>,
    "props": {"description": "created by {current_user_email}"},
    "links": [{"type": "concerns", "linkvalue": "concernsPerson"}]}}}
```

- The form answer is linked to the person the button ran on; the `concerns` link
  without `to` carries the value `concernsPerson` (absence → person).
- `form_answer` links the **source person**, not necessarily the caller.
- **Own person only:** the form guard (3.1) saves a request on the own person and
  refuses one for a colleague (both confirmed). The manager still sees requester
  (actor link) and person concerned on every request.
- Opening the form already creates an empty `draft` answer, also when the save is
  then refused; managers ignore `draft` answers and remove stale ones.
- The action has no prompts: Apply in the first dialog creates the draft and opens
  the referenced form. Enter kind and dates there; opening it is not a completed
  request. A `requested` submit has no decision-notification trigger in this recipe.

`sp_qualification_upload` (manager): on `person`, scopes `[<master_scope_id>]`,
`{"type": "form_answer", "name": "Certificate {now}", "form": "<qualification_form_udid>", "result_scope_id": <planning_scope_id>, "require_scope_write": <master_scope_id>}`.

### 4.3 Manager decisions — absences

```json
{"key": "sp_absence_approve", "label": "Approve absence", "body": {
  "object_types": ["absence"], "scopes": [<planning_scope_id>], "roles": ["member"],
  "condition": {"props": [{"key": "absenceStatus", "op": "eq", "value": "requested"}], "message": "Only requested absences can be approved"},
  "action": {"type": "update", "props": {"absenceStatus": "approved"}, "require_scope_write": <planning_scope_id>},
  "precheck": {"type": "person_time_overlap",
    "person_link": "concerns", "person_link_value": "concernsPerson",
    "against_type": "shift", "against_link": "worksShift",
    "from_key": "absenceStart", "to_key": "absenceEnd",
    "against_from": "shiftStart", "against_to": "shiftEnd",
    "against_status": ["planned", "published"],
    "confirm_prompt": "confirm",
    "message": "Attention: {n} shift(s) in this period are still staffed with this person: {namen}. Approving sets them to 'open' and removes the assignment. Approve anyway?",
    "set_on_confirm": {"shiftStatus": "open"},
    "hint": {"type": "serviceOrder", "name": "Note: shift {name} released – person absent",
             "props": {"orderStatus": "open", "task": "planNote"}, "linkvalue": "followUpOf"}}}}
```

- The precheck finds shifts of the same person (via `worksShift`) that overlap the
  absence, asks for confirmation, then sets them `open`, removes the assignment and
  creates one manager note per shift. `{n}` and `{namen}` are the platform's
  placeholders (count, names).
- `against_status`: list both `planned` and **`published`**, otherwise published
  shifts are not checked. Include `published` (confirm that the precheck then also releases published
  shifts and that the removed person is notified by the `link_removed` rule, phase 3).
- Gate approve/reject (`require_scope_write`).

`sp_absence_reject`: condition `absenceStatus eq requested` ("Only requested absences
can be rejected"); `{"type": "update", "props": {"absenceStatus": "rejected"}, "require_scope_write": <planning_scope_id>}`.

### 4.4 Manager decisions — shift requests

```json
{"key": "sp_shift_request_accept", "label": "Accept shift request", "body": {
  "object_types": ["changeRequest"], "scopes": [<planning_scope_id>], "roles": ["member"],
  "condition": {"props": [{"key": "requestKind", "op": "eq", "value": "shiftRequest"},
                          {"key": "changeStatus", "op": "eq", "value": "proposed"}],
                "message": "Only open shift requests can be accepted"},
  "action": {"type": "update", "props": {"changeStatus": "accepted"},
    "effects": [{"type": "comment", "text": "Shift request accepted {now} by {user_email} – now run 'Staff shift' on the shift"}],
    "require_scope_write": <planning_scope_id>}}}
```

Accepting does **not** staff the shift. The manager opens the shift and runs
`sp_shift_staff` (phase 1) with the requesting person. Two clicks by design.

`sp_shift_request_reject`: same condition ("… can be rejected"); prompt
`{"key": "reason", "label": "Reason (optional)", "type": "text", "required": false, "persist": false, "default": "no reason given"}`;
`props: {"changeStatus": "rejected"}`; effect comment `Shift request rejected {now} by {user_email}: {reason}`; gate.

### 4.5 Manager decisions — swap, takeover, handover

```json
{"key": "sp_swap_decide", "label": "Approve swap / takeover / handover (move staffing)", "body": {
  "object_types": ["changeRequest"], "scopes": [<planning_scope_id>], "roles": ["member"],
  "condition": {"props": [{"key": "requestKind", "op": "in", "value": ["swap", "takeover", "handover"]},
                          {"key": "changeStatus", "op": "eq", "value": "proposed"}],
                "message": "Only open swap, takeover or handover requests can be approved"},
  "prompts": [{"key": "person", "label": "Person taking over (see request: 'takingOver')", "type": "text", "object_types": ["person"], "required": true, "persist": false}],
  "action": {"type": "update", "props": {"changeStatus": "accepted"},
    "effects": [
      {"type": "replace_link", "on": "{linked:concerns:shift:shiftSwap}", "linktype": "worksShift", "side": "object1", "to": "{prompt:person}"},
      {"type": "replace_link", "on": "{linked:concerns:shift:counterShift}", "linktype": "worksShift", "side": "object1", "to": "{linked:concerns:person:requestedBy}"},
      {"type": "comment", "text": "Swap/takeover/handover approved {now} by {user_email}: shift moved to {person_name}"}],
    "require_scope_write": <planning_scope_id>}}}
```

- `replace_link` on the requested shift (`shiftSwap`) replaces the **person side**
  (`object1`) of its `worksShift` link with the prompted person; on a swap the second
  effect gives the counter shift to the requester. Exactly these links move — nothing
  else is touched.
- For `takeover` and `handover` there is no `counterShift` link (confirm: the second
  effect is skipped without error).
- For `handover` the manager chooses the person in the prompt; for `swap`/`takeover`
  copy the `takingOver` person of the request.
- The decision does not change `shiftStatus`. The phase-3 message "you took over this
  shift" hangs on `shiftStatus = swapped`; the decision path therefore reaches people
  through the request rules (4.7), not through the shift (confirm which messages a
  swap produces in phase 3).

`sp_swap_reject`: same condition; prompt
`{"key": "confirm", "label": "Confirm rejection", "type": "switch", "required": true, "persist": false}`;
`props: {"changeStatus": "rejected"}`; effect comment `Swap/takeover/handover rejected {now} by {user_email}`; gate.

```json
{"key": "sp_swap_execute", "label": "Execute swap on the shift (move staffing)", "body": {
  "object_types": ["shift"], "scopes": [<planning_scope_id>], "roles": ["member"],
  "condition": {"props": [{"key": "shiftStatus", "op": "in", "value": ["planned", "published", "swapped"]}], "message": "Shift is not staffed"},
  "prompts": [
    {"key": "giver", "label": "Person giving up the shift (see request: 'requestedBy')", "type": "text", "object_types": ["person"], "required": true, "persist": false},
    {"key": "taker", "label": "Person taking over (see request: 'takingOver')", "type": "text", "object_types": ["person"], "required": true, "persist": false,
     "options_filter": {"link_to": "{linked:concerns:space:station}", "linktype": "concerns", "linkvalue": "qualifiedFor", "direction": "from", "min": 1}}],
  "action": {"type": "update", "props": {"shiftStatus": "swapped"},
    "links": [
      {"type": "worksShift", "remove": "pair", "from": "{giver}", "to": "{object_udid}"},
      {"type": "worksShift", "from": "{taker}", "to": "{object_udid}", "require": "absent", "text": "This person is already on this shift"}],
    "effects": [{"type": "comment", "text": "Swap {now}: given by {giver_name} to {taker_name}"}],
    "require_scope_write": <planning_scope_id>}}}
```

`sp_swap_execute` is the manual path on one shift (e.g. a phone agreement without a
request). It sets `swapped`, which the publish action accepts again (phase 1).

### 4.6 Legacy field `proposedKey`

Older builds still write `proposedKey` (`worksShift` / a shift-request
marker) and keeps it as a hidden inbox column. No gate, button or notification uses
it any more; all decisions read `requestKind`. A fresh build can leave it out
(confirm: nothing else depends on it).

### 4.7 Triggers and notifications

Notification rules are **defined in phase 3** ([phase3.md](phase3.md) §6, e-mail/push
off until the phase-3 acceptance). The events of this phase and who they reach:

| Rule (key) | `on` / type | Condition | Recipients (`to_link` / `to_linkvalue`) | Text (example) |
|---|---|---|---|---|
| `sp_msg_absence_approved` | update absence | `changed absenceStatus`, `= approved` | `concerns` / `concernsPerson` | "Your absence was approved: {object_name}." |
| `sp_msg_absence_rejected` | update absence | `= rejected` | `concerns` / `concernsPerson` | "Your absence was rejected: {object_name}." |
| `sp_msg_shift_request_accepted` | update changeRequest | `changed changeStatus`, `= accepted`, `requestKind eq shiftRequest` | `concerns` / `requestedBy` | "The shift lead accepted your shift request ({object_name}). {linked:concerns:shiftRequest:name} Please check 'My shifts'." |
| `sp_msg_shift_request_rejected` | same | `= rejected`, `shiftRequest` | `concerns` / `requestedBy` | "… rejected your shift request …" |
| `sp_msg_swap_approved` | update changeRequest | `= accepted`, `requestKind in [swap, takeover, handover]` | `concerns` / `requestedBy` | "The shift lead approved your request ({object_name}). {linked:concerns:shiftSwap:name} Please check 'My shifts'." |
| `sp_msg_swap_partner_approved` | same | same | `concerns` / `takingOver` | "… approved a swap … You take over …" |
| `sp_msg_swap_rejected` | same | `= rejected`, same kinds | `concerns` / `requestedBy` | "… rejected your request …" |

Always restrict with `to_linkvalue`: `to_link: "concerns"` with `to_prop: "email"` and
`all: true` alone reaches **every** linked object with an e-mail. Optional manager
notes (absence approved → "check affected shifts", swap approved → "move staffing")
are not used; the precheck (4.3) and
`sp_swap_decide` (4.5) replace them.

## 5. Views

Create with `onto_interface_create_def` in the planning scope, `roles: ["member"]`,
`view_config` as JSON string with `access.require = "write"` (managers only). Staff
views ("My requests", "My shifts" with the request buttons) are phase 3.

### 5.1 `sp_request_inbox` — request inbox (manager)

Wanted effect: all change requests, newest/open first; filters
status and kind; columns title, kind, status as coloured badge (open = amber,
accepted = green, rejected = red), created by, date, shift, persons; a hidden `udid`
column; row buttons chosen by `requestKind` and `changeStatus`. Block form (confirm: block-only equivalent —
especially the badge column, the person list and the "open first" order):

```json
{"elements": ["filter", "table"],
 "access": {"require": "write"},
 "table": {"from": "objects", "type": "changeRequest",
  "columns": [
    {"key": "udid", "system": "udid", "hidden": true},
    {"key": "title", "system": "name", "label": "Title"},
    {"key": "kind", "prop": "requestKind", "label": "Kind",
     "werte": {"swap": "Swap", "takeover": "Takeover", "handover": "Handover", "shiftRequest": "Shift request"}},
    {"key": "status", "prop": "changeStatus", "label": "Status",
     "werte": {"proposed": "open", "accepted": "accepted", "rejected": "rejected"}},
    {"key": "createdBy", "prop": "description", "label": "Created by"},
    {"key": "date", "system": "created", "format": "wochentag_datum_zeit", "label": "Date"},
    {"key": "shift", "link": "concerns", "richtung": "vorwaerts", "linkvalue": "shiftSwap", "type": "shift", "system": "name", "label": "Shift"},
    {"key": "openShift", "link": "concerns", "richtung": "vorwaerts", "linkvalue": "shiftRequest", "type": "shift", "system": "name", "label": "Open shift"},
    {"key": "requester", "link": "concerns", "richtung": "vorwaerts", "linkvalue": "requestedBy", "type": "person", "prop": ["firstName", "lastName"], "label": "Requested by"},
    {"key": "partner", "link": "concerns", "richtung": "vorwaerts", "linkvalue": "takingOver", "type": "person", "prop": ["firstName", "lastName"], "label": "Taking over"}],
  "filter": ["status", "kind"],
  "sort": {"key": "date", "dir": "desc"},
  "row_actions": [
    {"action": "sp_swap_decide", "label": "Decide", "icon": "check",
     "when": {"requestKind": ["swap", "takeover", "handover"], "changeStatus": "proposed"}},
    {"action": "sp_swap_reject", "label": "Reject", "icon": "remove",
     "when": {"requestKind": ["swap", "takeover", "handover"], "changeStatus": "proposed"}},
    {"action": "sp_shift_request_accept", "label": "Accept", "icon": "check",
     "when": {"requestKind": "shiftRequest", "changeStatus": "proposed"}},
    {"action": "sp_shift_request_reject", "label": "Reject", "icon": "remove",
     "when": {"requestKind": "shiftRequest", "changeStatus": "proposed"}}]}}
```

- `row_actions[].when` keys are **property keys** of the row object; an array means
  "one of". Decided rows show no buttons.
- The button only shows the action; the action's own `condition` and gate decide
  whether it runs. Keep both in sync.
- An older filter form is `filter.fields` with
  `{"field": "changeStatus", "type": "select", "source": "distinct"}` (and the same for
  `requestKind`). With blocks, `filter` names the column keys.
- A badge column looks like
  (`"type": "badge", "map": {"proposed": {"type": "badge", "color": "#f9a825", "value": "open"}, …}`);
  whether `badge`/`map` work on block columns is worth confirming. `werte` is the fallback.
- Absences are **not** in this inbox. Managers decide them on the absence (buttons
  `sp_absence_approve` / `sp_absence_reject`) or from the staff detail (5.3). An
  absence inbox: (confirm: block list of `absence` with a person column via
  `concerns`/`concernsPerson` and `row_actions` on `absenceStatus = requested`).

### 5.2 `sp_staff_list` — staff list (manager)

Base set: persons (master); sorted by name; row button opens the detail page.

```json
{"elements": ["table"],
 "access": {"require": "write"},
 "table": {"from": "objects", "type": "person",
  "columns": [
    {"key": "udid", "system": "udid", "hidden": true},
    {"key": "name", "system": "name", "label": "Name"},
    {"key": "firstName", "prop": "firstName", "label": "First name"},
    {"key": "lastName", "prop": "lastName", "label": "Last name"},
    {"key": "email", "prop": "email", "label": "Login e-mail"},
    {"key": "birthYear", "prop": "birthYear", "label": "Year of birth", "format": "jahr"}],
  "sort": {"key": "name", "dir": "asc"},
  "row_actions": [{"label": "Detail", "icon": "eye-open", "url": "ontouser/interface/show/sp_staff_detail?udid={udid}"}]}}
```

Do not show a phone column; phone is protected data (E2) and is not on the master
person in this skill. `format: "jahr"` shows `1990` instead of a
date. Hard-reload the browser after changing a format.

### 5.3 `sp_staff_detail` — staff detail with subforms (manager)

Element `detail` on one person (`?udid=<person_udid>`), header fields from the person,
panels as **subforms** reached over links (`via`). Lives in planning (no data scope):
the manager's read covers persons in master and shifts/absences in planning; staff
never get in (`access.require`).

```json
{"elements": ["detail"],
 "access": {"require": "write"},
 "detail": {"type": "person",
  "fields": [
    {"system": "name", "label": "Name"},
    {"prop": "firstName", "label": "First name"},
    {"prop": "lastName", "label": "Last name"},
    {"prop": "email", "label": "Login e-mail"},
    {"prop": "birthYear", "label": "Year of birth", "format": "jahr"},
    {"system": "scope", "label": "Area"},
    {"system": "type", "label": "Type"},
    {"system": "modified", "key": "modifiedUtc", "label": "Last changed"}],
  "panels": [
    {"title": "Qualified for", "type": "subform", "from": "objects", "objekt": "space",
     "via": {"link": "concerns", "richtung": "vorwaerts", "linkvalue": "qualifiedFor"},
     "sort": {"key": "name", "dir": "asc"},
     "columns": [{"key": "name", "system": "name"}]},
    {"title": "Next shifts", "type": "subform", "from": "objects", "objekt": "shift",
     "via": {"link": "worksShift", "richtung": "vorwaerts"},
     "wo": [{"prop": "shiftStart", "op": ">=", "wert": "{today}"},
            {"prop": "shiftStatus", "op": "!=", "wert": "cancelled"}],
     "sort": {"prop": "shiftStart", "dir": "asc"},
     "columns": [
       {"key": "day", "prop": "shiftStart", "format": "wochentag_datum"},
       {"key": "time", "prop": "shiftStart", "bis": "shiftEnd", "format": "zeitspanne"},
       {"key": "station", "prop": "station", "werte": {"kitchen": "Kitchen", "service": "Service", "bar": "Bar", "dishwashing": "Dishwashing", "shiftLead": "Shift lead"}},
       {"key": "status", "prop": "shiftStatus", "werte": {"open": "open", "planned": "planned", "published": "published", "swapped": "swapped", "cancelled": "cancelled"}}]},
    {"title": "Absences", "type": "subform", "from": "objects", "objekt": "absence",
     "via": {"link": "concerns", "richtung": "rueckwaerts"},
     "sort": {"prop": "absenceStart", "dir": "desc"},
     "columns": [
       {"key": "kind", "prop": "absenceKind", "werte": {"vacation": "Vacation", "dayOffWish": "Day-off wish", "training": "Training", "availability": "Availability", "sick": "Sick"}},
       {"key": "from", "prop": "absenceStart", "format": "datum"},
       {"key": "to", "prop": "absenceEnd", "format": "datum"},
       {"key": "status", "prop": "absenceStatus", "werte": {"requested": "requested", "approved": "approved", "rejected": "rejected"}}]},
    {"title": "Files", "type": "dateien", "field": "hasfile"},
    {"title": "Comments", "type": "comments"}]}}
```

- `via.richtung`: `vorwaerts` = links **from** the person (qualification, `worksShift`);
  `rueckwaerts` = links **to** the person (absence → person). `objekt` restricts the
  type, so change requests that also point to the person via `concerns` do not appear
  in "Absences".
- Do not list `performs` as link for absences (an older actual-time path); this skill
  does not use it.
- `absenceNote` is deliberately not shown (no diagnosis surface).
- Optional panel "Requests": `objekt: "changeRequest"`, `via: {"link": "concerns", "richtung": "rueckwaerts", "linkvalue": "requestedBy"}`, columns kind, status, created (confirm: not yet built).
- Protected data (pay, contract, private contact) is a separate manager-only panel or
  view once phase 4 has fixed where it lives (confirm).

## 6. Recipe (tool order with example arguments)

```json
[
  {"tool": "onto_type_show", "arguments": {"name": "changeRequest", "scope_id": <planning_scope_id>, "limit": 1}},

  {"tool": "onto_formdef_create", "arguments": {"...": "title 'Request absence', scope <team_scope_id>"}},
  {"tool": "onto_formdef_save", "arguments": {"udid": "<absence_form_udid>", "name": "sp_absence_request", "formdef": {"...": "see 3.1"}}},
  {"tool": "show_formdef", "arguments": {"udid": "<absence_form_udid>"}},

  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_absence_request", "label": "Request absence", "body": "<JSON string of 4.2>"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_swap_request", "label": "Request swap", "body": "<JSON string of 4.2>"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_takeover_request", "label": "Request takeover", "body": "<JSON string>"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_handover_request", "label": "Request handover", "body": "<JSON string>"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_shift_request", "label": "Request shift", "body": "<JSON string of 4.2>"}},

  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_absence_approve", "label": "Approve absence", "body": "<JSON string of 4.3>"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_absence_reject", "label": "Reject absence", "body": "<JSON string>"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_shift_request_accept", "label": "Accept shift request", "body": "<JSON string of 4.4>"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_shift_request_reject", "label": "Reject shift request", "body": "<JSON string>"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_swap_decide", "label": "Approve swap / takeover / handover", "body": "<JSON string of 4.5>"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_swap_reject", "label": "Reject swap / takeover / handover", "body": "<JSON string>"}},
  {"tool": "onto_actiondef_save", "arguments": {"key": "sp_swap_execute", "label": "Execute swap on the shift", "body": "<JSON string of 4.5>"}},
  {"tool": "onto_actiondef_list", "arguments": {"limit": 200}},

  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_request_inbox", "label": "Requests", "scope_id": <planning_scope_id>,
     "roles": ["member"], "object_type_ids": [<changeRequest_type_id>], "description": "Change and swap requests; decision per row; managers only.",
     "view_config": "<JSON string of 5.1>"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_staff_detail", "label": "Staff detail", "scope_id": <planning_scope_id>,
     "roles": ["member"], "object_type_ids": [<person_type_id>], "description": "One person: qualifications, next shifts, absences, files, comments; managers only.",
     "view_config": "<JSON string of 5.3>"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_staff_list", "label": "Staff", "scope_id": <planning_scope_id>,
     "roles": ["member"], "object_type_ids": [<person_type_id>], "description": "Staff list for managers; row opens the detail page.",
     "view_config": "<JSON string of 5.2>"}},

  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_swap_request", "udid": "<shift_udid of staff A>",
     "prompts": {"partner": "<person_udid of staff B>", "counterShift": "<shift_udid of staff B>", "message": "TEST-2 swap"}}},
  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_swap_decide", "udid": "<request_udid>",
     "prompts": {"person": "<person_udid of staff B>"}}},
  {"tool": "onto_object_show", "arguments": {"udid": "<shift_udid of staff A>"}}
]
```

Order: forms → staff actions → manager actions → views → tests. Define the inbox only
after the decision actions exist (row actions name them). Run the request actions as a
**staff test account** (the bridge and the guard only prove something there); as the
manager, `{user_person}` resolves only if a master person carries the manager's login
e-mail (confirm).

## 7. Smoke tests (MCP)

| # | Call | Expected |
|---|---|---|
| P2-1 | `onto_actiondef_list` | staff actions with scopes planning + team and `result_scope_id`; manager actions with planning only and `require_scope_write` |
| P2-2 | staff: `sp_swap_request` on own published shift | `changeRequest` in **planning**, `requestKind swap`, `changeStatus proposed`, four `concerns` links with the exact values |
| P2-3 | staff: `sp_swap_request` on a colleague's shift | refused with "Only your own shift"; nothing created |
| P2-4 | staff: `sp_shift_request` on a staffed shift | refused with the condition message |
| P2-5 | staff: `sp_absence_request` with `dayOffWish` | `absence` in planning, `absenceStatus requested`, link `concernsPerson` → own person |
| P2-5b | staff: `sp_absence_request` on a colleague, submit | refused ("This form does not concern your person"); no `requested` answer for the colleague; remove the empty draft |
| P2-6 | manager: `sp_swap_decide` on P2-2 | request `accepted`; shift A now `worksShift` from B, counter shift from A; no other link changed; comment present |
| P2-7 | manager: `sp_swap_decide` on a `shiftRequest` | refused (condition) |
| P2-8 | manager: `sp_shift_request_accept`, then `sp_shift_staff` | request `accepted`; shift `planned` with the requester |
| P2-9 | manager: `sp_absence_approve` on an absence that overlaps a staffed shift | confirmation with count and names; after confirm: shift `open`, assignment removed, one manager note `followUpOf` |
| P2-10 | second decision on any decided request/absence | refused (condition) |
| P2-11 | staff: any decision action | not offered / refused (gate) |
| P2-12 | `onto_interface_show` inbox, list, detail | `access.require` = `write`; definitions use blocks only |
| P2-13 | `onto_credit_balance` (manager and staff test account) | staff paid their own actions; spend logged |

## 8. Browser checks

| Role | Check | Expected |
|---|---|---|
| manager | open `sp_request_inbox` | open requests show **Decide + Reject** for swap/takeover/handover and **Accept + Reject** for shift requests; decided rows show no buttons; filters kind and status work |
| manager | "Decide" on a swap | dialog asks for the person taking over; after saving, the week grid (phase 1) shows both people on their new shifts |
| manager | open `sp_staff_list` → "Detail" | detail page with header fields, year of birth as a year, panels Qualified for / Next shifts (no cancelled, from today) / Absences / Files / Comments |
| manager | open an absence that collides with a shift → "Approve" | warning with the shift names; confirm releases the shift |
| staff (test account; full check in phase 3) | own shift in the team view → buttons | Request swap / takeover / handover visible; partner picker lists only colleagues qualified for that station |
| staff | open shift → "Request shift" | request created; colleague's staffed shift has no such button |
| staff | own person → "Request absence" | form with the no-diagnosis notice; kind list contains Day-off wish |
| staff | open `sp_request_inbox` or `sp_staff_detail` by URL | refused |
| staff | out of credits, press a request button | HTTP 402 (dialog may hang) — top up via `ontouser_team_transfer`, see prerequisites |

## 9. Failure patterns

| Symptom | Cause | Fix |
|---|---|---|
| inbox shows no buttons on a new request | `requestKind` missing (set later or by a legacy form) | set it in the create action; legacy forms without `requestKind` must not be used |
| "Decide" visible but refused | `when` and action `condition` disagree | keep them identical |
| decision accepted, nobody moved | `replace_link.on` uses a link value that differs from the request's link (case, spaces) | use the exact `shiftSwap` / `counterShift` / `requestedBy` strings |
| everyone removed from the shift | `remove: true` instead of `remove: "pair"` | `remove: "pair"` |
| staff request lands in team scope or fails with 403 | `result_scope_id` missing or outside `action` | put it inside `action` |
| save refused: person binding | bridge action without `{user_person}` / `{user_email}` / `{current_user_email}` | add one (not needed for `form_answer`) |
| `requestedBy` link empty | caller has no master person with their login e-mail | fix the person's `email` (phase 3) |
| partner picker empty | shift has no `station` link or colleagues lack `qualifiedFor` | phase 1 links |
| precheck misses a published shift | `against_status` without `published` | include it |
| certificate with wrong format accepted | validation pattern not enforced on MCP submit | check after submit |
| staff files an absence for a colleague | form definition without `guards` | add the form guard (3.1) |
| request button vanished for everyone | action `condition` compares with a user placeholder | remove it; use the form guard (3.1) |
| staff's own absence refused ("does not concern your person") | no master person with the login e-mail, or the action links a different `concerns` target | fix the person's `email`; keep the action's `concerns` link to the source person |
| health details in an absence | free text in `absenceNote` | label "(no diagnosis)", manager removes it; never show the note in views |

## 10. Checks after phase 2

Run these once in your workspace; they are part of the acceptance scenario
([acceptance-scenario.md](acceptance-scenario.md), section 7):

- each of the three request actions refuses a decision by a staff member who is not
  the manager (the guard answers, nothing changes);
- `sp_absence_request` saves the own person and refuses a colleague (P2-5, P2-5b);
- `sp_swap_decide` handles takeover and handover without a second link error, and the
  requester receives exactly one message while the shift status stays unchanged;
- the precheck reports a published week as published when you retry it
  (`against_status`);
- a qualification file is visible on the detail page (`hasfile`), and a staff member
  with the form-writer right can save a form.
