# Tool traps — maintenance and inspection deadlines

Read the platform list first:
[tool-traps.md](../../../telesherpa-ontology-platform/references/features/tool-traps.md).
This file only adds traps that showed up while building this solution.

1. **Photos and signature go in a formdef, not in action prompts.** Action
   prompts accept only `text`, `textarea`, `int`, `float`, `select`, `picker`,
   `switch`, `date`, `datetime` and `time`. Use widgets `images` and
   `signature`, and set the action to `form_answer` with `action.form` bound
   to that formdef.
2. **Form date fields use widget `datepicker` with `mode: date`.** Send
   `YYYY-MM-DD`. A date-time value on a date property is rejected with HTTP
   400 and nothing is written.
3. **Empty form fields are not stored.** A trigger placeholder for a blank
   field stays as literal text (for example `{nextduedate}`). `apply_inspection`
   must accept `nextduedate` only when it matches `YYYY-MM-DD`; otherwise it
   uses `date_add(lastdone, intervalDays)`.
4. **Trigger placeholders must match the form widget keys exactly.** The
   stored keys are `lastdone`, `nextduedate`, `result` and `note`, not
   camelCase (`lastDone`, `nextDueDate`). A mismatch means the value is not
   passed.
5. **The function input for the inspection result is `inspResult`.** In
   function effects, `{result}` is the function result (the computed due
   date), not the inspection result.
6. **Action conditions use operator `ne`, not `neq`.** A condition written
   with `neq` can hide the button. View filters use `!=`, `<`, `>=`, `<=`.
7. **List row actions need a hidden `udid` column.** Without it, the button
   has no object and does not open the form.
8. **Create an action with exactly one entry in `body.scopes`.** Adding several
   scopes on create is rejected (HTTP 400) and nothing is stored. Save once, then
   add the other scopes in a second save. A `form_answer` with `result_scope_id`
   also needs `assignedTo={current_user_email}`.
9. **`ontouser_scope_types_set` replaces the list.** Activating `serviceOrder`
   without including the types already on the scope will drop them.
10. **Empty `ofAsset` looks like a missing asset.** The lists join the asset
    through `concerns` with linkvalue `ofAsset`. Update the existing edge; do not
    create a second `concerns` link.
11. **Closing the duty hides it.** `apply_inspection` must not write
    `orderStatus=done` or `completedAt` on the duty. Only the protocol is
    `done`. The same open row is the next deadline.
12. **Missing `ofOrder` on the protocol** means the function cannot find the
    duty and the due date is not updated.
13. **`result=defect` on the form does not create a defect order.** Use
    `report_defect` on the asset when a defect row is required.
14. **All open inspections must exclude `orderKind=defect`.** Without that
    filter, a newly reported defect appears in the open-inspections count.
15. **Start cards cannot point at a view in another scope.** Install the team
    counterparts, then point the cards at those view names. A card aimed at a
    maintenance-scope view is rejected (HTTP 400).
16. **Do not set `data_scope_id` on the inspection lists.** Person-binding hides
    unassigned orders.
17. **One write at a time.** Parallel `onto_object_create_link` calls can time
    out. Read the graph, then create only the edges that are still missing.
18. **`remove: true` is still the general unlink trap.** If you ever detach a
    link, use `remove: "pair"`.
19. **Prices come from `onto_credit_pricing` today.** A table in another skill
    or in yesterday's log is not the price. Quote the live key and the number
    you read; do not copy a figure from this skill.
