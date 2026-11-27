# Phase 3 — staff view: accounts, "My shifts", open shifts, day-off wish, start card, notifications

**Goal:** every staff member has a managed account bound to their master person
(`person.email` = login), opens the workspace through the **team door**, sees **only
their own** shifts and requests, finds open shifts, files a day-off wish, lands on the
start card "My shifts", and is notified **only when affected**. One message to
everybody concerned happens only at the **first publication** of their shifts.

**Input:** phases 0–2 passed; intake questions 8, 9, 13, 16, 19, 24.

**Rights (unchanged from phase 0, now set for real accounts):**

| Account | `<company>_master` | `<company>_planning` | `<company>_team` |
|---|---|---|---|
| Manager / owner | R W M | R W M | R W M |
| Shift lead (optional) | R – – | R W – | R W – |
| Staff member | **R – –** | **– – –** (no membership) | R W – |

Staff have no right on planning. A planning object opens for them only through the
**person link**: their shift via `worksShift`, their absence or request via
`concerns`; a colleague's object stays closed and answers as if it did not exist.
Staff views use shifts, requests or absences as their base set and bind them to the
master person through the `person` block; "Open shifts for me" uses `passt`. The
views list what the person link reaches — they do not filter a readable scope.
Writes into planning go only through scope bridges (phases 2 and 4). Do **not**
grant planning read "so views work".

**Budget (pay-per-use):** accounts and rights are cheap writes; the expensive part is
the staff accounts' own action runs (20 credits each, paid from **their** balance).
Give each staff test account a small balance (e.g. 200 credits; confirm against the
acceptance scenario). **Triggers and notifications cost no credits** — only the
writes that cause them do.

**Platform references:**
[view-blocks.md](../../../telesherpa-ontology-platform/references/features/view-blocks.md) (person binding, periods, matching, rules, counters, deleted objects) ·
[company-manager.md](../../../telesherpa-ontology-platform/references/features/company-manager.md) (invite codes, managed accounts, transfers) ·
[start-cards.md](../../../telesherpa-ontology-platform/references/features/start-cards.md) (start cards, blocks) ·
[notifications-and-link-events.md](../../../telesherpa-ontology-platform/references/features/notifications-and-link-events.md) (notify, `link_removed`) ·
[scope-bridges.md](../../../telesherpa-ontology-platform/references/features/scope-bridges.md) (bridge, guard, person binding) ·
[member-agent-rules.md](../../../telesherpa-ontology-platform/references/features/member-agent-rules.md) (`access.require`, placeholders).

Placeholders: `<staff_profile_id>`, `<management_code>`, `<my_shifts_view>` (name of
the view), `<startcard_id>`. View block keywords as in [phase1.md](phase1.md).

---

## 1. Objects, properties, options

No new object types. Used here:

| Type | Key | Values | Role in this phase |
|---|---|---|---|
| person (master) | `email` | login e-mail | binds the account; must match exactly (lower case) |
| shift | `shiftStatus` | `open`, `planned`, `published`, `swapped`, `cancelled` | notification conditions |
| shift | `firstNoticeStatus` | `open`, `sent` | first-publication marker (phase 0 §1.4) |
| absence | `absenceKind = dayOffWish` | | day-off wish |
| absence | `absenceStatus` | `requested`, `approved`, `rejected` | decision messages |
| changeRequest | `requestKind`, `changeStatus` | phase 2 | decision messages |

`firstNoticeStatus` is the scope-specific marker created in phase 0 §1.5 (default
`open`). It must exist on every shift **before** the shift is published; the
first-publication rule only looks for "not `sent`". **Before enabling the schedule
rule, initialise already published historical shifts to `sent`** when no catch-up
message is wanted. Their past date does not exclude them. New shifts keep `open`
until first publication is processed. Publishing a plan period changes only the
period; publish the individual shifts separately.

## 2. Links

| Link | Use in this phase |
|---|---|
| `worksShift` person → shift | own shifts in team views; guard for own-row actions; recipients of shift messages |
| `concerns` / `requestedBy`, `takingOver` (request → person) | recipients of request decisions |
| `concerns` / `concernsPerson` (absence → person) | recipients of absence decisions |
| `concerns` / `qualifiedFor` (person → station) | open shifts "for me"; partner pickers |

## 3. Accounts (step by step)

1. **Code:** `create_invite_code` in the team scope with `kind: "management"`,
   `max_uses: 1`, an expiry date and a `label` (e.g. `staff TEST-3 cook`). The code
   grants no rights; it only marks the redeemer as managed by your scope.
2. **Hand over** the code to the staff member (or the test agent/human). Human accounts register with a dedicated mailbox, receive an activation e-mail,
   activate, and then call `redeem_invite_code`. The master person must use the
   **same e-mail as the activated login**. `example.com` is for documentation and
   synthetic records, not an activatable mailbox. If tests permit only these
   placeholder addresses, stop the human-login tests and record the blocker. An
   agent-registration route creates its own address and needs no mailbox; it does
   not activate an arbitrary `example.com` human login. Use only a separately
   authorised test-account route; never substitute a real staff account silently.
3. **Check:** `ontouser_team_index` lists the account with `managed_by_scope_id`.
4. **Rights:** `ontouser_team_set_scope_rights` — master `1/0/0`, team `1/1/0`. **No
   call for planning** (not even with zeros). Read back with `ontouser_team_show`.
5. **Credits:** `ontouser_team_transfer` with `to_profile_id`, `credits`, `reason`,
   `idempotency_key` (reuse the same key on a retry; a repeat answers "already booked").
6. **Person binding:** `onto_object_show` on the master person — `email` equals the
   login. Without it `{user_person}` and `{current_user_email}` find nothing.

Staff without their own device (intake 13): the manager clocks and files for them;
they get no account. Never share one account between people.

## 4. Forms

No new form. The **day-off wish** uses the absence form of phase 2
(`sp_absence_request`, `absenceKind = dayOffWish`).

## 5. Actions

No new actions. Staff use the bridge actions of phase 2 (requests) and phase 4
(clocking) from team views. Check that every staff action lists the team scope in
`body.scopes` and every manager action carries its execution gate. A gated button
may still appear; verify that staff execution is refused, not merely its visibility.

### 5.1 Day-off wish flow (absence)

| Step | Who | What | Result |
|---|---|---|---|
| 1 | staff | "My area" / own person → **Request absence**, kind `dayOffWish`, from/until | `absence` in planning, `requested`, link `concernsPerson` → own person |
| 2 | staff | "My absences" | the wish is listed as requested |
| 3 | manager | absence → **Approve absence** (precheck warns if the person is on a shift then) | `approved`; overlapping shifts released only after confirmation |
| 4 | trigger | `sp_msg_absence_approved` | message to the person only |
| 3' | manager | **Reject absence** | `rejected`; `sp_msg_absence_rejected` to the person only |

A day-off wish is a wish, not a right: approval is the manager's decision. Sick leave
goes through the same form but never carries a diagnosis.

**Own person only:** without the form guard (phase 2 §3.1) a staff member could
start this form on a readable colleague and save a complete request for that
colleague (confirmed). With the guard, saving for a colleague is refused and saving
on the own person works (both confirmed). Managers still see requester and person
concerned on every request. The current next-shift view
has no absence entry; provide a deliberate own-person entry (for example §7.6),
but do not treat the entry link as an execution permission check. The first action
dialog may have no inputs: Apply starts the original form, whose fields are entered
and submitted in the next step.

## 6. Triggers and notifications

Create with `onto_trigger_create` in the **planning** scope. Every notify effect
carries `title`, `text`, optional `url` (the staff view to open), and `email` / `push`
switches. **Keep `email: false, push: false` until the acceptance of this phase**,
then switch on with `onto_trigger_update`. In-app messages always arrive.

Rules hang on the event; triggers run asynchronously (1–5 minutes, scheduled rules on
a 5-minute tick). Everything a text needs must exist at that moment.

### 6.1 Who is told — only the affected people

| Key | Event | Condition | Recipients (`to_link` + `to_linkvalue`) | Text (example, label language from intake 19) |
|---|---|---|---|---|
| `sp_msg_first_publication` | `on: schedule`, shift | `shiftStatus eq published`, `firstNoticeStatus neq sent` | `worksShift` (all persons on the shift); then `set_property firstNoticeStatus = sent` | "Your shift was published: {object_name}." |
| `sp_msg_shift_cancelled` | update shift | `changed shiftStatus`, `= cancelled`, `firstNoticeStatus eq sent` | `worksShift` | "Your shift was cancelled: {object_name}. You do not need to come." |
| `sp_msg_shift_restaffed` | update shift | `changed shiftStatus`, `= published`, `firstNoticeStatus eq sent` | `worksShift` | "You are now on this shift: {object_name}. Please check your shifts." |
| `sp_msg_shift_swapped` | update shift | `changed shiftStatus`, `= swapped`, `firstNoticeStatus eq sent` | `worksShift` | "You took over this shift: {object_name}. Please check your shifts." |
| `sp_msg_assignment_removed` | `on: link_removed`, shift, `link_types: ["worksShift"]` | – | `to_removed: true` (the removed person) | "You are no longer on {object_name}." |
| `sp_msg_shift_request_accepted` | update changeRequest | `changed changeStatus`, `= accepted`, `requestKind eq shiftRequest` | `concerns` / `requestedBy` | "The shift lead accepted your shift request ({object_name}). {linked:concerns:shiftRequest:name} Please check 'My shifts'." |
| `sp_msg_shift_request_rejected` | same | `= rejected`, `shiftRequest` | `concerns` / `requestedBy` | "The shift lead rejected your shift request ({object_name}). {linked:concerns:shiftRequest:name}" |
| `sp_msg_swap_approved` | update changeRequest | `= accepted`, `requestKind in [swap, takeover, handover]` | `concerns` / `requestedBy` | "The shift lead approved your request ({object_name}). {linked:concerns:shiftSwap:name} Please check 'My shifts'." |
| `sp_msg_swap_partner_approved` | same | same | `concerns` / `takingOver` | "The shift lead approved a swap ({object_name}). {linked:concerns:shiftSwap:name} You take over — please check 'My shifts'." |
| `sp_msg_swap_rejected` | update changeRequest | `= rejected`, same kinds | `concerns` / `requestedBy` | "The shift lead rejected your request ({object_name}). {linked:concerns:shiftSwap:name}" |
| `sp_msg_absence_approved` | update absence | `changed absenceStatus`, `= approved` | `concerns` / `concernsPerson` | "Your absence was approved: {object_name}." |
| `sp_msg_absence_rejected` | same | `= rejected` | `concerns` / `concernsPerson` | "Your absence was rejected: {object_name}." |

Rules:
- **Swap, cancellation, assignment:** only the persons on the shift or named on the
  request get a message. Never `to: <all staff>`.
- **First publication is the only "everybody" message**: every person staffed on a
  published shift hears about it once; the marker `sent` stops repeats. There is **no
  bulk publish** — shifts are published one by one (phase 1), so the first-publication
  messages arrive per shift. A single summary per person and plan is an open decision
  (confirm: plan-level message, not part of this skill yet).
- Later changes to an announced shift (`firstNoticeStatus = sent`) notify only the
  affected persons via the change rules above.
- **Always `to_linkvalue`** on request and absence rules. `to_link: "concerns"` alone
  with `all: true` would also reach every other person the request points to.
- `{linked:…}` texts: put the placeholder at the end without a prefix — when the link
  is missing it resolves to nothing and no half sentence remains.
- `remove: "pair"` and `replace_link` both raise `link_removed`; a released person
  therefore gets "no longer on …" automatically.

```json
{"tool": "onto_trigger_create", "arguments": {"scope_id": <planning_scope_id>, "key": "sp_msg_first_publication", "name": "First publication of a shift",
  "body": {"on": "schedule", "object_types": ["shift"], "enabled": true,
    "condition": {"props": [{"key": "shiftStatus", "op": "eq", "value": "published"},
                            {"key": "firstNoticeStatus", "op": "neq", "value": "sent"}]},
    "effects": [
      {"type": "notify", "to_link": "worksShift", "to_prop": "email", "all": true,
       "title": "Shift published", "text": "Your shift was published: {object_name}.",
       "url": "ontouser/interface/show/<my_shifts_view>", "email": false, "push": false},
      {"type": "set_property", "props": {"firstNoticeStatus": "sent"}}]}}}
```

```json
{"tool": "onto_trigger_create", "arguments": {"scope_id": <planning_scope_id>, "key": "sp_msg_swap_partner_approved", "name": "Swap approved – partner",
  "body": {"on": "update", "object_types": ["changeRequest"], "enabled": true,
    "condition": {"changed": ["changeStatus"], "props": [
      {"key": "changeStatus", "op": "eq", "value": "accepted"},
      {"key": "requestKind", "op": "in", "value": ["swap", "takeover", "handover"]}]},
    "effects": [{"type": "notify", "to_link": "concerns", "to_linkvalue": "takingOver", "to_prop": "email", "all": true,
      "title": "Swap: you take over",
      "text": "The shift lead approved a swap ({object_name}). {linked:concerns:shiftSwap:name} You take over — please check 'My shifts'.",
      "url": "ontouser/interface/show/<my_shifts_view>", "email": false, "push": false}]}}}
```

```json
{"tool": "onto_trigger_create", "arguments": {"scope_id": <planning_scope_id>, "key": "sp_msg_assignment_removed", "name": "Assignment removed",
  "body": {"on": "link_removed", "object_types": ["shift"], "link_types": ["worksShift"], "enabled": true,
    "effects": [{"type": "notify", "to_removed": true, "title": "Assignment changed",
      "text": "You are no longer on {object_name}.",
      "url": "ontouser/interface/show/<my_shifts_view>", "email": false, "push": false}]}}}
```

Known gaps:
- First-publication and restaffing rules both inspect the current state. Exactly
  one first-publication message without an additional restaffing message has not
  been confirmed for all event/schedule orderings; do not present this as passed.
- A **handover** has no `takingOver` person; the person the manager picks gets the
  shift through `replace_link` but no request message, and the shift status does not
  change, so no shift rule fires (confirm: a message for the new person on
  handover).
- `sp_msg_shift_restaffed` fires only when the status **changes** to `published`; a
  person added to an already published shift without a status change is not told
  (confirm).
- A cancelled shift that was never published (`firstNoticeStatus` ≠ `sent`) sends
  nothing — intended: nobody had been told about it.
- The manager notes of phase 1/2 (cancelled shift, absence released) stay in planning;
  they are not messages.

## 7. Views (team scope)

All staff views live in the **team** scope with `data_scope_id = <planning_scope_id>`
and a **person binding**. A team view without person binding is refused when saved;
7.1 is the exception that binds through `wo` on `email = {'current_user_email'}`
(placeholder spellings: see glossary).
The `person` block carries `link`, `richtung`, `prop` and `type`; it compares
against the signed-in person automatically. Do not add a `wert` or an e-mail
placeholder to that block. `passt` binds matching open shifts to the viewer instead.
Every view shows only own or explicitly matching rows; there is no person parameter. Views are paginated (10 rows per
page by default, 200 at most) — keep a period or an upcoming-only filter. All views in this section are confirmed in the
browser as staff (only own rows) and as manager, except "My absences" (7.4).

### 7.1 `sp_my_next_shift` — "My next shift" (block view, tested)

```json
{"elements": ["table"],
 "table": {"from": "objects", "type": "person", "scopes": ["<company>_master"],
  "wo": [{"prop": "email", "op": "=", "wert": "{'current_user_email'}"}],
  "links": {"next": {"link": "worksShift", "richtung": "vorwaerts", "type": "shift",
                     "sort": {"prop": "shiftStart", "dir": "asc"},
                     "wo": [{"prop": "shiftStatus", "op": "!=", "wert": "cancelled"},
                            {"prop": "shiftStart", "op": ">=", "wert": "{today}"}]}},
  "columns": [
    {"key": "day", "link": "next", "prop": "shiftStart", "format": "wochentag_datum", "label": "Day"},
    {"key": "time", "link": "next", "prop": "shiftStart", "bis": "shiftEnd", "format": "zeitspanne", "label": "Time"},
    {"key": "station", "link": "next", "prop": "station", "label": "Station",
     "werte": {"kitchen": "Kitchen", "service": "Service", "bar": "Bar", "dishwashing": "Dishwashing", "shiftLead": "Shift lead"}},
    {"key": "status", "link": "next", "prop": "shiftStatus", "label": "Status",
     "werte": {"published": "published", "open": "open", "planned": "planned", "swapped": "swapped", "cancelled": "cancelled"}}],
  "nur": ["day"],
  "sort": {"key": "day", "dir": "asc"}}}
```

```json
{"tool": "onto_interface_create_def", "arguments": {"name": "sp_my_next_shift", "label": "My next shift",
  "scope_id": <team_scope_id>, "data_scope_id": <planning_scope_id>, "roles": ["member"], "object_type_ids": [<person_type_id>],
  "description": "Only the logged-in person: next shift from today (Europe/Berlin) via worksShift; cancelled shifts ignored.",
  "view_config": "<JSON string above>"}}
```

### 7.2 `sp_my_shifts` — "My shifts" (start card target)

Wanted effect: all own shifts from today on, chronologically, as cards or table: day
and time, station, kind, status (cancelled marked), actual times once clocked; row
buttons on each shift: Request swap / takeover / handover (phase 2), Clock in / Clock
out (phase 4). Filters station and status.

The view is built from the
`person` block (confirmed: as staff it lists only the person's own shifts). The
`wo` filter on `{today}` keeps it to upcoming shifts — without it every past shift
is listed too; today's shifts stay in, so a running shift can still be clocked out.
The row object is a shift, so row actions run on that shift.

```json
{
  "elements": [
    "filter",
    "table"
  ],
  "table": {
    "from": "objects",
    "type": "shift",
    "status": "active",
    "person": {
      "link": "worksShift",
      "richtung": "rueckwaerts",
      "prop": "email",
      "type": "person"
    },
    "wo": [
      {
        "prop": "shiftStart",
        "op": ">=",
        "wert": "{today}"
      }
    ],
    "columns": [
      {
        "key": "udid",
        "system": "udid",
        "hidden": true
      },
      {
        "key": "day",
        "prop": "shiftStart",
        "format": "wochentag_datum",
        "label": "Day"
      },
      {
        "key": "time",
        "prop": "shiftStart",
        "bis": "shiftEnd",
        "format": "zeitspanne",
        "label": "Time"
      },
      {
        "key": "station",
        "prop": "station",
        "label": "Station",
        "werte": {
          "kitchen": "Kitchen",
          "service": "Service",
          "bar": "Bar",
          "dishwashing": "Dishwashing",
          "shiftLead": "Shift lead"
        }
      },
      {
        "key": "kind",
        "prop": "shiftKind",
        "label": "Kind",
        "werte": {
          "early": "Early",
          "late": "Late",
          "split": "Split",
          "night": "Night"
        }
      },
      {
        "key": "status",
        "prop": "shiftStatus",
        "label": "Status",
        "werte": {
          "planned": "planned",
          "published": "published",
          "swapped": "swapped",
          "cancelled": "cancelled – does not take place"
        }
      }
    ],
    "filter": [
      "station",
      "status"
    ],
    "sort": {
      "key": "day",
      "dir": "asc"
    },
    "row_actions": [
      {
        "action": "sp_clock_in",
        "label": "Clock in"
      },
      {
        "action": "sp_clock_out",
        "label": "Clock out"
      },
      {
        "action": "sp_swap_request",
        "label": "Swap"
      },
      {
        "action": "sp_takeover_request",
        "label": "Takeover"
      },
      {
        "action": "sp_handover_request",
        "label": "Handover"
      }
    ]
  }
}
```

Each row action still checks its condition and guard. A visible button is not
permission. Create this view in team with `data_scope_id` planning and object type
`shift`; keep the same scope pair for the other staff views below.

### 7.3 `sp_my_week` — "My week"

Use the same columns, filters, row actions and person binding as `sp_my_shifts`, with
a week period instead of the upcoming-only filter (confirmed in the browser: same
rows as the reference view). The period switch uses `?woche=YYYY-MM-DD`; without a
date it opens on the current week (Monday, `basis` default `woche`).
`zeitraum.key` names the English column key `day`.

```json
{
  "elements": [
    "filter",
    "table"
  ],
  "table": {
    "from": "objects",
    "type": "shift",
    "status": "active",
    "person": {
      "link": "worksShift",
      "richtung": "rueckwaerts",
      "prop": "email",
      "type": "person"
    },
    "columns": [
      {
        "key": "udid",
        "system": "udid",
        "hidden": true
      },
      {
        "key": "day",
        "prop": "shiftStart",
        "format": "wochentag_datum",
        "label": "Day"
      },
      {
        "key": "time",
        "prop": "shiftStart",
        "bis": "shiftEnd",
        "format": "zeitspanne",
        "label": "Time"
      },
      {
        "key": "station",
        "prop": "station",
        "label": "Station",
        "werte": {
          "kitchen": "Kitchen",
          "service": "Service",
          "bar": "Bar",
          "dishwashing": "Dishwashing",
          "shiftLead": "Shift lead"
        }
      },
      {
        "key": "kind",
        "prop": "shiftKind",
        "label": "Kind",
        "werte": {
          "early": "Early",
          "late": "Late",
          "split": "Split",
          "night": "Night"
        }
      },
      {
        "key": "status",
        "prop": "shiftStatus",
        "label": "Status",
        "werte": {
          "planned": "planned",
          "published": "published",
          "swapped": "swapped",
          "cancelled": "cancelled – does not take place"
        }
      }
    ],
    "filter": [
      "station",
      "status"
    ],
    "sort": {
      "key": "day",
      "dir": "asc"
    },
    "row_actions": [
      {
        "action": "sp_clock_in",
        "label": "Clock in"
      },
      {
        "action": "sp_clock_out",
        "label": "Clock out"
      },
      {
        "action": "sp_swap_request",
        "label": "Swap"
      },
      {
        "action": "sp_takeover_request",
        "label": "Takeover"
      },
      {
        "action": "sp_handover_request",
        "label": "Handover"
      }
    ],
    "zeitraum": {
      "key": "day",
      "von": "{period_start}",
      "bis": "{period_end}"
    },
    "param": "woche",
    "span": 7
  }
}
```

### 7.4 `sp_my_requests` — "My requests"

Requests and absences have different types and fields, and a block list shows one
object type. Use two views: "My requests" (confirmed in the browser: as staff only
the person's own or involved requests) and "My absences" (same pattern, still to
verify in browser). Link both from the staff front page.

The creation recipes in phase 2 link request/absence → person, so the binding uses
`richtung: vorwaerts`. It shows requests involving the viewer — as requester
(`requestedBy`) or as named partner (`takingOver`); it grants no decision actions. A
deployment using person → request instead must use `rueckwaerts` to match its actual
link direction.

```json
{"elements": ["filter", "table"],
 "table": {"from": "objects", "type": "changeRequest", "status": "active",
  "person": {"link": "concerns", "richtung": "vorwaerts", "prop": "email", "type": "person"},
  "columns": [
    {"key": "kind", "prop": "requestKind", "label": "Kind",
     "werte": {"swap": "Swap", "takeover": "Takeover", "handover": "Handover", "shiftRequest": "Shift request"}},
    {"key": "subject", "system": "name", "label": "Request"},
    {"key": "status", "prop": "changeStatus", "label": "Status",
     "werte": {"proposed": "Requested", "accepted": "Accepted", "rejected": "Rejected"}},
    {"key": "updated", "system": "modified", "format": "wochentag_datum_zeit", "label": "Last change"}],
  "filter": ["kind", "status"],
  "sort": {"key": "updated", "dir": "desc"}}}
```

Companion view `sp_my_absences` — "My absences" (confirm in the browser):

```json
{"elements": ["filter", "table"],
 "table": {"from": "objects", "type": "absence", "status": "active",
  "person": {"link": "concerns", "richtung": "vorwaerts", "prop": "email", "type": "person"},
  "columns": [
    {"key": "kind", "prop": "absenceKind", "label": "Kind",
     "werte": {"vacation": "Vacation", "sick": "Sick", "dayOffWish": "Day-off wish", "training": "Training", "availability": "Availability"}},
    {"key": "from", "prop": "absenceStart", "format": "datum", "label": "From"},
    {"key": "to", "prop": "absenceEnd", "format": "datum", "label": "Until"},
    {"key": "status", "prop": "absenceStatus", "label": "Status",
     "werte": {"requested": "Requested", "approved": "Approved", "rejected": "Rejected"}}],
  "filter": ["kind", "status"],
  "sort": {"key": "from", "dir": "desc"}}}
```

`absenceNote` is not shown (no diagnosis surface, country module §3).

### 7.5 `sp_open_shifts` — "Open shifts for me"

`ohne_link` removes staffed shifts; `passt` compares the shift's station target
(`concerns` / `station`) with the viewer's qualification target (`concerns` /
`qualifiedFor`). Use the English link values of phases 0–2. `passt` satisfies the
team-door person binding. No nested link chain is needed. Confirmed in the browser:
as a staff member the view lists exactly the unstaffed open shifts of the stations
the person is qualified for, the same rows as the reference view. The `{today}`
filter is an addition of this skill (past open shifts cannot be requested).

```json
{
  "elements": [
    "filter",
    "table"
  ],
  "table": {
    "from": "objects",
    "type": "shift",
    "status": "active",
    "ohne_link": {
      "link": "worksShift",
      "richtung": "rueckwaerts"
    },
    "passt": {
      "link": "concerns",
      "mein_value": "qualifiedFor",
      "objekt_value": "station",
      "type": "space"
    },
    "wo": [
      {
        "prop": "shiftStatus",
        "op": "=",
        "wert": "open"
      },
      {
        "prop": "shiftStart",
        "op": ">=",
        "wert": "{today}"
      }
    ],
    "columns": [
      {
        "key": "udid",
        "system": "udid",
        "hidden": true
      },
      {
        "key": "day",
        "prop": "shiftStart",
        "format": "wochentag_datum",
        "label": "Day"
      },
      {
        "key": "time",
        "prop": "shiftStart",
        "bis": "shiftEnd",
        "format": "zeitspanne",
        "label": "Time"
      },
      {
        "key": "station",
        "prop": "station",
        "label": "Station",
        "werte": {
          "kitchen": "Kitchen",
          "service": "Service",
          "bar": "Bar",
          "dishwashing": "Dishwashing",
          "shiftLead": "Shift lead"
        }
      }
    ],
    "filter": [
      "station"
    ],
    "sort": {
      "key": "day",
      "dir": "asc"
    },
    "row_actions": [
      {
        "action": "sp_shift_request",
        "label": "Request shift"
      }
    ]
  }
}
```

The example selects `shiftStatus = open`, the unstaffed state in this skill. Do not
also require `published`: phase 1 publishes staffed shifts, and these are mutually
exclusive values. Check matching with both a qualified and an unqualified account.

A simple "Open shifts" table without `passt` can be used by managers in planning
(`access.require: write`). Do not remove `passt` from a staff door to bypass binding.

### 7.6 Staff front page

`sp_my_area` is optional: link "My shifts", "My week", "My requests", "My absences"
and "Open shifts for me", plus Request absence (day-off wish) on the own person.
A composite `elements: ["blocks"]` page remains optional (confirm the exact
container syntax). The required views above do not depend on it.

No planning membership and no copies of shifts into team are needed.

## 8. Start card "My shifts"

A start card links a view for everybody who can read its scope **and** sees the view.
It has no roles.

```json
{"tool": "onto_startcard_save", "arguments": {"scope_id": <team_scope_id>, "iface": "sp_my_shifts", "title": "My shifts"}}
```

- The view must belong to the card's scope (team); a view of another scope is refused
  ("view does not belong to this scope").
- Saving needs **manage** on the scope; staff never see the configuration page (403)
  and get no menu entry.
- `onto_startcard_index` lists cards with `id` and `sort_order`; reorder with
  `onto_startcard_move` (`id`, `dir` = `up`/`down`); remove with `onto_startcard_delete`.
- The required card points at `sp_my_shifts`; check as staff that the card opens the
  own shifts.

## 9. Recipe (tool order with example arguments)

```json
[
  {"tool": "create_invite_code", "arguments": {"scope_id": <team_scope_id>, "kind": "management", "max_uses": 1, "label": "TEST-3 staff cook", "expires": "2026-12-31"}},
  {"tool": "ontouser_team_index", "arguments": {"scope_id": <team_scope_id>}},
  {"tool": "ontouser_team_set_scope_rights", "arguments": {"profile_id": <staff_profile_id>, "scope_id": <master_scope_id>, "can_read": 1, "can_write": 0, "can_manage_scope": 0}},
  {"tool": "ontouser_team_set_scope_rights", "arguments": {"profile_id": <staff_profile_id>, "scope_id": <team_scope_id>, "can_read": 1, "can_write": 1, "can_manage_scope": 0}},
  {"tool": "ontouser_team_show", "arguments": {"profile_id": <staff_profile_id>}},
  {"tool": "ontouser_team_transfer", "arguments": {"to_profile_id": <staff_profile_id>, "credits": 200, "reason": "TEST-3 staff test balance", "idempotency_key": "trattoria-test3-cook-200"}},

  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_my_next_shift", "...": "see 7.1"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_my_shifts", "...": "see 7.2"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_my_week", "...": "see 7.3"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_my_requests", "...": "see 7.4, type changeRequest"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_my_absences", "...": "see 7.4, type absence"}},
  {"tool": "onto_interface_create_def", "arguments": {"name": "sp_open_shifts", "...": "see 7.5"}},
  {"tool": "onto_interface_show", "arguments": {"name": "sp_my_shifts"}},
  {"tool": "onto_startcard_save", "arguments": {"scope_id": <team_scope_id>, "iface": "sp_my_shifts", "title": "My shifts"}},
  {"tool": "onto_startcard_index", "arguments": {}},

  {"tool": "onto_trigger_create", "arguments": {"key": "sp_msg_first_publication", "...": "see 6.1"}},
  {"tool": "onto_trigger_create", "arguments": {"key": "sp_msg_assignment_removed", "...": "see 6.1"}},
  {"tool": "onto_trigger_index", "arguments": {"limit": 200}},

  {"tool": "onto_object_execute_action", "arguments": {"action_key": "sp_shift_publish", "udid": "<shift_udid of the staff test account>"}},
  {"tool": "ontouser_notification_index", "arguments": {}}
]
```

Order: accounts and rights → staff views → start card → notification rules (e-mail
and push off) → publish one test shift → check messages → acceptance → switch e-mail
and push on. The exact arguments of `create_invite_code` (expiry field name) come from
the platform skill (confirm).

## 10. Smoke tests

| # | Call / check | Expected |
|---|---|---|
| S10 | `ontouser_team_show` (each managed account) | memberships exactly as in the rights table: staff = master **read**, **no** planning membership, team read+write; shift lead as listed |
| S11 | browser as staff: open team views; try a manager/planning view URL | team views show **only own** rows; direct open of a manager view is **refused** |
| P3-1 | `onto_object_show` master person of the staff account | `email` = login; no pay, health or private contact fields |
| P3-2 | read `sp_my_shifts`, `sp_my_week`, `sp_my_requests`, `sp_my_absences`, `sp_open_shifts` | team scope, `data_scope_id` planning; `person` or `passt` binding; definitions as in §7 |
| P3-3 | `onto_startcard_index` | card "My shifts" in the team scope pointing at the team view |
| P3-4 | `onto_startcard_save` with a view of another scope | refused |
| P3-5 | publish a staffed test shift, wait ≤ 5 min | the staffed person has "Shift published"; marker `sent`; nobody else got a message |
| P3-6 | publish nothing new, wait two ticks | no second message (marker) |
| P3-7 | cancel the published shift | only the persons on it get "cancelled" |
| P3-8 | `sp_shift_release` on a published shift | only the removed person gets "no longer on …"; no "you are now on" message |
| P3-9 | approve a swap (phase 2) | requester and partner each get their message; the old assignment message to the requester; third persons nothing |
| P3-10 | reject a shift request | only the requester |
| P3-11 | approve a day-off wish | only the person |
| P3-12 | staff account: `onto_credit_balance` after its actions | balance reduced by its own action runs only |
| P3-13 | staff account: "Request shift" on a row of "Open shifts for me" | request created in planning, `requestedBy` = own person; shift unchanged; the new request appears in "My requests" (worth confirming with a staff account) |

## 11. Browser checks

| Role | Check | Expected |
|---|---|---|
| staff | log in → start page | panel "start cards for the team" shows "My shifts"; no menu entry for start cards or team management |
| staff | open "My shifts" | only own shifts; cancelled marked; buttons only on own rows |
| staff | open "My next shift" | exactly one row (the next own shift) or none |
| staff | own person → Request absence → Day-off wish | request created; appears in "My absences" as requested |
| staff | My week / My requests | correct period and only own or involved rows |
| staff | My absences | only own absences (confirm in the browser) |
| staff | Open shifts for me | unstaffed future shifts at qualified stations only |
| staff | open a colleague's shift or a manager view by URL (week list, inbox, payroll) | refused / redirected |
| staff | read colleagues on master | only basic fields (name, login e-mail, stations); no pay, health, private contact |
| staff | after a published shift | in-app message; e-mail/push only after they are switched on |
| manager | start card configuration page | card listed, reorder and delete work |

## 12. Failure patterns

| Symptom | Cause | Fix |
|---|---|---|
| team view empty for a staff member | person `email` differs from the login (case, typo) | fix `email` on the master person |
| team view refused on save | no person binding with `data_scope_id` | add the documented `person` block (or `passt` for matching open shifts) |
| placeholder rejected by the validator | explicit e-mail filter in the person-base view without single quotes | in `sp_my_next_shift` write `{'current_user_email'}`; the `person` block of the other staff views needs no placeholder |
| staff sees colleagues' shifts | binding missing, or planning read granted | fix the view; remove planning membership |
| first-publication message twice | marker not set by the rule, or reset by an action | `set_property firstNoticeStatus = sent` in the same rule; never reset it |
| no first-publication message | `firstNoticeStatus` already `sent`, or no linked recipient | check the marker and linked persons; old published shifts with `open` are processed by the schedule rule too |
| everybody on a request got the message | `to_linkvalue` missing | add it |
| message text ends with "Shift: ." | prefix before an empty `{linked:…}` | put the placeholder last, no prefix |
| no message after release | link type not listed in `link_types` of the `link_removed` rule | list `worksShift` |
| staff click does nothing / dialog hangs | staff account has no credits (402) | top up with `ontouser_team_transfer` |
| a button without prompts opens no dialog | prompt-less action in a team view | give every staff action at least one optional prompt with a default |
| start card missing for staff | staff cannot read the card's scope, or the view is hidden for them (`access.require`) | card in the team scope, view readable for staff |

## 13. Checks after phase 3

Run these once in your workspace; they are part of the acceptance scenario
([acceptance-scenario.md](acceptance-scenario.md), section 7):

- a staff account opens "My absences" (§7.4) and requests an open shift that is not
  yet linked to it (P3-13) — both work with staff rights only;
- the first publication produces one plan summary, not one message per shift;
- a handover notifies the person picked, and adding a person to an already published
  shift notifies that person without a status change.
