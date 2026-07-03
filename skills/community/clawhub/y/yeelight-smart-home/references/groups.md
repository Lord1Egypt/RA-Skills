# Groups

Use this reference for device groups and lighting groups.

## Intent Routing

- Use `entity.list` or `entity.get` for group discovery.
- Use `group.structure.list` when the user asks for group membership, grouping structure, or group organization under a home.
- Use `group.detail.get` when the user asks for one group's detailed configuration or when a group write plan needs stronger preflight evidence.
- Use `group.create` for creating a persistent group; Runtime validates and executes the Runtime request directly.
- Persistent `group.create` needs at least one explicit member device by name or id. If the user only says "在这个房间建一个灯组" without naming the member lights, ask which devices should join. For not-yet-installed lights or slot-based groups, use `lighting.design.import` instead of creating an empty live group.
- Use `group.update` when the user changes a group's name, description, icon, or room assignment. Runtime must validate and execute the Runtime request directly and verify the group with `entity.list`.
- Do not claim group membership changes are executable from `group.update`; member-list editing support remains owner-reviewed.
- Use `group.delete` only when the user explicitly asks to delete one group. Runtime must validate and execute the Runtime request directly, re-check the group, and verify removal after execution.
- Use `group.batch_delete` only when the user explicitly asks to delete multiple groups. Runtime caps one request at 20 groups, resolves each target by id or unique name, and verifies every group disappeared from `entity.list`.
- For `group.batch_delete`, use `names` or `items[]` rows such as `{"name":"客厅灯组"}` or `{"groupId":"..."}`. Do not send `groupNames[]`.
- Do not assume devices can be grouped together. Runtime must validate device membership and capability rules.
- If the user says "this room's lights" and a group is not named, pass natural target text to Runtime rather than inventing a group.
- If the user is importing a lighting design with not-yet-installed slots and asks for same-type grouping, the Skill must decide the room-local grouping strategy and pass explicit `rooms[].groups[]` rows with `groupCategory`, `groupCapability`, and `slotKeys` to `lighting.design.import`. Treat imported groups as design metadata until Runtime confirms the import; do not present them as existing controllable groups before real devices are installed.

## Grouping Rules

- Grouping is for devices that should be controlled together because they are in the same space and share a practical capability.
- Prefer room-local groups such as "客厅筒灯" or "餐厅吊灯"; avoid cross-room groups unless the user explicitly asks for a whole-home or area-level control surface.
- Do not mix devices whose main control capabilities differ, such as color-only and color-temperature-only lights, unless Runtime returns common capability evidence.
- If `group.create` returns `group_capability_not_shared_by_selected_devices` or similar shared-capability rejection, do not retry sibling group capabilities blindly. Read `entity.capabilities` for the named member devices, then create the group only with devices that share the same practical component and writable properties, or ask the user to split the group.
- Sensors, gateways, panels, and knobs are usually automation evidence or control surfaces, not lighting groups.
- A single device is not a useful group unless Runtime exposes a specific product grouping feature and the user asks for it.
- For design proposals, use group names as candidate organization, not proof that the group exists. Creating or changing a group is persistent R2 configuration.

## User Wording

- "把这几盏灯编成一组": `group.create` with explicit member candidates.
- "各房间相同类型自动成组" while creating slots: `lighting.design.import` with Skill-authored `rooms[].groups[]` rows in the grouped design topology.
- "改一下这个灯组名字": `group.update`.
- "把餐厅灯组删了": `group.delete`.
- "以后客厅这些灯一起调": propose a group plan or a scene, depending on whether the user wants a control target or a saved effect.
