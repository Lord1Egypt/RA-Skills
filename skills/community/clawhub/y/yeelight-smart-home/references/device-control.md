# Device Control

Use this reference for home summary, entity lists, entity details, capability checks, state query, temporary light control, and scene execution.

## Fast Direct Control

For ordinary user goals such as "打开孩子屋吸顶灯", "把客厅主灯调到 60%", "执行晚安情景", or "启用主卧 9 点自动化", send one final Runtime request. Do not first call `entity.list`, `entity.get`, `entity.capabilities`, room list, or device detail only to discover IDs.

Runtime maintains a long-lived topology cache and resolves targets from names, room qualifiers, IDs, and candidates. Give Runtime the user's target words, including likely typos or homophones; Runtime will conservatively resolve high-confidence matches or return candidates when ambiguous. Runtime refreshes topology once if the cached entity index misses. The cache resolves identity only, not current device state:

- For state or diagnostic questions, still send one Runtime request with the user's target words. Runtime may use cached topology to find the entity, but it must read live state, capabilities, or details before answering the factual question.
- Device control/state:
  ```json
  {
    "intent": "light.power.set",
    "parameters": {
      "houseId": "known-or-selected-house-id",
      "roomName": "孩子屋",
      "deviceName": "吸顶灯",
      "power": true
    }
  }
  ```
- Scene execution:
  ```json
  {
    "intent": "scene.execute",
    "parameters": {
      "houseId": "known-or-selected-house-id",
      "sceneName": "晚安"
    }
  }
  ```
- When the user provides multiple target hints, pass them together instead of choosing one:
  ```json
  {
    "intent": "light.brightness.set",
    "targets": [
      {"entityType": "room", "name": "客厅"},
      {"entityType": "device", "name": "主灯"}
    ],
    "parameters": {"brightness": 60}
  }
  ```

Only ask the user after Runtime returns `clarification_required`. If Runtime returns candidates, ask the smallest disambiguation question from those candidates. Use `entity.list` when the user asks to browse inventory, compare devices, audit topology, or when Runtime explicitly asks for a read step after a complex payload rejection.

- Use `home.summary` for a user asking what homes are available.
- Use `entity.list` for mixed home-scoped entity inventory across areas, rooms, devices, groups, scenes, and automations.
- When the user asks to list or find entities within a room, type, or keyword such as "灯光区的 RGBW 设备", include the natural filters in the same `entity.list` request (`entityType`, `roomName`/`roomId`, and `name` when a keyword is present) so Runtime returns a focused list instead of a full-home inventory.
- Use `entity.get` when the user names a specific entity and asks what it is.
- Use `device.list` when the user asks for device candidates in one home or a device-affecting plan needs a safer preflight list with room/gateway ownership evidence.
- Use `device.virtual_count.get` when the user asks how many virtual devices exist in the selected home or a capacity/diagnostic flow needs that count.
- Use `device.detail.get` for device metadata details when the user asks for device identity, placement, model, or configuration evidence.
- Use `device.attr.list` when the user asks for device attribute evidence before a diagnosis or persistent change.
- Use `sensor.list` when the user asks which sensors exist in the home.
- Use `sensor.event.list` when the user asks for sensor event definitions or sensor-trigger evidence.
- Use `device.energy.summary` when the user asks for device electricity or energy usage.
- Use `device.weather.get` when the user asks for weather context tied to a device.
- Use `meshgroup.detail.get` when the user asks for a Mesh group, its member devices, or group detail evidence.
- Use `node.sorted_device.list` when the user asks for devices under a known room, device, or home node with their saved order. Provide resource identity only when Runtime already returned it; do not guess it from a display name.
- Use `entity.capabilities` before claiming a device, group, scene, or automation supports a property or action.
- Use product-level `thing.schema.*` intents only for product model questions; do not substitute them for `entity.capabilities` on installed devices.
- Use `product.pedia.search` for product consultation, manuals, FAQ candidates, SKU resources, and product attachments.
- Use `device.slot.create` when the user explicitly asks to add or reserve not-yet-installed lighting device positions in a home. This creates standard design slots through Runtime execution; it is not device pairing, not network onboarding, and not evidence that the device is online. Product selection and quantity expansion must be completed before the Runtime call. For existing homes, only use it for a new design room/section; do not append slots into an existing same-name room.
- Use `thing.product.info.batch_get` for v2 product definitions when the user provides `capabilityPid` values.
- Use `thing.product.info.v3.batch_get` when the user provides `capabilityPid` values and a product definition version.
- Use `thing.product.list.v3` when the user asks for the versioned product list, not for installed home devices.
- Use `node.property_config.get` when the user asks for installed-node property configuration evidence for a known node id and node type.
- Use `state.query` for current device state. Pass `parameters.deviceId` when known, or `deviceName` plus room qualifiers when the user names the target. Never answer current power, brightness, online status, or similar real-time values from topology cache alone.
- Use `entity.rename.batch` when the user explicitly asks to batch rename devices and scenes. Keep every item explicit and let Runtime resolve/validate targets; Runtime accepts device and scene resources, caps one request at 20 items, and verifies names with `entity.list`.
- Use `device.remove` only when the user explicitly asks to delete a device record from the home. This is R3 high impact: confirm in chat first, then call Runtime; Runtime verifies the device disappeared from `entity.list`.
- Use `device.unbind` only when the user explicitly asks to unbind a device from the current account/home. This is R3 high impact: confirm in chat first, then call Runtime. Runtime accepts only `clearMac` and `unbindRelDevices` as options and verifies the device disappeared from `entity.list`.
- Use light-specific intents for power, brightness, color temperature, and RGB color when the user asks for direct lighting control. Prefer `light.power.set`, `light.brightness.set`, `light.color_temperature.set`, and `light.color.set`.
- Route white-light wording such as "暖白", "暖光", "自然白", "冷白", "偏暖", or "偏冷" to `light.color_temperature.set` or `light.color_temperature.adjust`, not `light.color.set`. Use RGB color only when the user clearly asks for a color such as red, blue, pink, purple, a hex value, or an explicit RGB value.
- For direct `light.color.set`, send `color` or `value` as an RGB integer, or `hex` as a hex string. Do not send `{r,g,b}` objects unless Runtime explicitly returns that shape.
- Use `scene.execute` for running an existing scene.
- Avoid `lighting.design.apply` for a large temporary action array when the same user goal can run an existing scene or a small set of direct `light.*` calls. If Runtime returns an execution-size or apply failure, prefer `scene.execute` or individual light-property intents instead of repeatedly retrying the same large apply payload.
- Never invent property names, ranges, device IDs, current states, or success.

## Standard Property Vocabulary

Use only the clear field names that Runtime exposes in SkillRequest payloads and responses. Do not author lower-level device-property identifiers in SkillRequest JSON; when unsure, use `intent.explain`, `entity.capabilities`, or `state.query` and follow the returned standard fields.

| Standard field | Meaning | Typical use |
|---|---|---|
| `power` | on/off | Direct light write, scene/automation action, state read. |
| `brightness` | brightness level | Direct light write, scene/automation action, state read. |
| `colorTemperature` | color temperature | Direct light write, scene/automation action, state read when supported. |
| `color` | RGB color | Direct light write, scene/automation action, state read when supported. |
| `mode` | product mode | Read or preserve from Runtime evidence unless the intent schema explicitly allows writing it. |
| `online` | online status | Read-only state or diagnostics. |
| `sensorActive` | sensor active | Sensor state or automation condition evidence. |
| `alarm` | alarm/tamper state | Sensor state or automation condition evidence. |
| `doorClosed` | contact/door closed | Sensor state or automation condition evidence. |
| `occupancyDetected` | occupancy detected | Sensor state or automation condition evidence. |
| `motionDetected` | motion detected | Sensor state or automation condition evidence. |
| `humidity` | humidity | Sensor state or automation condition evidence. |
| `currentTemperature` | current temperature | Sensor/climate state or automation condition evidence. |
| `currentPosition` | current curtain/position | Curtain state evidence. |
| `targetPosition` | target curtain/position | Curtain action only when Runtime capability evidence allows it. |
| `switchPower` | switch/channel power | Switch state/action only when Runtime returns channel capability evidence. |
| `airConditionerTargetTemperature` | AC target temperature | Climate action only when Runtime capability evidence allows it. |

Direct light-control intents only support verified lighting properties such as `power`, `brightness`, `colorTemperature`, and `color`. Sensor and diagnostic properties such as `motionDetected`, `occupancyDetected`, `doorClosed`, or `alarm` are for state/capability reading or automation conditions, not direct light writes.

## Direct Light Intent Shapes

Use these shapes for direct single-device control. In SkillRequest JSON, include `houseId` in `parameters` or `homeRef` when known; in traditional shell usage the CLI may also accept `--house-id`.

Power:
```json
{
  "intent": "light.power.set",
  "parameters": {
    "houseId": "known-or-selected-house-id",
    "roomName": "孩子屋",
    "deviceName": "吸顶灯",
    "power": true
  }
}
```

Brightness:
```json
{
  "intent": "light.brightness.set",
  "parameters": {
    "houseId": "known-or-selected-house-id",
    "roomName": "客厅",
    "deviceName": "主灯",
    "brightness": 60
  }
}
```

Color temperature:
```json
{
  "intent": "light.color_temperature.set",
  "parameters": {
    "houseId": "known-or-selected-house-id",
    "roomName": "孩子屋",
    "deviceName": "吸顶灯",
    "colorTemperature": 3000
  }
}
```

RGB color:
```json
{
  "intent": "light.color.set",
  "parameters": {
    "houseId": "known-or-selected-house-id",
    "roomName": "客厅",
    "deviceName": "氛围灯",
    "color": 16744628
  }
}
```

Equivalent hex input is also acceptable when Runtime supports it for the intent:

```json
{
  "intent": "light.color.set",
  "parameters": {
    "houseId": "known-or-selected-house-id",
    "roomName": "客厅",
    "deviceName": "氛围灯",
    "hex": "#ff80b4"
  }
}
```
