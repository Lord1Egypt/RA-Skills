# Form engine

The form engine allows structured data capture via forms whose answers land in the ontology
as event objects.

## Concept

- **Form** = object type `form` with `formdef` JSON (field definitions).
- **Answer** = standalone event object, field values as properties.
- **Links:** `usesForm` (form→answer), `performs` (person→answer), `concerns` (answer→target object).
- **Props + scope inherit the FORMULAR scope.** Field `scope_id` = optional visibility (fail-closed).

## MCP tools (agent workflow)

For filling in via agent (not app/web): `list_formdefs` → `prepare_form_answer` →
`submit_form_answer` (once or several times with `status: draft`) → `submit_form_answer`
(`status: sent`) → optionally `show_form_answer` for checking.

- **The parameter name is `form_udid` everywhere, not `formdef_udid`** — applies to
  `prepare_form_answer`, `submit_form_answer`, `show_form_answer` and
  `resolve_form_answer`, although the underlying object is of type `form`
  (formdef JSON as property).
- **`submit_form_answer` AND `show_form_answer` both need `form_udid` AND
  `answer_udid`** (two-part route, deliberately no automatic resolution via the
  `usesForm` link). Only the `answer_udid` known (e.g. from an answer list)?
  First call `resolve_form_answer(answer_udid)` to fetch the matching `form_udid`.
- `submit_form_answer`'s `values` object lands as an `answer` property per field key from
  `show_formdef`; subform fields get a LIST of row objects as value.

## Pitfalls

- Form answers are event objects (state description at a point in time), NOT
  mutations on the target object.
- Cross-form aggregation runs via the link to the person, not via a shared object.
