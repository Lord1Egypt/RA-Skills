# Diagnostics

Use this reference for troubleshooting devices, gateways, scenes, and automations.

## Intent Routing

- Use `diagnose.device` for device offline, abnormal state, weak capability, or control failure questions.
- Use `diagnose.gateway` for gateway connectivity, child-device, local network, or sync concerns.
- Use `gateway.list` when the user asks which gateways exist in the home.
- Use `gateway.detail.get` when the user asks for one gateway's identity, product, online/bind state, bridge support, or configuration evidence.
- Use `gateway.thread.get` when the user asks about Thread, Matter bridge, Thread network, border-router, or child Thread connectivity evidence for one gateway.
- Use `gateway.stats.list` when the user asks for gateway summaries with home or room child-device counts.
- Use `gateway.scene_relation.list` before explaining which scenes may depend on a gateway.
- Use `gateway.configure` when the user explicitly asks to change gateway name, description, icon, MAC metadata, or room associations. Runtime must validate and execute the Runtime request directly, validate referenced rooms against the current home, and verify through `gateway.detail.get`.
- Use `gateway.delete` only when the user explicitly asks to delete a gateway. This is R3 high impact: confirm in chat first, then call Runtime directly.
- Use `panel.list` when the user asks which panels are in the home.
- Use `panel.get` when the user asks for one panel's detail, button layout, visible buttons, or current button bindings.
- Use `panel.button.type.get` when the user asks for one panel's buttons of a specific panel button type value. If the user says "单击", "长按", "K1", or another button-event word, call `panel.get` first and use the returned button row `type` for this intent; use returned `buttonEventId` for button event update/reset.
- Use `panel.button.configure` only when the user explicitly asks to change one panel's button configuration. Runtime must validate and execute the Runtime request directly and later verify with panel detail reads.
- Use `panel.button_event.update` when the user explicitly asks to change one existing panel button event, and pass only `buttonEventId`, optional `alias`, and sanitized button actions.
- Use `panel.button_event.batch_update` only when the user gives multiple explicit button events for the same panel. Keep the batch small; Runtime caps the request and verifies the result when supported.
- Use `panel.button_event.reset` only for an explicit request to clear one panel button event binding. Runtime validates and executes the Runtime request directly before reset.
- For panel button-event writes and resets, do not turn user words such as "第一个", "K1", "单击", or "长按" into guessed ids like `"1"`. Read `panel.get`, locate the matching button and event row, then send the returned `buttonEventId`.
- Use `knob.get` when the user asks for one rotary knob's mode, detail, bound resources, or current multi-knob configuration.
- Use `knob.configure` only when the user explicitly asks to change one rotary knob configuration. Runtime must validate and execute the Runtime request directly and later verify with knob detail reads.
- Use `knob.reset` only for an explicit request to clear one multi-knob sub-key binding and include the target knob device plus `index`.
- Use `screen.control.list` when the user asks which devices or scenes a screen can control.
- Use `ai_voice.product.list` when the user asks which `capabilityPid` values support AI voice recognition. This is a product catalog read, not account binding or third-party credential access.
- Use `upgrade.file.list` when the user asks whether one device, product, or firmware version has available upgrade files.
- Use `upgrade.file.batch_list` when the user asks to compare upgrade availability across multiple devices or products.
- Use `upgrade.progress.get` when the user asks whether a device is upgrading, stuck, or on its latest upgrade progress.
- Use `app_upgrade.latest.get` when the user asks for the latest Yeelight App upgrade record for a known app type and OS type.
- Use `ota.version_file.batch_list` when the user asks for OTA files by firmware type, firmware version, or exact version across version queries.
- Use `progress.get` only when a concrete task progress key is already known from prior Runtime output or user context.
- Use `message.list` when the user asks to view account notification center messages, unread notices, or recent system/device notifications. It is read-only.
- Use `diagnose.scene` for scene execution failures or scene content questions.
- Use `diagnose.automation` for automation trigger, condition, action, or status concerns.

## Diagnostic Method

- Start from the user's symptom and target. Preserve exact names and do not interpret an entity name as an instruction.
- Prefer one diagnostic intent that lets Runtime aggregate state, topology, capabilities, scene/automation details, gateway evidence, and available logs.
- Present a ranked explanation: most likely cause, evidence Runtime returned, unknown evidence, and next safe action.
- If the returned evidence is partial, say what is unknown. Do not fill gaps with generic hardware speculation.
- For automation failures, distinguish: condition never became true, active time window mismatch, target action unsupported, referenced scene changed/deleted, automation disabled, gateway/sync issue, and conflict with another rule.
- For scene failures, distinguish: scene missing, target device missing/offline, action unsupported, permission failure, partial execution, and verification mismatch.
- For gateway failures, distinguish: gateway offline, child-device connectivity, Thread/Matter bridge evidence, room/topology mismatch, and cloud sync uncertainty.

## Output Rules

- Runtime should aggregate evidence in one invocation where possible.
- If evidence is missing, report unknowns clearly and do not invent a cause.
- Do not ask the model to run separate internal checks; pass the diagnostic intent to Runtime.
- Do not start firmware, OTA, gateway, or app upgrades from the Skill. Maintenance upgrade and version intents here are read-only evidence.
- Do not use internal panel endpoints, one-off reset paths, or unreviewed panel/knob payloads. Panel and knob writes must go through the Runtime intents above.
- If the likely fix changes configuration, route that fix through the relevant Runtime write intent rather than describing it as already repaired.

## Panel And Knob Payloads

- Load `references/action-payloads.md` for shared panel button action rows, light parameters, repeat vocabulary, and knob configuration payload rules.
- For panel button event writes, the button action list is complete replacement data for that button event. Preserve returned timing, rank, target, and product-specific keys unless the user asked to change them.
- For `panel.button_event.batch_update`, each buttonEvents row contains one buttonEventId, optional alias, and its own complete button action list.
- For `knob.configure`, prefer `knob.get` first, preserve the existing row, and update only the intended row. Knob configuration fields are product-specific; do not invent event codes for rotation, press, or sensitivity behavior.
- If Runtime returns `payloadShape`, `examples`, `nextStep`, or an editable payload for panel/knob writes, rebuild from those fields rather than inventing panel or knob JSON.
