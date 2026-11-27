# Forms and actions — handover, return and defects

The handover and return forms follow the measured inspection path, applied
twice. The defect form follows the measured `report_defect` path on a
`building`. Photos and signatures belong in a formdef, not in action prompts.
Action prompts do not accept those widget types. Bind each action as
`form_answer`.

Create each action with **exactly one** scope in `body.scopes` (the venue
scope; for `report_defect`, create first with the master scope), then add the
team scope in a second save. `result_scope_id` is `<venue_scope_id>`.
`assignedTo={current_user_email}` is required when `result_scope_id` is set.
Condition operator is `ne`, not `neq`.

Empty form fields are not stored. A trigger placeholder for a blank field stays
as literal text. Trigger placeholders must match the form widget keys exactly
(lowercase keys such as `lastdone`, not `lastDone`). In function effects,
`{result}` is the function result; name the condition result input `inspResult`.

## 1. Shared handover and return form fields

Both forms live in the team scope, `answer_type` `serviceOrder`. Widget keys are
stored as written; keep them lowercase. Form date fields use widget `datepicker`
with `mode: date` and value `YYYY-MM-DD`.

| Key | Widget | Required | Notes |
|---|---|---|---|
| `result` | select `pass` / `defect` | yes | condition of the venue at this handover |
| `note` | textarea | no | inventory, cleanliness and damage notes |
| `keyset` | textarea | yes | keys handed over or returned |
| `meters` | textarea | no | meter readings as the caretaker already writes them |
| `images` | `images` | yes | `max` 5; validation `min_count:1` |
| `handedoverby` | `signature` | — | signature of the caretaker or chair handing over; stored as a PNG on the protocol |
| `receivedby` | `signature` | — | signature of the hirer receiving; stored as a PNG on the protocol |
| `lastdone` | `datepicker`, `mode: date` | yes | date of this protocol, `YYYY-MM-DD` |
| `orderKind` | select, only the protocol kind below | yes | classifies the protocol |
| `orderStatus` | select, only `done` | yes | keeps the protocol off the open-booking lists |

Each form has one `images` widget and two `signature` widgets with distinct
keys (`handedoverby`, `receivedby`). A form may have two `signature` fields;
this has been tested. Handover and return remain two protocols because they
happen at different times; each protocol carries both signatures.
Inventory and meters are text areas; the business types the list it already uses.

The `keyset`, `meters`, `handedoverby` and `receivedby` widget keys are lowercase. Do not send `keySet`, `meterReading`, `handedOverBy` or `receivedBy` as form keys if you want the values stored under the keys above.

## 2. Action `record_handover`

Type `form_answer` on `serviceOrder`, bound to the handover form (`orderKind`
only `handoverProtocol`). Condition: `orderStatus` is `open` or `inProgress`,
and `orderKind` `ne` `handoverProtocol` and `ne` `returnProtocol` and `ne`
`defect`.

Action props:

```json
{
  "orderKind": "handoverProtocol",
  "orderStatus": "done",
  "assignedTo": "{current_user_email}"
}
```

Link: `concerns` with `linkvalue` `ofOrder` to `{object_udid}` (the booking the
button was run on). Protocol name, for example `Handover {now}`.

## 3. Action `record_return`

Same pattern. The return form fixes `orderKind` to `returnProtocol`. Condition:
`orderStatus` is `open` or `inProgress`, and `orderKind` `ne` `handoverProtocol`
and `ne` `returnProtocol` and `ne` `defect`. Props use
`orderKind=returnProtocol`, `orderStatus=done`,
`assignedTo={current_user_email}`. The same `ofOrder` link. Protocol name,
for example `Return {now}`.

## 4. Functions and triggers

Create both functions in the venue scope.

### `apply_handover`

Inputs: `objekt` (object, required — the **booking**, not the protocol),
`inspResult` (string, required), `note` (string, optional), `keyset` (string,
required), `meters` (string, optional), `lastdone` (datetime, required).

Effects, `set_property` on `objekt`: `result`=`{inspResult}`,
`inspectionNote`=`{note}`, `keySet`=`{keyset}`, `lastDone`=`{lastdone}`,
`orderStatus`=`inProgress`. Do not set `completedAt`. Do not close the booking
at handover.

### `apply_return`

Same inputs. Effects, `set_property` on `objekt`: `result`=`{inspResult}`,
`inspectionNote`=`{note}`, `keySet`=`{keyset}`, `lastDone`=`{lastdone}`,
`orderStatus`=`done`.

A booking is a one-off hire, so the return function closes the booking and the
row leaves the open lists. That is a deliberate difference from recurring
inspection duties, which stay open. Read the booking back after the first
return save and quote `orderStatus`.

### Triggers

All in the venue scope, object type `serviceOrder`, enabled.

| Key | Event | Condition | Function |
|---|---|---|---|
| `on_handover_recorded` | insert | `orderKind` `eq` `handoverProtocol` | `apply_handover` |
| `on_handover_recorded_update` | update | same, plus `changed`: `result`, `lastdone`, `keyset`, `meters` | `apply_handover` |
| `on_return_recorded` | insert | `orderKind` `eq` `returnProtocol` | `apply_return` |
| `on_return_recorded_update` | update | same, plus `changed`: `result`, `lastdone`, `keyset`, `meters` | `apply_return` |

Function inputs on all four (placeholders = exact form widget keys):

```json
{
  "objekt": "{linked:concerns:ofOrder:udid}",
  "inspResult": "{result}",
  "note": "{note}",
  "keyset": "{keyset}",
  "meters": "{meters}",
  "lastdone": "{lastdone}"
}
```

`{linked:concerns:ofOrder:udid}` resolves the booking. `{result}` here is the
protocol's `result` field, not the function result. If `meters` was left empty,
do not write the literal `{meters}` onto the booking; skip that property when
the value is not real text.

## 5. Form and action `report_defect`

Form in the team scope, `answer_type` `serviceOrder`. Fields:

| Key | Required | Notes |
|---|---|---|
| `task` | yes | short title |
| `description` | yes | description of the defect |
| `orderKind` | — | fixed to `defect` |
| `orderStatus` | — | fixed to `open` |

Action type `form_answer`, object type `building` (and `space` only when
`onto_link_index` has confirmed `concerns` / `ofAsset` for that pair). Create
with `body.scopes` = `[<master_scope_id>]` and `result_scope_id` =
`<venue_scope_id>`, then add the team scope in a second save. Bind the form.
Props: `orderKind=defect`, `orderStatus=open`,
`assignedTo={current_user_email}`. Link: `concerns` with `linkvalue` `ofAsset`
to the venue the action was run on.

The new order lands in the venue scope, appears in `defects` / `team_defects`,
and must not appear in the open-booking lists.

## 6. Typical errors

- Action prompts used for photos or a signature → put them in the formdef (two `signature` fields if both parties sign) and
  set `action.type=form_answer`.
- Action condition operator `neq` instead of `ne` → the button does not show.
- Missing hidden `udid` column on the list → the row action has no object.
- Trigger placeholders in camelCase (`{keySet}`, `{lastDone}`) → the values
  are not passed.
- `{result}` used as a function input name → it collides with the function result.
- `ofOrder` missing on the protocol → the function cannot find the booking.
- `assignedTo` omitted on a `form_answer` with `result_scope_id` → HTTP 400.
- Action create with several scopes → HTTP 400, nothing stored.
- `orderStatus=done` written onto the booking at handover → the booking leaves
  the in-progress and open lists too early.
- All open bookings missing `orderKind = venueBooking` (or failing to exclude
  `defect`) → a newly reported defect leaks into the booking count.
