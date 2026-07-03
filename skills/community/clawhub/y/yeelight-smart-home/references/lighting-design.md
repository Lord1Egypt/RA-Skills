# Lighting Design

Use this reference as the routing and workflow entry for full-home lighting design, future device slots, room ambience, scene recipes, and standard design import.

## Intent Routing

- Use `lighting.design.plan` for advice-only design, layout, ambience, or ritual planning.
- Use `lighting.design.apply` only for temporary real-device state changes: `power`, `brightness`, `colorTemperature`, and `color`.
- `lighting.design.apply` does not use scene/import action rows. For apply, send explicit real-device actions such as `parameters.design.actions[] = {"deviceId":"...","property":"brightness","value":45}` or direct fields like `brightness` when Runtime has a single resolved target.
- Use `device.slot.create` when the user asks to add or reserve not-yet-installed lighting positions in an existing home as a new design room/section. Do not use it to append slots into an already existing same-name room; Runtime will block that path because the current import path would create a duplicate room.
- Use `lighting.design.import` when the user asks to materialize a full design topology into a new, empty, or lightly configured home. It imports the standard design model through Runtime and can include rooms, design slots, groups, areas, scenes, and automations.
- For "创建/新建/设计添加一个家庭" plus full topology, prefer one `lighting.design.import` request with the standard design model and no `parameters.houseId`, no `homeRef.name`, and no CLI `--house-id`; Runtime creates the home and selects the returned `houseId`.
- For a configured existing home with many rooms, devices, groups, scenes, or automations, prefer dedicated Runtime intents such as `room.batch_create`, `group.create`, `scene.create/update`, and `automation.create/update` unless the user explicitly asks for full-home metadata import.

## Required Subreferences

- Product selection and candidate judgment: `references/lighting-product-selection.md`.
- Standard lighting design import model: `references/lighting-design-import.md`.
- Nested action rows, conditions, operations, and machine schema lookup: `references/payload-shapes.md`.
- Scene recipe conversion: `references/scene-recipes.md`.
- Automation schedule/trigger recipes: `references/automation-recipes.md`.
- Broader lighting experience, mood interpretation, and compound scene flows: `references/lighting-experience.md`.
- Full multi-room import example: `assets/examples/lighting-design-full-home.json` for new-home import; add `houseId` only for an existing target home.

Load only the needed subreference unless the user asks for a full-home materialization. For requests like "帮我创建和设计一个家庭，客厅一个吸顶灯..." load all six subreferences above.

## Design Workflow

1. Normalize the utterance into home, areas, rooms, device slot families, quantities, product constraints, groups, scenes, automations, and corrections.
2. Query `operation.lesson.list` for `intent=lighting.design.import` and a small `limit` before building a full-home import. Apply relevant confirmed lessons such as target-home resolution, known payload-shape traps, or fastest path rules.
3. Decide target home mode:
   - New home wording: build the standard design model with the request `name` as the home name, omit house identifiers and `homeRef.name`, and call `lighting.design.import` once. Do not call `home.create` first and do not inherit the current profile houseId.
   - Existing named home wording: resolve/select the home first or use a known `homeRef.id`/`parameters.houseId`; call `lighting.design.import` only when the home is empty/lightly configured or the user explicitly wants full metadata import.
   - Existing selected home new-room slot additions: use `device.slot.create` with the selected or explicit `houseId`. If the room name already exists, ask for a new design-room name or use a dedicated append capability only when Runtime exposes one.
4. Build the design in this fixed order: room structure -> device slots -> room-local groups -> scenes -> automations. Each later layer may reference only `key` values created by earlier layers.
5. Apply `references/lighting-experience.md` before choosing ambience parameters.
6. Resolve each distinct slot family to a concrete product candidate before import. Run `node scripts/product-select.mjs --query "<slot wording>" --room "<room>" --goal "<design goal>" --limit 8`.
7. Expand quantities into explicit `rooms[].deviceSlots[]` rows. Do not send `quantity`, `autoGroup`, or fuzzy slots to Runtime.
8. Author groups before the Runtime call as explicit room-local `rooms[].groups[]` rows. Use `groupCategory`, `groupCapability`, and `slotKeys`.
9. Author scene and automation rows only when their `targetKey` exists in the same import model. Use objective `set` values, not mood words.
10. Call `lighting.design.import` once. After Runtime returns success or partial, report the actual imported counts, returned `houseId`, and whether Runtime selected it as the current home.
11. If Runtime fails with a reusable cause such as target-home confusion, unsupported design field, validation pattern, or a better fallback path, record `operation.lesson.record` before the final answer.
12. Use `references/response-presentation.md` for the final surface. A successful new-home import should be shown as a new home dashboard with selected-home context, room/device-slot/group/scene/automation summaries, warnings, and partial failures.

Do not stop at a static design document when the user asked to "添加槽位", "预留", "导入", "落到系统里", or "完善整个家庭".

## Requirement Normalization

- Preserve room attribution and order. "客厅一个吸顶灯, 2 个黑色格栅灯" means three slot rows under the living room after quantity expansion.
- Parse apartment shorthand before slot expansion. "三室两厅一卫" implies room candidates such as 客厅, 餐厅, 主卧, 次卧, 卧室3, 卫生间 unless the user provides explicit room names.
- If a lighting slot lacks a room but surrounding wording clearly implies one, assign it to the plausible stated room and record the assumption in `extraMeta.notes`; otherwise ask one smallest question.
- Later corrections override earlier statements for the same target. Merge same-room repeated mentions before import.
- Keep user-stated constraints: series, color, install style, opening, size, wattage, beam angle, shape, head count, protocol, product nickname, and version words.
- Normalize obvious wording only for understanding: 感应器 means 传感器; 厘米 means cm; 八瓦 means 8w; 十二瓦 means 12w; 十五瓦 means 15w; 七十五开孔 means 75开孔; 艾斯/爱斯/爱思 means S 系列; 三十六度 means 36°; 120射灯 means E20射灯 as a folk product phrase; 一来 means 易来.
- Do not create real sensors, gateways, panels, or paired devices just to satisfy an automation. For full-home design materialization, missing trigger hardware should become explicit non-controllable design slots or installer recommendations, not silent omissions. For existing-home automation execution, use triggers only when Runtime verifies installed sensor capability.
- Map automation trigger wording to likely planning hardware before deciding whether the rule is executable: motion/presence/no-motion events imply a presence or motion sensor slot; door/window events imply a contact sensor slot; illuminance/low-light events imply an illuminance-capable sensor slot; button/knob events imply a control-surface slot. Put these in notes/recommendations unless the user explicitly asked to include those future slots in the design.
- Do not discard user intent only because one condition/action is unsupported. Remove or downgrade only the unsupported condition, keep supported actions and design metadata when still meaningful.

## Existing Home Safety

Full design import can replace or reshape home design metadata. It is best for new homes, empty homes, or deliberate full-design materialization.

For existing homes with substantial configuration:

- Add rooms with `room.batch_create`.
- Rename/update rooms, areas, groups, scenes, or automations with their dedicated intents.
- Create standalone groups/scenes/automations with `group.create`, `scene.create`, and `automation.create`.
- Use `lighting.design.import` only when the user explicitly wants full metadata import for that home and has confirmed the broad change in chat.

## New Home Import Fast Path

When the user says a sentence like:

> 帮我设计添加一个易来新家家庭，客厅一个吸顶灯...

Use this shortest path:

1. Load product/design references and choose products before building the Runtime request.
2. Build the standard model with request field `name = "易来新家家庭"`, `rooms[].deviceSlots[]`, `rooms[].groups[]`, `scenes[].actions[]`, and `automations[].trigger/actions`.
3. Do not include `parameters.houseId`, do not set `homeRef.name`, do not pass CLI `--house-id`, and do not use the currently selected home.
4. Call `lighting.design.import` once.
5. Treat `result.selectedHouseId` as the new current home for later turns.

If a model mistakenly imports a new-home request into the current sample/default home, record an `operation.lesson.record` lesson for `lighting.design.import` with `lessonType=resource_resolution`.

## Response Shape

- For a proposal: give concise room-by-room design and assumptions.
- For a materialization request: call Runtime, then use a new home dashboard or change-result card from `references/response-presentation.md`; report actual created/imported items, selected-home context, and partial failures.
- For ambiguity: ask one smallest question only when it materially changes product choice, room assignment, or persistent configuration.
