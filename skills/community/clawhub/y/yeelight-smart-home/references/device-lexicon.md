# Device Lexicon Reference

Use this reference to extract stable meaning from Yeelight Pro device/product language. The goal is not to memorize product copy; the goal is to preserve useful words, choose the right Runtime intent family, and avoid false certainty.

## Extraction Model

Extract slots, not IDs. A good SkillRequest keeps these slots visible for Runtime:

| Slot | Examples | Skill behavior |
| --- | --- | --- |
| Location slot | 客厅、主卧、餐厅、走廊、全屋、某个家庭 | Pass as home/room/area context. Do not turn location into a device. |
| Entity role slot | 灯、灯组、情景、自动化、网关、面板、旋钮、传感器、收藏 | Use it to choose the reference module and candidate intent family. |
| Product slot | S20射灯、E系列筒灯、青空灯、跑道屏、Matter网关 | Preserve as product wording; installed target still needs Runtime evidence. |
| Capability slot | 亮一点、2700K、彩色、有人、照度低、按钮双击 | Map to capability/event language, then let Runtime validate support. |
| Operation slot | 打开、调暗、移动到房间、删除、分享、排序、诊断 | Choose read/control/config/delete/diagnose lane and respect Runtime risk policy. |
| Constraint slot | 晚上、5分钟、只影响餐厅、不要彩色、保留原顺序 | Pass as parameters or conversationContext, not as hidden assumptions. |

## Resolution Ladder

| User phrase type | Examples | Routing |
| --- | --- | --- |
| Looks like installed entity | 客厅主灯、餐厅灯组、回家情景、离家自动化 | `entity.list`/domain list/detail first; ask clarification on collisions. |
| Looks like product family | S系列筒灯、120射灯、青空灯、跑道屏 | Use product/schema or design context; do not claim it exists in the home. |
| Looks like symptom | 网关离线、灯不亮、自动化没触发 | Route to diagnostics, preserving symptom words and target candidates. |
| Looks like organization | 首页排序、收藏、房间、区域、分组 | Route to home-room-area/groups reference and pending-plan writes when persistent. |
| Looks like installer/pairing | 配网、绑定、扫码、BLE、添加设备 | Do not simulate onboarding; use Runtime block/manual guidance unless reviewed. |

## Device Language Families

| Family | Candidate words | Routing note |
| --- | --- | --- |
| Lighting | 青空灯、筒灯、射灯、灯带、格栅灯、线条灯、泛光灯、球泡、灯泡 | `device-control`, `lighting-design`, `scenes`; target may be device, group, room or scene. |
| Control surface | 智能开关、情景开关、旋钮开关、墙壁开关、全面屏、全景屏、跑道屏 | `diagnostics`, `thing-model`; writes go through panel/knob semantic intents. |
| Sensor | 传感器、人在传感器、人体红外传感器、门窗传感器、光照传感器 | `automations`, `automation-events`, `diagnostics`; usually evidence or condition vocabulary. |
| Bridge and protocol | 网关、Mesh、Matter、Thread、KNX、DALI、VRF | `diagnostics`; topology evidence only, not onboarding or pairing authority. |
| Shading and climate | 窗帘、梦幻帘、开合帘、卷帘、温控器、风管机 | `device-control`, `automations`; installed-device evidence and capability validation first. |

## Product Vocabulary To Preserve

- Series: S系列、S20、S21、E系列、E20、E+系列、E14、E27、M20、C系列、D系列、P系列、P20、P21
- Protocols: Mesh、Mesh版、蓝牙、Matter、Thread、KNX、DALI、VRF
- Device families: 青空灯、筒灯、射灯、筒射灯、吊线灯、灯带、格栅灯、线条灯、泛光灯、斗胆灯、球泡、灯泡、智能开关、情景开关、旋钮开关、墙壁开关、全面屏、全景屏、旋钮屏、跑道屏、窗帘、梦幻帘、开合帘、卷帘、电机、温控器、风管机、驱动、电源、模组、模块、网关、传感器、人在传感器、人体红外传感器、门窗传感器

## Feature Words

| Feature | Candidate words | How to use |
| --- | --- | --- |
| Finish/color | 白色、黑色、深空灰、晶墨灰、丝墨青、汉玉白、亮银、亮金 | Preserve as product wording or disambiguation hint, not capability evidence. |
| Shape/installation | 方形、圆形、无边框、窄边框、磁吸、轨道、明装、嵌入式、折叠、贴装、墙面、吊顶 | Preserve for product search, lighting design and fuzzy target text. |
| Size/opening | 3寸、30cm、60cm、35开孔、55开孔、75开孔、80开孔 | Preserve exactly; do not convert into device id or room id. |
| Head count | 单头、双头、3头、5头、6头、10头、12头 | Preserve for product wording and lighting design. |
| Beam angle | 15°、24°、36°、60° | Preserve for product/design context only. |
| Power/wiring | 8w、12w、15w、36w、恒压、高压、低压、DC、零火 | Preserve as product/install context; never treat as authorization to configure wiring. |

## Series Words

| Series | Interpretation | Preserve |
| --- | --- | --- |
| D系列 | 产品系列词，用于保留用户自然描述 | 防眩、基础智能 |
| E系列 | 产品系列词，用于区分同类灯具候选 | 调光、深防眩 |
| S系列 | 产品系列词，用于区分同类灯具候选 | 高显指、高性能 |
| P系列 | 产品系列词，用于设计或选型语境 | 高端、创新 |

## Recognition Rules

- Preserve model, series, color, shape, size, power, beam angle, protocol, installation style and display words in the natural target.
- Normalize obvious spoken variants only as candidate understanding. Runtime remains the final resolver.
- Do not turn room names, scene names, group names, installation tasks, sales wording or debugging symptoms into device identities.
- If the user names several devices, keep their order and pass natural descriptions to Runtime instead of resolving IDs yourself.
- Treat every product word as a candidate phrase. Installed devices, current state and writable capability must come from Runtime evidence.

## Normalized Aliases

| User wording | Normalized wording | Kind |
| --- | --- | --- |
| 感应器 | 传感器 | synonym |
| 厘米 | cm | unit |
| 八瓦 | 8w | number_unit |
| 七十五 | 75 | number |
| 艾斯系列 | S系列 | phonetic |
| 120射灯 | E20射灯 | folk_name |
| 一来 | 易来 | phonetic |
| 干节点 | 干接点 | synonym |
| 开合帘 | 窗帘 | folk_name |
| 小夜灯 | 夜灯 | folk_name |

## Ambiguity Handling

- "客厅灯" may mean one device, a light group, every light in the room, or a scene target. Keep location and role separate.
- "有人传感器" or "感应器" is sensor vocabulary, not proof that the user's home has that sensor.
- "120射灯" or "S系列筒灯" is product language. Do not assume installed target, model id, or capability from it.
- Old automatic device-addition or default-device assumptions are blocked. Adding, pairing or onboarding devices requires a reviewed Runtime path or official manual guidance.
- For product selection or lighting design, mention candidate families only as candidate guidance when Runtime or the user's request asks for design/recommendation context.
