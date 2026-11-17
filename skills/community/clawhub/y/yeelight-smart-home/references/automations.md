# Automations

Use this reference for automation rules and schedules.

## Intent Routing

- Use `automation.create` when the user wants a new persistent rule. Runtime validates, creates the automation, and verifies it through the automation list when supported. It needs a complete rule payload: name, active window, repeat rule, `trigger` or `conditions`, and `actions[]`.
- When the user imports a full lighting design that includes simple scheduled design intent such as "主卧每天 9 点亮起来", route to `lighting.design.import` if it is part of the requested design topology and can target keys from that design. For a standalone automation or later edit, use `automation.create` or `automation.update`.
- Use `automation.supported.list` or `automation.supported.v2.list` when the user asks what automation conditions/actions are supported or when a future automation write needs source-backed capability evidence.
- Use `automation.list` when the user asks for all saved automations in one home or when a follow-up update/delete/toggle needs a complete home-level automation candidate list.
- Use `automation.list.page` when the user asks to browse, count, or review saved automations with pagination.
- Use `automation.detail.get` when the user asks to inspect one existing automation's conditions, schedule, actions, repeated rules, or impact before an update.
- Use `schedule_job.list` when the user asks for saved timed jobs or scheduled action rules in one home.
- Use `automation.rule.list` when the user asks for automation rule details or rule-level impact evidence.
- Use `automation.update` for changing conditions, time windows, actions, or names. It requires a complete rule payload and must not be used as a partial patch.
- Use `automation.enable` and `automation.disable` only when the user asks to toggle an existing automation. Runtime validates and executes the Runtime request directly and verifies the saved automation status after execution.
- Use `automation.delete` only when the user explicitly asks to delete one automation. Runtime must validate and execute the Runtime request directly, re-check the automation, and verify removal after execution.
- Use `automation.batch_delete` only when the user explicitly asks to delete multiple automations. Runtime caps one request at 20 automations, resolves each target by id or unique name, and verifies every automation disappeared from `entity.list`.
- For `automation.batch_delete`, use `names` or `items[]` rows such as `{"name":"主卧9点开灯"}` or `{"automationId":"..."}`. Do not send `automationNames[]`.
- Use `automation.explain` for "why", "what does this rule do", or rule audit requests.
- Use `automation.capabilities` when the user asks what automation creation, update, toggle, diagnosis, or delete capabilities are currently available in this Runtime.

## Planning Checklist

- Every automation proposal needs trigger, target scope, action, active time window, repeat rule, and conflict assumptions.
- Split a reusable ambience from its trigger: create or reference a scene for the desired lighting effect, then use automation to run that scene.
- Prefer minimum blast radius. A room sensor should normally affect that room or a path, not the whole home.
- For safety and comfort, add time windows or illuminance checks to motion-triggered lighting when the user's wording allows it.
- Use different no-motion delays by room role: short for corridor or bathroom, longer for living room or study, and explicit confirmation for bedroom.
- Ask one smallest question if any required piece is missing: target room/device, trigger device, time window, repeat days, action, or whether to enable after creation.
- Do not silently add a sensor, scene, room, group, or device if the rule would need one. Present it as a missing dependency or recommendation candidate.
- A design slot can be created for planning future lights, but it is not a live sensor or controllable device. Keep slot-based automations as design metadata unless Runtime confirms a supported automation payload.
- For user's typo or vague wording, preserve the utterance and ask Runtime to resolve; do not manually construct event IDs or product IDs.

## Recommended Patterns

- Presence plus time window: good for corridor, entrance, bathroom, and night path light.
- Illuminance plus occupancy: avoids turning lights on when daylight is enough.
- Schedule plus gradual transition: good for wake-up, sleep preparation, and daily routines.
- Door/contact plus narrow action: good for entrance, wardrobe, storage, and safety reminders.
- Manual scene plus optional automation: first save a scene, then ask whether the user wants a recurring trigger.
- Conflict review before broad writes: for all-home, member, gateway, HVAC, or multi-room automations, prefer `automation.explain` or `automation.list` evidence before update/create.

## Anti-Patterns

- One sensor controlling the whole home without a second condition.
- A rule that immediately reverses another rule or a recent manual override.
- Fixed-time lighting that ignores daylight when illuminance sensors exist.
- Multiple overlapping automations in one room doing similar actions.
- Triggering on unsupported device categories such as curtains or HVAC unless Runtime returns support.
- Treating a product family, room name, or old prompt rule as proof that the required sensor exists.

## Execution Rules

- Missing devices, sensors, events, actions, or time details should become the smallest clarification question.
- Never invent sensors, events, actions, gateway behavior, or background execution results.
- Treat new or changed automations as persistent configuration. If the user already asked for the change, call the Runtime intent directly; for destructive or broad changes, confirm in chat first.
- Treat `automation.capabilities` as policy evidence, not as proof that every named automation action can be executed.
- Do not put status changes inside `automation.update`; use `automation.enable` or `automation.disable` for existing automation state.
- Imported design automations may be listable and toggleable even when they are not safely editable through `automation.update`. If an imported rule update is refused or has missing gateway/device references, keep the original rule and propose a replacement live automation via `automation.create`; disable/delete the imported rule only after explicit user confirmation.
- For safety, a newly planned automation should not be described as enabled or running unless Runtime says so. Status values are Runtime evidence, not wording to infer manually.
- Automation condition candidates include presence, motion, contact, illuminance, button, knob, time window, duration, and threshold only after Runtime validates the entity and event.
- Current Runtime automation action rows accept existing `device`, `group`, `meshGroup`, or `scene` targets. For a room-wide or area-wide lighting result, first create or reuse a scene that represents the room/area effect, then create the automation to execute that scene. Keep room/area action wording as planning language until Runtime exposes it in `intent.explain`.
- Timing words such as delayed execution, delayed off, duration, repeat window, and active time range are allowed only as parameters for Runtime planning.
- Dynamic light flow, curtain motor action, audio playback, panel action, and air-conditioning mode are product-specific; do not claim support unless Runtime returns it.
- If Runtime blocks automation creation or update, keep the proposal as non-applied guidance and explain the returned reason.

## Update Payload Contract

For follow-ups such as "把回家开灯自动化改到 18 点" or "主卧每天 9 点亮起来改成暖光", do not send a partial patch. Use this flow:

1. Resolve the target automation by name or id if needed.
2. Call `automation.detail.get`.
3. Prefer the returned `editablePayload` when Runtime provides it. Otherwise use the returned detail as the source of the complete rule.
4. Preserve the full condition object and full `actions[]` list unless the user explicitly asked to replace them.
5. Modify only the intended fields: `trigger` or `conditions`, active window, repeat rule, action `set` object, or name.
6. Send `automation.update` with the complete rule payload.

`automation.create` and `automation.update` both require a complete rule shape. For create, omit `automationId`; for update, use `automationId` when already known, otherwise use a unique `automationName` or `currentName`; preserve all existing conditions/actions unless the user explicitly asked to replace them.

`automation.detail.get` should return `editablePayload` and `updateShape` when Runtime can read enough detail. Treat `editablePayload` as the safest source for update requests. If it contains nested objects, keep them as objects in the next SkillRequest.

`automation.create` requires the same complete shape as update except `automationId` is omitted. `automation.update` uses `automationId` or a unique `automationName/currentName` and resends the full rule payload. Load `references/action-payloads.md` for condition fields, action rows, light parameters, repeat types, and complete create/update examples. Key reminders:

- The common daily schedule condition is an and group with one alarm condition using `HH:mm:ss` clock format.
- Include `rank` on every new automation action row so cloud validation has explicit action order, even when there is only one action.
- Source-backed event, fact, or fact-change conditions must come from Runtime supported-list, detail, or clarification evidence.
- Preserve nested condition groups and unknown product-specific action keys returned by `automation.detail.get`.
- Status toggles do not belong in automation update.

Do not put `status` in `automation.update`. Use `automation.enable` or `automation.disable` for state toggles.

If Runtime returns `clarification_required` with `payloadShape`, `examples`, or `nextStep`, treat those fields as the authoritative call contract. Ask only if a required target, field, or action choice is still missing after reading that contract.
