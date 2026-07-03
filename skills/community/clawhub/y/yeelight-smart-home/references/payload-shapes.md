# Payload Shapes

Use this reference when a Runtime intent accepts nested actions, conditions, items, operations, button events, or lighting design JSON.

## Contract Lookup First

Before guessing a large payload, ask Runtime for the objective contract:

```json
{
  "contractVersion": "1.0",
  "requestId": "intent-explain-scene-update",
  "locale": "zh-CN",
  "utterance": "查看 scene.update 的参数格式",
  "intent": "intent.explain",
  "parameters": {
    "intent": "scene.update"
  }
}
```

Use returned `requestSchema`, `payloadGuide.payloadShape`, `examples`, and `nextStep` as authoritative. If Runtime returns `editablePayload` or `updateShape`, read-modify-send that complete payload.

## CLI Standard Contract Fields First

For new SkillRequest JSON, prefer clear standard field names.

- Use `targetType`, `targetId` or `targetKey`, `targetName`, and top-level `set` in action rows when building from user language.
- Preserve returned row fields from `editablePayload` during read-modify-write updates. For new user-authored rows, use only `targetType`, `targetId` or `targetKey`, `targetName`, and `set`.
- Use `trigger`, `conditions`, `activeWindow`, `repeat`, and `repeatDays` for automation rules when building from user language.
- Use `power`, `brightness`, `colorTemperature`, and `color` inside `set`.

## Common Action Row

Scene actions, automation actions, design-import actions, panel button actions, and knob-related actions share this basic row idea:

```json
{
  "targetType": "device",
  "targetId": "device-or-group-id",
  "targetName": "target display name",
  "rank": 0,
  "set": {
    "power": true,
    "brightness": 60,
    "colorTemperature": 3000
  }
}
```

Required fields depend on the intent and Runtime schema.

- `targetType` names the target kind such as `device`, `group`, `room`, `scene`, or `home`.
- `targetId` is used for existing installed resources only when Runtime or the user already supplied it.
- `targetKey` is used in `lighting.design.import` and must reference a key from the same import model.
- `targetName` is display evidence; preserve it when Runtime returns it.
- `rank` preserves action order; keep existing order on update unless the user asks to reorder.
- Optional row timing uses `delay`, `duration`, and `delayoff`.
- Additional fields returned by detail reads should be preserved. Do not invent product-specific action fields from natural language.

## Target Type Semantics

Use Runtime entity evidence, not guessed ids. For design import, use keys from the same model:

- `targetType: "room"` with `targetKey` from `rooms[].key`.
- `targetType: "device"` with `targetKey` from `rooms[].deviceSlots[].key`.
- `targetType: "group"` with `targetKey` from `rooms[].groups[].key`.
- `targetType: "scene"` with `targetKey` from `scenes[].key`.
- `targetType: "home"` with the top-level `key` when the action is intentionally whole-home.

Do not remap area or room ids into another target type unless Runtime returned that mapping.

## Light Action Parameters

```json
{
  "set": {
      "power": true,
      "brightness": 60,
      "colorTemperature": 3000,
      "color": 16777215
  }
}
```

- `power`: boolean.
- `brightness`: 1-100.
- `colorTemperature`: usually 2700-6500 when supported.
- `color`: RGB integer or Runtime-accepted color value. For direct `light.color.set`, prefer an RGB integer or `hex`; do not author `{r,g,b}` objects unless Runtime explicitly returns that shape.
- `delay`, `duration`, `delayoff`: non-negative milliseconds.
- `toggle`, `adjust`, `flow`, `action`, custom or channel-specific keys require Runtime/product evidence.

For updates, preserve unknown keys returned by `editablePayload`. Change only the intended field unless the user asks to replace the whole action.

## Capability Vocabulary

Use the readable fields above for new writes. If Runtime returns unknown target-specific fields in an `editablePayload`, preserve them only during read-modify-write updates and do not author new requests with those fields.

| Public field | Meaning | Notes |
| --- | --- | --- |
| power | power/on | Boolean light power. |
| brightness | brightness/level | Integer 1-100 for common lighting writes. |
| colorTemperature | color temperature | Kelvin-style color temperature where supported. |
| color | color/RGB | RGB integer or Runtime-accepted color value. |
| mode | mode | Product-specific mode; preserve only from evidence. |
| online | online | Read-only online state. |
| motion / occupancy | motion / occupancy | Sensor evidence, not a light action. |
| contactClosed | door/contact closed | Contact sensor evidence. |
| illuminance | environment light level | Illuminance evidence. |
| switchPower | switch power | Multi-channel switch evidence. |

For multi-channel devices, use only the readable channel structure returned by Runtime detail or capability evidence. Preserve returned channel-specific fields on update.

## Repair Rule

If a payload fails with `clarification_required`, do not retry variants blindly. Use the returned `acceptedFields`, `payloadShape`, `examples`, `nextStep`, `editablePayload`, or `updateShape`; ask the user only when a remaining business choice cannot be inferred.
