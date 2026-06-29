# Diagnostics

Use this reference for troubleshooting devices, gateways, scenes, and automations.

- Use `diagnose.device` for device offline, abnormal state, weak capability, or control failure questions.
- Use `diagnose.gateway` for gateway connectivity, child-device, local network, or sync concerns.
- Use `gateway.list` when the user asks which gateways exist in the home.
- Use `gateway.detail.get` when the user asks for one gateway's identity, product, online/bind state, bridge support, or configuration evidence.
- Use `gateway.thread.get` when the user asks about Thread, Matter bridge, Thread network, border-router, or child Thread connectivity evidence for one gateway.
- Use `gateway.stats.list` when the user asks for gateway summaries with home or room child-device counts.
- Use `gateway.scene_relation.list` before explaining which scenes may depend on a gateway.
- Use `gateway.configure` when the user explicitly asks to change gateway name, description, icon, MAC metadata, or room associations. Runtime must return a pending plan, validate referenced rooms against the current home, and verify through `gateway.detail.get`.
- Use `gateway.delete` only when the user explicitly asks to delete a gateway. Runtime must return an R3 local-approval plan; ordinary chat confirmation is not enough.
- Use `panel.list` when the user asks which panels are in the home.
- Use `panel.get` when the user asks for one panel's detail, button layout, visible buttons, or current button bindings.
- Use `panel.button.type.get` when the user asks for one panel's buttons of a specific press or key type.
- Use `panel.button.configure` only when the user explicitly asks to change one panel's button configuration. Runtime must return a pending plan and later verify with panel detail reads.
- Use `panel.button_event.update` when the user explicitly asks to change one existing panel button event, and pass only `buttonEventId`, optional `alias`, and sanitized `details`.
- Use `panel.button_event.batch_update` only when the user gives multiple explicit button events for the same panel. Keep the batch small; Runtime caps and verifies the plan.
- Use `panel.button_event.reset` only for an explicit request to clear one panel button event binding. Runtime returns a pending plan before reset.
- Use `knob.get` when the user asks for one rotary knob's mode, detail, bound resources, or current multi-knob configuration.
- Use `knob.configure` only when the user explicitly asks to change one rotary knob configuration. Runtime must return a pending plan and later verify with knob detail reads.
- Use `knob.reset` only for an explicit request to clear one multi-knob sub-key binding and include the target knob device plus `index`.
- Use `screen.control.list` when the user asks which devices or scenes a screen can control.
- Use `ai_voice.product.list` when the user asks which product ids support AI voice recognition. This is a product catalog read, not account binding or third-party credential access.
- Use `upgrade.file.list` when the user asks whether one device, product, or firmware version has available upgrade files.
- Use `upgrade.file.batch_list` when the user asks to compare upgrade availability across multiple devices or products.
- Use `upgrade.progress.get` when the user asks whether a device is upgrading, stuck, or on its latest upgrade progress.
- Use `app_upgrade.latest.get` when the user asks for the latest Yeelight App upgrade record for a known app type and OS type.
- Use `ota.version_file.batch_list` when the user asks for OTA files by firmware type, firmware version, or exact version across version queries.
- Use `progress.get` only when a concrete task progress key is already known from prior Runtime output or user context.
- Use `message.list` when the user asks to view account notification center messages, unread notices, or recent system/device notifications. It is read-only.
- Use `diagnose.scene` for scene execution failures or scene content questions.
- Use `diagnose.automation` for automation trigger, condition, action, or status concerns.
- Runtime should aggregate evidence in one invocation where possible.
- If evidence is missing, report unknowns clearly and do not invent a cause.
- Do not ask the model to run separate raw checks; pass the diagnostic intent to Runtime.
- Do not start firmware, OTA, gateway, or app upgrades from the Skill. Maintenance upgrade and version intents here are read-only evidence.
- Do not use B2B panel endpoints, legacy single-knob reset, or raw panel/knob payloads. Panel and knob writes must go through the semantic pending-plan intents above.
