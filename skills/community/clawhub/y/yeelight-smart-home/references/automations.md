# Automations

Use this reference for automation rules and schedules.

- Use `automation.create` when the user wants a new persistent rule. Runtime must return a pending plan; after confirmation, `plan.commit` re-validates, creates the automation, and verifies it through the automation list.
- Use `automation.supported.list` or `automation.supported.v2.list` when the user asks what automation conditions/actions are supported or when a future automation write needs source-backed capability evidence.
- Use `automation.list` when the user asks for all saved automations in one home or when a follow-up update/delete/toggle needs a complete home-level automation candidate list.
- Use `automation.list.page` when the user asks to browse, count, or review saved automations with pagination.
- Use `automation.detail.get` when the user asks to inspect one existing automation's conditions, schedule, actions, repeated rules, or impact before an update.
- Use `schedule_job.list` when the user asks for saved timed jobs, scheduled actions, or legacy schedule-task style rules in one home.
- Use `automation.rule.list` when the user asks for automation rule details or rule-level impact evidence.
- Use `automation.update` for changing conditions, time windows, actions, or names. It requires a complete rule payload, returns a pending plan, and must not be used as a partial patch.
- Use `automation.enable` and `automation.disable` only when the user asks to toggle an existing automation. Runtime returns a pending plan and verifies the saved automation status after commit.
- Use `automation.delete` only when the user explicitly asks to delete one automation. Runtime must return a pending plan, re-check the automation, and verify removal after commit.
- Use `automation.batch_delete` only when the user explicitly asks to delete multiple automations. Runtime caps one plan at 20 automations, resolves each target by id or unique name, and verifies every automation disappeared from `entity.list`.
- Use `automation.explain` for "why", "what does this rule do", or rule audit requests.
- Use `automation.capabilities` when the user asks what automation creation, update, toggle, diagnosis, or delete capabilities are currently available in this Runtime.
- Missing devices, sensors, events, actions, or time details should become the smallest clarification question.
- Never invent sensors, events, actions, gateway behavior, or background execution results.
- Treat new or changed automations as persistent R2 configuration; commit only by returned `planId`. Update and toggle plans ignore model-supplied mutation fields during commit and execute only the stored local plan.
- Treat `automation.capabilities` as policy evidence, not as proof that every named automation action can be executed.
- Do not put status changes inside `automation.update`; use `automation.enable` or `automation.disable` for existing automation state.
- For safety, a newly planned automation should not be described as enabled or running unless Runtime says so. Status values are Runtime evidence, not wording to infer manually.
- Automation condition candidates include presence, motion, contact, illuminance, button, knob, time window, duration, and threshold only after Runtime validates the entity and event.
- Automation action vocabulary may include executing a scene, room/area on-off, brightness or color-temperature adjustment, light power/brightness/color-temperature/RGB, curtain position, and multi-channel switch state. Keep these as planning words; Runtime validates actual support.
- Timing words such as delayed execution, delayed off, duration, repeat window, and active time range are allowed only as parameters for Runtime planning.
- Dynamic light flow, curtain motor action, audio playback, panel action, and air-conditioning mode are product-specific; do not claim support unless Runtime returns it.
