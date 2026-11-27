# Forms and actions — collection and delivery reports

This is the measured inspection path, applied twice: one form for the collection
condition report, one form for the delivery condition report and handover.
Photos and signatures belong in a formdef, not in action prompts. Action
prompts do not accept those widget types. Bind each action as `form_answer`.

Create each action with **exactly one** scope in `body.scopes` (the transport
scope), then add the team scope in a second save. `result_scope_id` is
`<transport_scope_id>`. `assignedTo={current_user_email}` is required when
`result_scope_id` is set. Condition operator is `ne`, not `neq`.

Empty form fields are not stored. A trigger placeholder for a blank field stays
as literal text. Trigger placeholders must match the form widget keys exactly
(lowercase keys such as `lastdone`, not `lastDone`). In function effects,
`{result}` is the function result; name the condition result input `inspResult`.

## 1. Shared form fields

Both forms live in the team scope, `answer_type` `serviceOrder`. Widget keys are
stored as written; keep them lowercase. Form date fields use widget `datepicker`
with `mode: date` and value `YYYY-MM-DD`.

| Key | Widget | Required | Notes |
|---|---|---|---|
| `result` | select `pass` / `defect` | yes | condition at this handover |
| `note` | textarea | no | observed condition, packing or damage notes |
| `images` | `images` | yes | `max` 5; validation `min_count:1` |
| `handedoverby` | `signature` | — | signature of the party handing over; stored as a PNG on the protocol |
| `receivedby` | `signature` | — | signature of the party receiving; stored as a PNG on the protocol |
| `lastdone` | `datepicker`, `mode: date` | yes | date of this report, `YYYY-MM-DD` |
| `orderKind` | select, only the protocol kind below | yes | classifies the protocol |
| `orderStatus` | select, only `done` | yes | keeps the protocol off the open-job lists |

Each form has one `images` widget and two `signature` widgets with distinct
keys (`handedoverby`, `receivedby`). A form may have two `signature` fields;
this has been tested. Collection and delivery remain two protocols because they
happen at different times; each protocol carries both signatures.
The widget keys are lowercase. Do not send `handedOverBy` or `receivedBy` as
form keys.

## 2. Action `record_collection`

Type `form_answer` on `serviceOrder`, bound to the collection form
(`orderKind` only `collectionReport`). Condition: `orderStatus` is `open` or
`inProgress`, and `orderKind` `ne` `collectionReport` and `ne` `deliveryReport`.

Action props:

```json
{
  "orderKind": "collectionReport",
  "orderStatus": "done",
  "assignedTo": "{current_user_email}"
}
```

Link: `concerns` with `linkvalue` `ofOrder` to `{object_udid}` (the job the
button was run on). Protocol name, for example `Collection report {now}`.

## 3. Action `record_delivery`

Same pattern. The delivery form fixes `orderKind` to `deliveryReport`.
Condition: `orderStatus` is `open` or `inProgress`, and `orderKind` `ne`
`collectionReport` and `ne` `deliveryReport`. Props use
`orderKind=deliveryReport`, `orderStatus=done`,
`assignedTo={current_user_email}`. The same `ofOrder` link. Protocol name,
for example `Delivery report {now}`.

## 4. Functions and triggers

Create both functions in the transport scope.

### `apply_collection`

Inputs: `objekt` (object, required — the **job**, not the protocol),
`inspResult` (string, required), `note` (string, optional), `lastdone`
(datetime, required).

Effects, `set_property` on `objekt`: `result`=`{inspResult}`,
`inspectionNote`=`{note}`, `lastDone`=`{lastdone}`, `orderStatus`=`inProgress`.
Do not set `completedAt`. Do not close the job at collection.

### `apply_delivery`

Same inputs. Effects, `set_property` on `objekt`: `result`=`{inspResult}`,
`inspectionNote`=`{note}`, `lastDone`=`{lastdone}`, `orderStatus`=`done`.

A transport job is a one-off move, so the delivery function closes the job and
the row leaves the open lists. That is a deliberate difference from recurring
inspection duties, which stay open. Read the job back after the first delivery
save and quote `orderStatus`.

### Triggers

All in the transport scope, object type `serviceOrder`, enabled.

| Key | Event | Condition | Function |
|---|---|---|---|
| `on_collection_recorded` | insert | `orderKind` `eq` `collectionReport` | `apply_collection` |
| `on_collection_recorded_update` | update | same, plus `changed`: `result`, `lastdone` | `apply_collection` |
| `on_delivery_recorded` | insert | `orderKind` `eq` `deliveryReport` | `apply_delivery` |
| `on_delivery_recorded_update` | update | same, plus `changed`: `result`, `lastdone` | `apply_delivery` |

Function inputs on all four (placeholders = exact form widget keys):

```json
{
  "objekt": "{linked:concerns:ofOrder:udid}",
  "inspResult": "{result}",
  "note": "{note}",
  "lastdone": "{lastdone}"
}
```

`{linked:concerns:ofOrder:udid}` resolves the job. `{result}` here is the
protocol's `result` field, not the function result.

## 5. Typical errors

- Action prompts used for photos or a signature → put them in the formdef (two `signature` fields if both parties sign) and
  set `action.type=form_answer`.
- Action condition operator `neq` instead of `ne` → the button does not show.
- Missing hidden `udid` column on the list → the row action has no object.
- Trigger placeholders in camelCase → the values are not passed.
- `{result}` used as a function input name → it collides with the function result.
- `ofOrder` missing on the protocol → the function cannot find the job.
- `assignedTo` omitted on a `form_answer` with `result_scope_id` → HTTP 400.
- Action create with several scopes → HTTP 400, nothing stored.
- `orderStatus=done` written onto the job at collection → the job leaves the
  in-progress and open lists too early.
