# Lighting Design Import

Use this reference for `lighting.design.import` and `device.slot.create` payloads. The caller authors the standard `yeelight-home` design model only.

## Runtime Boundary

- Build explicit rooms, future device slots, room-local groups, scenes, and automations in `parameters`.
- Keep product selection, grouping strategy, scene design, automation intent, ambience judgment, and assumptions in the Skill/user decision path.
- Do not send `quantity`, `autoGroup`, fuzzy slots, clear-all flags, overwrite flags, cloud ids, or implementation-specific ids in a design import.
- For a new home import, put the home name in the request `name` field and omit house identifiers, `homeRef.name`, and CLI `--house-id`.
- For an existing home import, include `parameters.houseId` or `homeRef.id` only after Runtime or the user has already identified the target home.
- Runtime returns `success` only after the import is verified through readback. If cloud import cannot be fully verified after Runtime submission, Runtime returns `partial` with `partialState` and any read-back topology it can safely obtain; use that response instead of manually chaining `home.search`, `home.list`, or `entity.list`.
- `device.slot.create` on an existing home uses the standard lighting design import path. It can create a new design room with slots, but must not be used to append slots to an existing same-name room because that would create a duplicate room. If Runtime returns `device_slot_create_existing_room_would_duplicate_room`, ask for a distinct design-room name or use a future dedicated append capability.

## Top-Level Shape

```json
{
  "name": "家庭或设计名",
  "key": "home-design-key",
  "gatewayName": "默认网关",
  "rooms": [],
  "areas": [],
  "scenes": [],
  "automations": []
}
```

`key` is a caller-local stable key used only by this request. Use readable lowercase keys when possible.

## Rooms And Device Slots

```json
{
  "key": "living",
  "name": "客厅",
  "deviceSlots": [
    {
      "key": "living-grille-1",
      "name": "客厅黑色格栅灯1",
      "product": {
        "skuCode": "copy-from-product-select",
        "capabilityPid": 198666,
        "productComponentId": 4,
        "productName": "已选产品名",
        "category": "格栅灯",
        "series": "P20",
        "notes": "选择原因或安装假设"
      }
    }
  ],
  "groups": []
}
```

- Expand quantities into explicit `deviceSlots[]` rows.
- Use each slot's `key` for later group, scene, and automation references.
- Future slots are design metadata. They are not paired online devices and do not prove controllability.
- `product.skuCode`, `product.capabilityPid`, and `product.productComponentId` must come from `scripts/product-select.mjs` after the AI chooses a candidate. Never invent them.
- `skuCode` identifies the concrete selected SKU number visible to designers/installers. `capabilityPid` identifies the capability/firmware identity shared by products with the same controllable capability; it is not the concrete SKU and not a user-facing product ID. `productComponentId` identifies the product capability component.
- Preserve exact model, color, shape, beam angle, opening size, finish, and selection reasoning in readable product fields and `notes`.
- If no candidate has trustworthy `skuCode`, `capabilityPid`, and `productComponentId`, ask one smallest product clarification or use product consultation before importing.

## Groups

```json
{
  "key": "living-grille-group",
  "name": "客厅格栅灯组",
  "groupCategory": "lighting",
  "groupCapability": "colorTemperature",
  "slotKeys": ["living-grille-1", "living-grille-2"]
}
```

- Put groups under the room that owns the slots.
- Use `groupCategory: "lighting"` for lighting groups.
- Use `groupCapability` to describe the shared controllable capability, such as `power`, `brightness`, `colorTemperature`, or `color`.
- Only group same-room compatible slots unless the user explicitly asks for cross-room or whole-home control.
- Create same-type groups only for quantity >= 2; do not create one-member groups.

## Areas

```json
{
  "key": "public-area",
  "name": "公共区",
  "roomKeys": ["living", "dining"]
}
```

Areas are optional. Use them only when the user asked for zones, floors, public/private grouping, or later scenes need area-level design scope.

## Scenes

```json
{
  "key": "living-home",
  "name": "客厅回家模式",
  "actions": [
    {
      "targetType": "group",
      "targetKey": "living-grille-group",
      "targetName": "客厅格栅灯组",
      "rank": 0,
      "set": {
        "power": true,
        "brightness": 70,
        "colorTemperature": 3500
      }
    }
  ]
}
```

- `targetType` should be `room`, `device`, `group`, `scene`, or `home` only when the referenced key exists in the same request.
- `targetKey` points to a room key, device slot key, group key, scene key, or home key from the same model.
- Use objective values in `set`; do not leave mood words in executable actions.
- Put optional action timing such as `delay`, `duration`, and `delayoff` on the action row.

## Automations

```json
{
  "key": "master-9am",
  "name": "主卧9点亮灯",
  "activeWindow": {"start": "00:00:00", "end": "23:59:59"},
  "repeat": "daily",
  "trigger": {"conditionKind": "alarm", "time": "09:00:00"},
  "actions": [
    {
      "targetType": "device",
      "targetKey": "master-ceiling-1",
      "targetName": "主卧方形吸顶灯",
      "rank": 0,
      "set": {
        "power": true,
        "brightness": 60,
        "colorTemperature": 3000
      }
    }
  ]
}
```

- `trigger` holds the primary trigger, such as `{"conditionKind":"alarm","time":"09:00:00"}` for a clock trigger.
- Use `conditions[]` only when the rule needs additional source-backed facts beyond the primary trigger.
- Non-clock rules can use `conditionKind: "event"`, `conditionKind: "fact_change"`, and `conditionKind: "fact"` only when Runtime/product evidence supplies the needed target and capability details. Keep trigger-like rows (`alarm`, `event`, `fact_change`) separate from fact-check rows.
- Automation `actions[]` use the same `targetType`, `targetKey`, and `set` shape as scenes.
- Do not invent sensor triggers, event names, or missing products; keep them as notes or recommendations unless Runtime evidence supports them.
- If a design automation depends on future trigger hardware, add an `extraMeta.notes` or slot note explaining the required planning hardware instead of creating an executable trigger. Common mappings: presence/motion/no-motion -> presence or motion sensor; door/window open/closed/timeout -> contact sensor; illuminance threshold/rise/drop -> illuminance-capable sensor; button/knob gesture -> control surface.

## Full Example

For a multi-room example with groups, scenes, and automations, load `assets/examples/lighting-design-full-home.json`.
