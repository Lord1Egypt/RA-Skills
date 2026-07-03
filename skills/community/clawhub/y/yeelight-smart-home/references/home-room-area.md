# Home Room Area

Use this reference for homes, rooms, and areas.

## Intent Routing

- Use `home.list` when the user asks for all homes, needs to choose the right home, or a later delete/member/transfer plan needs account-level home candidates with counts.
- Use `home.search` when the user provides a partial home name and needs candidates before selecting, updating, deleting, joining, or managing members of a home.
- Use `entity.list` or `entity.get` for read-only entities inside one selected home.
- For home, room, area, device, group, scene, or automation names, pass the user's original target words when they are unique enough, even if they may contain a typo or homophone; Runtime resolves high-confidence matches and returns ambiguity instead of guessing low-confidence targets.
- Use `home.detail.get` when the user asks for current home details beyond the home list.
- Use `home.stat.get` when the user asks for home-level counts, organization statistics, or impact evidence before a home-wide plan.
- Use `geo_area.children.list` when the user asks for selectable city/geographic area candidates or when a new or updated home needs an `areaCode` and no city name is known yet. It is account-level geographic lookup, not a home-space area query.
- Use `geo_area.search` when the user provides a country, province, state, city, or area name and needs candidate `areaCode`/`areaName` values before `home.create` or `home.update`.
- Use `home.member.list` when the user asks who is in the current home; Runtime returns only masked member evidence.
- Use `home.member.current.get` only when the user provides or prior Runtime output supplies the member/user id; member contact fields are returned masked.
- Use `home.member.invite` when the user explicitly asks to generate a home sharing invite. Runtime validates and executes the Runtime request directly, accepts expiry and normal/admin role only, and verifies with masked member-list evidence after execution.
- Use `home.member.accept_share` when the user explicitly asks to accept a structured home sharing code. Pass only the returned or user-provided `shareId`, `createTime`, and optional expected `houseId`; Runtime derives the recipient from the current local account and verifies the accepted home through `home.summary`.
- Use `home.member.configure` when the user explicitly asks to change a member between normal and admin. Pass `memberName` when the user names a member; pass `memberId` only when Runtime or the user already supplied it. Runtime validates and executes the Runtime request directly, rejects owner/master transfer through this intent, and verifies the role through `home.member.list`.
- Use `home.member.remove`, `home.member.transfer`, or `home.member.quit` only for explicit member removal, owner transfer, or leaving a shared home. For remove/transfer, pass `memberName` when the user names a member; pass `memberId` only when Runtime or the user already supplied it. These are R3 high-impact operations: get explicit chat confirmation first, then call the Runtime intent directly.
- Use `home.create` when the user explicitly asks to create a new home/family. Pass only structured fields such as `name`, `description`/`desc`, `icon`, `areaCode`, and `areaName`; Runtime executes the account-scoped create and verifies the created home by home list or created-house accessibility.
- If the user asks to create a new home and immediately design it, route the selected products, rooms, slots, groups, scenes, and automations directly to one `lighting.design.import` request. Do not require real devices to be installed before creating design slots.
- Use `home.update` when the user changes home profile fields such as name, description, icon, area code/name, building name/address, or floor name. Runtime must validate and execute the Runtime request directly; home name is verified by home detail readback, while address/floor metadata relies on cloud write acknowledgement plus readable home detail.
- Use `home.delete` only when the user explicitly asks to delete the current home. This is R3 high impact: ask for explicit chat confirmation first, then call Runtime directly.
- Use `home.sort.list` when the user asks to inspect the current home page or room organization order before changing it.
- Use `room.list` when the user asks for rooms in the selected home or when a room-affecting plan needs room candidates and device counts.
- Use `room.search` when the user gives a partial room name and needs candidates before moving devices, assigning areas, updating, or deleting rooms.
- Use `room.detail.get` when the user asks for one room's detail or when a persistent room-affecting plan needs stronger preflight evidence for a known room id.
- Use `area.detail.get` when the user asks for an area detail, associated rooms, parent area context, or when an area update plan needs stronger preflight evidence.
- Use `room.create` or `area.create` for creating a persistent room or area; Runtime must validate and execute the Runtime request directly before the cloud write.
- Use `room.rename` for room name changes. For natural-language rename such as "把孩子屋改成儿童房", pass `roomName` or `currentName` as the current room name and `newName` or `name` as the new display name; do not call `entity.list` only to obtain `roomId` when the current room name is unique. Runtime resolves the room id from the entity list, validates, executes, and verifies the new room name with `entity.list`.
- Use `room.update` when the user changes room metadata such as name, icon/image, gateway binding fields, sequence, or room capability. Runtime must validate and execute the Runtime request directly; name is verified through `entity.list`, while other submitted metadata is treated as a guarded cloud write acknowledgement.
- Use `room.batch_create` or `room.batch_update` when the user explicitly asks to create or update multiple rooms in one operation. Keep every room item explicit; Runtime caps one request at 20 rooms and verifies room names through `entity.list`.
- Use `room.area.configure` when the user asks to add or remove one room from one or more areas. Runtime validates the room and area ids, executes the Runtime request, and verifies by write acknowledgement plus room/area accessibility through `entity.list`.
- When the user asks to add or remove multiple rooms from an area in one utterance, use `operation.batch.configure` with one explicit `room.area.configure` operation per room. Do not send `roomNames[]` to one `room.area.configure` request.
- Use `device.rename` for cloud device name changes and `device.move` for moving one device to another room. Runtime must validate and execute the Runtime request directly and later verify the device name or `roomId` with `entity.list`.
- Use `device.move_room.batch` when the user asks to move multiple devices into rooms in one operation. Keep the batch explicit as either `items: [{deviceId, roomId}]` or an equivalent device-to-room map; Runtime caps one plan at 20 items and verifies each device `roomId`.
- Use `area.update` when the user changes an area's name, description, icon, parent area, or complete room association list. Runtime must validate and execute the Runtime request directly and verify the area with `entity.list`.
- Use `group.list` when the user asks for custom groups or needs group candidates with room membership before group update/delete.
- Use `group.search` when the user gives a partial group name and needs candidates before changing or deleting a group.
- Cross-house movement remains unsupported unless Runtime returns explicit support for it.
- Use `home.sort.configure` when the user explicitly asks to reorder items on the home page or within a home/room organization surface; Runtime must validate and execute the Runtime request directly and later verify by reading the sort result.
- Use `home.lock_all` or `home.unlock_all` only when the user explicitly asks to lock or unlock reset ability for all devices in the current home. Runtime validates and executes the Runtime request directly with whole-home impact preview and verifies by write acknowledgement plus home entity-list accessibility.
- Use `favorite.list` when the user asks what is currently pinned, favorited, or shown in favorite shortcuts.
- Use `favorite.plan` when the user asks for a non-persistent recommendation for how to organize favorites; it must not be described as an applied change.
- Use `favorite.add` when the user asks to add a device, group/mesh group, or scene to favorites. Do not add rooms as favorites unless Runtime later exposes a cloud-verifiable room favorite target.
- Use `favorite.update` when the user asks to change an existing favorite's rank, enabled state, or resource mapping.
- Use `favorite.batch_add` or `favorite.batch_update` when the user asks to organize multiple favorites in one request. Runtime must execute one batch request and later verify every item through the favorites list.
- Use `favorite.delete` when the user explicitly asks to remove one favorite shortcut. Use `favorite.batch_delete` when the user explicitly asks to remove multiple favorite shortcuts. Runtime resolves the target favorites first, caps one request at 20 items, executes directly, and verifies every removal through `favorite.list`.
- For favorite and sort writes, pass Runtime-returned resource identity such as `entityType` plus entity id fields; do not ask the user for internal numeric type fields.
- For `home.sort.configure`, use a shape with a sort surface/target plus `items[]`; each item carries an entity type, resource id, and rank. Read `home.sort.list` first when preserving existing unspecified items.
- For favorite batch writes, use `items[]`; each row carries a favorite id for updates/deletes or a resource identity for add, plus optional rank and validity. If `favorite.list` returns duplicate rows for the same target without `favoriteId`, include the returned `rank` together with `targetType` and `targetId` to delete the intended favorite row.
- For `room.batch_create` and `room.batch_update`, use `rooms[]` or `items[]`; create rows need names, update rows need room ids. If the user names rooms for batch update, call `room.list` or `room.detail.get` first and fill each row's `roomId`; do not send name-only batch update rows.
- For multi-room area membership, use `operation.batch.configure` with operations such as `{"intent":"room.area.configure","parameters":{"roomName":"影音厅","addAreaNames":["公共区"]}}` and another row for `玄关`.
- For `device.move_room.batch`, use explicit `items[]` rows of device id and target room id, or an equivalent device-to-room map when Runtime accepts it.
- Use `room.delete` or `area.delete` only when the user explicitly asks to delete one target. Runtime must validate and execute the Runtime request directly, re-check the target, and verify removal after execution.
- Use `room.batch_delete` or `area.batch_delete` only when the user explicitly asks to delete multiple rooms or areas. Runtime caps one request at 20 targets, resolves each target by id or unique name, and verifies every target disappeared from `entity.list`.
- For room/area batch delete payloads, use `names` or `items[]` rows such as `{"name":"测试书房"}` or `{"roomId":"..."}` / `{"areaId":"..."}`. Do not send type-specific plural fields such as `roomNames[]` or `areaNames[]`.

## Spatial Modeling Rules

- Home is the hard isolation boundary for entities, local memory, and recommendations. Never merge homes with similar names.
- Current home is only the default execution context. If the user's wording, recent task, or emotional context points to another home, resolve that intended home before using the selected context.
- Semantic home switch rule: when the user names or clearly implies a home different from the current selected home, use `home.search` or `home.list` to find candidates. For read-only questions, use the resolved home when there is one clear match. For control, create, update, delete, import, or other writes, ask one concise confirmation to use or switch to the intended home unless the user explicitly named it as the target in the same command.
- After a new-home lighting import succeeds and Runtime reports the selected home, treat that returned home as the current conversation home and say so in the response.
- Room is the primary user-facing operation anchor. Area is a higher-level organization layer for floors, zones, or public/private spaces.
- A lighting or automation proposal should preserve the user's spatial scope. "餐桌上方" is narrower than "餐厅"; "起夜路径" may span multiple rooms but only along the path.
- Do not create a default room, area, gateway binding, or real device placement to make a vague design look complete. If the user explicitly asks for an actionable lighting design with prebuilt slots, use `lighting.design.import` so Runtime creates governed design metadata.
- When reordering home page or favorites, preserve the user's explicit order and leave unspecified items in their current relative order unless Runtime returns another order.
- For batch create/update/delete, keep every target explicit. Do not infer "all bedrooms" or "all lights" from a vague plural if Runtime did not resolve them.

## Natural Language Mapping

- "我有哪些家庭/房间/区域": read-only list/detail intents.
- "新建儿童房/把书房改名": room or home/area write. For room rename, prefer `{houseId, roomName/currentName, newName/name}` so Runtime can resolve the room and avoid an extra lookup turn.
- "把设备移到餐厅": `device.move` or batch move with explicit targets.
- "首页把客厅放前面/收藏这些灯": sort or favorite write.
- "一楼公共区包括客厅餐厅": area update or create, depending on existing area evidence.
- "还没装灯，先建一个客厅格栅灯设计区放两个格栅灯槽位": `device.slot.create`.
- "在已有客厅里再追加两个格栅灯槽位": ask for a distinct design-room/section name or wait for a dedicated append capability; do not use `device.slot.create` against an existing same-name room.
- "帮这个新家做完整照明设计并落到系统里": one `lighting.design.import` request with the standard lighting design model.

## Clarification Triggers

- Ask one smallest clarification question when the target home, room, or area is ambiguous.
- Do not choose a home by guessing from a name collision.
- Ask before operating when the current selected home and the semantically intended home appear different and the user did not explicitly say to use the named home for this operation.
- Do not invent sorting ranks or favorite resource types. Pass the user's requested order and natural target names to Runtime when exact IDs are not available.
- Ask whether the change is conceptual design or real home configuration when the user mixes phrases such as "帮我规划" with "直接创建".
