# Device Control

Use this reference for home summary, entity lists, entity details, capability checks, state query, temporary light control, generic behavior requests, and scene execution.

- Use `home.summary` for a user asking what homes are available.
- Use `entity.list` for mixed home-scoped entity inventory across areas, rooms, devices, groups, scenes, and automations.
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
- Use `node.sorted_device.list` when the user asks for devices under a known room, device, or home node with their saved order. Provide `resType` and `resId`; do not guess them from a display name without Runtime evidence.
- Use `entity.capabilities` before claiming a device, group, scene, or automation supports a property or action.
- Use product-level `thing.schema.*` intents only for product model questions; do not substitute them for `entity.capabilities` on installed devices.
- Use `product.pedia.search` for product consultation, manuals, FAQ candidates, SKU/material-code resources, and product attachments.
- Use `thing.product.info.batch_get` for v2 product definitions when the user provides product ids.
- Use `thing.product.info.v3.batch_get` when the user provides product ids and a product definition version.
- Use `thing.product.list.v3` when the user asks for the versioned product list, not for installed home devices.
- Use `node.property_config.get` when the user asks for installed-node property configuration evidence for a known node id and node type.
- Use `state.query` for current device state.
- Use `entity.rename.batch` when the user explicitly asks to batch rename devices and scenes. Keep every item explicit and let Runtime resolve/validate targets; Runtime currently accepts device and scene resources, caps one plan at 20 items, and verifies names with `entity.list`.
- Use `device.remove` only when the user explicitly asks to delete a device record from the home. Runtime must return an R3 local-approval plan and verify the device disappeared from `entity.list` after approved commit.
- Use `device.unbind` only when the user explicitly asks to unbind a device from the current account/home. Runtime must return an R3 local-approval plan, accepts only `clearMac` and `unbindRelDevices` as options, and verifies the device disappeared from `entity.list` after approved commit.
- Use light-specific intents for power, brightness, color temperature, and RGB color when the user asks for direct lighting control.
- Use `behavior.execute` only for a temporary behavior that maps to Runtime-reviewed light properties: power, brightness, color temperature, or RGB color.
- Use `scene.execute` for running an existing scene.
- Never invent property names, ranges, device IDs, current states, or success.
