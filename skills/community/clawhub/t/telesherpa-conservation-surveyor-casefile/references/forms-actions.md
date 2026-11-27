# Forms and actions — record a survey

This is the measured inspection path: the form collects the values, the action
creates a protocol, the triggers run `apply_survey`, and the function updates
the case. Photos and signatures belong in a formdef, not in action prompts.
Action prompts do not accept those widget types. Bind the action as
`form_answer`.

Create the action with **exactly one** scope in `body.scopes` (the cases
scope), then add the team scope in a second save. `result_scope_id` is
`<cases_scope_id>`. `assignedTo={current_user_email}` is required when
`result_scope_id` is set. Condition operator is `ne`, not `neq`.

Empty form fields are not stored. A trigger placeholder for a blank field stays
as literal text. `apply_survey` must accept `nextduedate` only when it matches
`YYYY-MM-DD`; otherwise, when `intervalDays` is set on the case, it uses
`date_add(lastdone, intervalDays)`. Trigger placeholders must match the form
widget keys exactly (lowercase keys such as `lastdone` and `nextduedate`). In
function effects, `{result}` is the function result (the computed due date);
name the survey result input `inspResult`.

## 1. Form (team scope)

`answer_type` `serviceOrder`. Widget keys are stored as written; keep them
lowercase. Form date fields use widget `datepicker` with `mode: date` and
value `YYYY-MM-DD`.

| Key | Widget | Required | Notes |
|---|---|---|---|
| `result` | select `pass` / `defect` | yes | overall outcome of this visit |
| `note` | textarea | yes | findings as written text |
| `images` | `images` | yes | `max` 5; validation `min_count:1` |
| `signature` | `signature` | — | signature of the conservator or surveyor; stored as a PNG on the protocol |
| `confirmedby` | `signature` | no | optional client confirmation; stored as a PNG on the protocol |
| `lastdone` | `datepicker`, `mode: date` | yes | survey date, `YYYY-MM-DD` |
| `nextduedate` | `datepicker`, `mode: date` | no | next deadline, `YYYY-MM-DD`; leave empty to use the interval when one is set |
| `orderKind` | select, only `surveyProtocol` | yes | classifies the protocol |
| `orderStatus` | select, only `done` | yes | keeps the protocol off the open-case lists |

The form has one `images` widget and two `signature` widgets with distinct
keys: `signature` for the conservator or surveyor, and optional `confirmedby`
for client confirmation when the intake uses it. A form may have two
`signature` fields; this has been tested. The findings belong in the `note`
textarea. Do not add a drawing layer on the photographs.
The widget key `confirmedby` is lowercase. Do not send `confirmedBy` as a form key.

## 2. Action `record_survey`

Type `form_answer` on `serviceOrder`, bound to the form above. Condition:
`orderStatus` is `open` or `inProgress`, and `orderKind` `ne` `surveyProtocol`.

Action props:

```json
{
  "orderKind": "surveyProtocol",
  "orderStatus": "done",
  "assignedTo": "{current_user_email}"
}
```

Link: `concerns` with `linkvalue` `ofOrder` to `{object_udid}` (the case the
button was run on). Protocol name, for example `Survey {now}`.

The protocol lands in the cases scope. It must not appear in the open, overdue
or due-window lists (`orderStatus=done`).

## 3. Function `apply_survey`

Create in the cases scope. Inputs:

| Key | Type | Required | Meaning |
|---|---|---|---|
| `objekt` | object | yes | the **case**, not the protocol |
| `inspResult` | string | yes | survey result (`pass` / `defect`) |
| `note` | string | yes | becomes `inspectionNote` |
| `lastdone` | datetime | yes | survey date |
| `nextduedate` | datetime | no | typed next due date, if any |

Body: if `nextduedate` is not empty **and** matches `^[0-9]{4}-[0-9]{2}-[0-9]{2}`,
use that value; otherwise, if `intervalDays` on the case (`objekt`) is a
positive integer, `date_add(lastdone, intervalDays)`; otherwise leave
`dueDate` unchanged. Never treat the literal text `{nextduedate}` as a date.

For a one-off expert report with no follow-up interval, the next due date is
typed on the form, or it stays the deadline already on the case.

Effects, `set_property` on `objekt` (the case):

```json
{
  "result": "{inspResult}",
  "inspectionNote": "{note}",
  "lastDone": "{lastdone}",
  "dueDate": "{result}"
}
```

When the body leaves `dueDate` unchanged, omit the `dueDate` effect rather than
writing a blank or a placeholder. Do **not** set `orderStatus`, `completedAt`
or `description` on the case. After a successful run the case is still `open`
(or still `inProgress`).

## 4. Triggers

Both in the cases scope, object type `serviceOrder`, enabled.

| Key | Event | Condition | Effect |
|---|---|---|---|
| `on_survey_recorded` | insert | `orderKind` `eq` `surveyProtocol` | `run_function` `apply_survey` |
| `on_survey_recorded_update` | update | same, plus `changed`: `result`, `lastdone`, `nextduedate` | same function and inputs |

Function inputs on both triggers (placeholders = exact form widget keys):

```json
{
  "objekt": "{linked:concerns:ofOrder:udid}",
  "inspResult": "{result}",
  "note": "{note}",
  "lastdone": "{lastdone}",
  "nextduedate": "{nextduedate}"
}
```

`{linked:concerns:ofOrder:udid}` resolves the case. `{result}` here is the
protocol's `result` field, not the function result.

## 5. Typical errors

- Action prompts used for photos or a signature → put them in the formdef (two `signature` fields when the client also confirms) and
  set `action.type=form_answer`.
- Action condition operator `neq` instead of `ne` → the button does not show.
- Missing hidden `udid` column on the list → the row action has no object.
- Empty `nextduedate` written through as the literal `{nextduedate}` → guard
  with the `YYYY-MM-DD` pattern; otherwise use `date_add` only when
  `intervalDays` is a positive integer.
- Trigger placeholders in camelCase → the values are not passed.
- `{result}` used as a function input name → it collides with the function result.
- `orderStatus=done` written onto the **case** → the row disappears from every
  open list. Only the protocol is `done`.
- `ofOrder` missing on the protocol → the function cannot find the case.
- `assignedTo` omitted on a `form_answer` with `result_scope_id` → HTTP 400.
- Action create with several scopes → HTTP 400, nothing stored.
