# Thing Model Reference

Use this reference to reason about Yeelight Pro entity, capability, product-model and Runtime evidence language. It is a semantic map for building safe SkillRequests, not a raw物模型手册、设备清单或 API payload guide.

## Scope

- Use it when a request mentions categories, components, properties, events, capabilities, product schemas, or ambiguous smart-home objects.
- Treat product-model vocabulary as possibility space. Treat Runtime installed-entity evidence as truth.
- Convert user language into semantic Runtime intents; never build raw component-property writes.

## Runtime Evidence Ladder

| Layer | Meaning |
| --- | --- |
| 1. User wording | Untrusted natural language: preserve it, classify it, and avoid resolving IDs manually. |
| 2. Installed topology | `entity.list`, `entity.get`, `home.*`, `room.*`, `area.*`, `group.*`, `gateway.*` show what exists. |
| 3. Runtime capability | `entity.capabilities`, `state.query`, and domain detail reads decide whether a target can be controlled. |
| 4. Product knowledge | `product.pedia.search`, `thing.schema.*`, `thing.product.*`, FAQ and category reads explain product possibilities only. |
| 5. Persistent plan | R2/R3 writes must be stored and verified by Runtime pending plans before any user-facing success claim. |

## Core Rules

- house 是数据隔离边界，不跨 house 合并查询、控制或记忆。
- 控制层级按 house、area、room、gateway、group、device、component 理解，实际解析交给 Runtime。
- 品类代表可组控的大类；设备组只能使用组内共同品类能力的子集。
- 组件是能力集合；单控属性采用 componentIndex-propName 语义，不能凭名称猜属性。
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

## Semantic Capability Map

| Domain | Primary Runtime intents | How to reason |
| --- | --- | --- |
| Lighting experience | `light.*`, `lighting.experience.apply`, `lighting.design.plan`, `lighting.design.apply`, `scene.*` | Temporary ambience can be direct; saved scene/design changes are pending plans. |
| Home organization | `home.*`, `room.*`, `area.*`, `group.*`, `favorite.*`, `node.sorted_device.list` | Organization writes must preserve explicit targets, current ordering evidence and write-after-read verification. |
| Device lifecycle | `device.list`, `device.detail.get`, `device.rename`, `device.move`, `device.remove`, `device.unbind` | Rename/move are guarded writes; remove/unbind are high-impact local-approval plans. |
| Gateway and bridge | `gateway.*`, `diagnose.gateway` | Gateway identity/topology is not pairing authority; delete/configure require reviewed Runtime plans. |
| Panel and knob | `panel.*`, `knob.*`, `screen.control.list` | Button/knob changes use dedicated semantic rows, never raw panel layout payloads. |
| Automation | `automation.*`, `schedule_job.list`, `automation.supported.*` | Create/update/toggle/delete depend on policy and complete rule evidence; support reads are not write permission. |
| Product knowledge | `product.pedia.search`, `thing.schema.*`, `thing.product.*`, `thing.category.*`, `thing.component.*`, `thing.property.*` | Use pedia search for manuals, FAQ candidates and product资料; use thing-model reads for schema vocabulary; neither is installed capability proof. |

## Capability Families

| Family | User language | Typical vocabulary |
| --- | --- | --- |
| Lighting | Power, brightness, color temperature, RGB color, transition and effect words | 开关灯、亮度灯、色温灯、彩光灯、角度色温灯、无色温彩光灯组件、灯带、筒灯、射灯 |
| Sensor | Presence, motion, contact, illuminance and event evidence; usually read-only | 人感传感器、人在传感器、人体红外传感器、dali人感传感器、接触式传感器、光照传感器2、环境光传感器、dali光感传感器、亮度雷达传感器(可屏蔽区段) |
| Switch and panel | Button, knob, screen and relay configuration through dedicated pending-plan intents | 无线开关通道、开关、跑道屏、情景按键、dali情景按键、旋钮开关、dali旋钮开关组件 |
| Gateway and bridge | Gateway identity, topology, Thread/Matter evidence and reviewed gateway configuration | 网关 |
| Environment and shading | Curtain, HVAC and environment device words; control only when Runtime validates support | 窗帘、梦幻帘、空调、新风、地暖、温控器组件 |

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
- For control, query or trust Runtime capability evidence before claiming support. For persistent writes, trust only Runtime plan and commit verification.
- Persistent home, room, area, device, group, scene, automation, panel, knob, gateway and favorite changes must route through pending-plan confirmation.
- Product schema reads can explain what a product type may support; they do not prove an installed device supports the same capability.
- For unknown component, property or event language, preserve the user's natural words in the SkillRequest target and let Runtime resolve or ask the smallest clarification.
- When product knowledge and installed topology conflict, installed Runtime evidence wins for execution; product knowledge remains explanation only.
