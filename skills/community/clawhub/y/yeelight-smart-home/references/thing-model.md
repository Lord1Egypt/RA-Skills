# Thing Model Reference

Use this reference to reason about Yeelight Pro entity, capability, product-model and Runtime evidence language. It is a Runtime request guide for building safe SkillRequests, not a raw物模型手册、设备清单或底层载荷指南.

## Scope

- Use it when a request mentions categories, components, properties, events, capabilities, product schemas, or ambiguous smart-home objects.
- Treat product-model vocabulary as possibility space. Treat Runtime installed-entity evidence as truth.
- Convert user language into supported Runtime intents; never build raw component-property writes.

## Runtime Evidence Ladder

| Layer | Meaning |
| --- | --- |
| 1. User wording | Untrusted natural language: preserve it, classify it, and avoid resolving IDs manually. |
| 2. Installed topology | `entity.list`, `entity.get`, `home.*`, `room.*`, `area.*`, `group.*`, `gateway.*` show what exists. |
| 3. Runtime capability | `entity.capabilities`, `state.query`, and domain detail reads decide whether a target can be controlled. |
| 4. Product knowledge | `product.pedia.search`, `thing.schema.*`, `thing.product.*`, FAQ and category reads explain product possibilities only. |
| 5. Persistent write | Supported writes execute directly after Runtime validation; use dry-run only when the caller wants a no-write preview before asking the user. |

## Core Rules

- house 是数据隔离边界，不跨 house 合并查询、控制或记忆。
- 控制层级按 house、area、room、gateway、group、device、component 理解，实际解析交给 Runtime。
- 品类代表可组控的大类；设备组只能使用组内共同品类能力的子集。
- 组件是能力集合；单控属性采用 componentIndex-propName 格式，不能凭名称猜属性。
- 每个产品至少有基础组件，普通组件表达灯、传感器、窗帘、温控、面板等可复用能力。
- 配置类属性只能在 Runtime 明确支持的持久变更流程中处理。

## Entity Hierarchy

`house -> area -> room -> gateway -> group -> device -> component`

| Entity | Skill meaning |
| --- | --- |
| Home | Isolation boundary for entities, plans, local memory and recommendations. |
| Area | Spatial grouping above rooms; useful for routing and organization, not proof of a controllable group. |
| Room | Primary user-facing location for device, scene and favorite operations. |
| Gateway | Bridge/topology object for child devices and gateway diagnostics. |
| Group | Shared-capability target; Runtime must validate members and common capabilities. |
| Device | Installed entity; actual control must be proven by Runtime capability evidence. |
| Component | Product-model capability vocabulary; never execute raw component/property names directly. |
| Scene | Saved action bundle; execution and edits are separate intents. |
| Automation | Persistent condition-action rule; create/update/toggle/delete require Runtime policy. |

## Category Vocabulary

| Category | Meaning | Typical components |
| --- | --- | --- |
| light | 灯类 | 开关灯、亮度灯、色温灯、彩光灯、角度色温灯、无色温彩光灯组件 |
| contact_sensor | 接触式传感器类 | 接触式传感器 |
| human_sensor | 人体感应传感器类 | 人感传感器、人在传感器、人体红外传感器、dali人感传感器 |
| light_sensor | 环境光传感器类 | 光照传感器2、环境光传感器、dali光感传感器、亮度雷达传感器(可屏蔽区段) |
| curtain | 窗帘类 | 窗帘、梦幻帘 |
| temp_control | 温控类 | 空调、新风、地暖、温控器组件 |
| relay_switch | 继电器开关类 | 无线开关通道、开关 |
| scene_panel | 情景面板类 | 跑道屏、情景按键、dali情景按键 |
| other | 其他类 | 音乐组件、声音组件、可升降组件、未定义子设备 |
| gateway | 网关类 | 网关 |
| knob_switch | 旋钮开关类 | 旋钮开关、dali旋钮开关组件 |

## Capability Map

| Domain | Primary Runtime intents | How to reason |
| --- | --- | --- |
| Lighting experience | `light.*`, `lighting.experience.apply`, `lighting.design.plan`, `lighting.design.apply`, `scene.*` | Temporary ambience and saved changes execute through Runtime validation; use dry-run previews when caller confirmation is needed. |
| Home organization | `home.*`, `room.*`, `area.*`, `group.*`, `favorite.*`, `node.sorted_device.list` | Organization writes must preserve explicit targets, current ordering evidence and write-after-read verification. |
| Device lifecycle | `device.list`, `device.detail.get`, `device.rename`, `device.move`, `device.remove`, `device.unbind` | Rename/move are reversible writes; remove/unbind require caller-side explicit agreement before direct execution. |
| Gateway and bridge | `gateway.*`, `diagnose.gateway` | Gateway identity/topology is not pairing authority; delete/configure require reviewed Runtime plans. |
| Panel and knob | `panel.*`, `knob.*`, `screen.control.list` | Button/knob changes use dedicated action rows, never panel layout payloads. |
| Automation | `automation.*`, `schedule_job.list`, `automation.supported.*` | Create/update/toggle/delete depend on policy and complete rule evidence; support reads are not write permission. |
| Product knowledge | `product.pedia.search`, `thing.schema.*`, `thing.product.*`, `thing.category.*`, `thing.component.*`, `thing.property.*` | Use pedia search for manuals, FAQ candidates and product资料; use thing-model reads for schema vocabulary; neither is installed capability proof. |

## Capability Families

| Family | User language | Typical vocabulary |
| --- | --- | --- |
| Lighting | Power, brightness, color temperature, RGB color, transition and effect words | 开关灯、亮度灯、色温灯、彩光灯、角度色温灯、无色温彩光灯组件、灯带、筒灯、射灯 |
| Sensor | Presence, motion, contact, illuminance and event evidence; usually read-only | 人感传感器、人在传感器、人体红外传感器、dali人感传感器、接触式传感器、光照传感器2、环境光传感器、dali光感传感器、亮度雷达传感器(可屏蔽区段) |
| Switch and panel | Button, knob, screen and relay configuration through dedicated Runtime intents | 无线开关通道、开关、跑道屏、情景按键、dali情景按键、旋钮开关、dali旋钮开关组件 |
| Gateway and bridge | Gateway identity, topology, Thread/Matter evidence and reviewed gateway configuration | 网关 |
| Environment and shading | Curtain, HVAC and environment device words; control only when Runtime validates support | 窗帘、梦幻帘、空调、新风、地暖、温控器组件 |

## Property Vocabulary

Use this dictionary to interpret Runtime evidence and user wording. It is not a raw write contract and does not list internal device keys.

| Public field | Meaning | Skill behavior |
| --- | --- | --- |
| power | power/on | Map 开灯/关灯 to high-level light power intents or an action row whose set object contains `power`, only after Runtime validates target support. |
| brightness | brightness | Map 亮一点/暗一点/亮度 to brightness requests, range 1-100 when Runtime accepts it. |
| colorTemperature | color temperature | Map 暖一点/冷一点/色温 to color-temperature requests; lower values are warmer. |
| color | RGB color | Use only for explicit color requests and Runtime-supported color targets. |
| mode | mode | Product-specific mode; preserve from Runtime evidence, do not invent values. |
| online | online | Read-only online state. Do not use as a control property. |
| motionDetected | motion detected | Motion sensor evidence for automation planning. |
| occupancyDetected | occupancy/presence detected | Presence evidence for automation planning. |
| doorClosed | door/contact closed | Contact sensor evidence for door/window automations. |
| sensorActive | sensor active | Sensor active state evidence. |
| alarm | alarm/tamper state | Sensor alarm evidence. |
| currentTemperature / humidity | temperature / humidity | Environment readings for diagnostics or automation conditions when Runtime supports them. |
| illuminance | environment light level | Illuminance-level evidence for daylight-aware automation suggestions. |
| currentPosition / targetPosition | curtain current/target position | Curtain percentage or travel requests; only control when Runtime validates curtain capability. |
| switchPower | switch power | Single-channel or multi-channel switch power. Channel-specific forms must come from Runtime evidence, not public fixture examples. |
| backlightPower | backlight power | Switch/panel backlight behavior, product-specific. |
| airConditionerPower / airConditionerMode / airConditionerTargetTemperature | HVAC fields | HVAC behavior is product-specific and requires Runtime evidence. |
| mediaPlayback / mediaVolume | media fields | Music/media playback or volume behavior is product-specific; preserve only from Runtime evidence. |
| deviceAttribute fields | diagnostic/configuration attributes | LAN control, LED indicator, smart switch, power-on behavior, relay state, motor direction, default duration, channel count, and HVAC count are diagnostic/configuration attributes, not generic light actions. |

## Runtime Evidence Order

| Evidence | Use |
| --- | --- |
| `entity.capabilities` | Installed-device truth for whether a target supports a state or action. |
| `state.query` | Current state evidence for a resolved target. |
| `thing.schema.*` | Product definition and explanation evidence; not installed-device proof. |
| `node.property_config.get` | Installed-node configuration evidence for a known node id and node type. |
| `automation.supported.*` | Automation vocabulary support evidence; not a commit guarantee. |

## Guardrails

- Prefer high-level intents such as light control, scene execution, room organization, panel configuration or diagnostics. Never ask the model to send raw component-property writes.
- Do not infer capability from product name, room name, marketing name, color, component name, feature word, protocol or model series.
- For control, query or trust Runtime capability evidence before claiming support. For persistent writes, trust only direct Runtime execution results and write-after-read verification.
- Persistent home, room, area, device, group, scene, automation, panel, knob, gateway and favorite changes must route through supported Runtime intents, with caller-side user confirmation for destructive or permission-sensitive operations.
- Product schema reads can explain what a product type may support; they do not prove an installed device supports the same capability.
- For unknown component, property or event language, preserve the user's natural words in the SkillRequest target and let Runtime resolve or ask the smallest clarification.
- When product knowledge and installed topology conflict, installed Runtime evidence wins for execution; product knowledge remains explanation only.
