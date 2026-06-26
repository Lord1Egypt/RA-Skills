# HiFleet Claw 技能清单 / HiFleet Claw Skills

> 本文档为 HiFleet Claw 应用提供的技能索引，支持中英双语。技能将按序在 ClawHub 上实现。
> This document is the skill index for the HiFleet Claw application, in Chinese and English. Skills will be implemented one by one on ClawHub.

---

## 1. 船位 / Ship Position ✅ 已实现

| 中文 | 英文 |
|------|------|
| **名称** | 船位 |
| **Name** | Ship Position |
| **描述** | 查询、展示与管理船舶实时或历史位置信息，支持 AIS 报位、锚位、靠泊等状态。 |
| **Description** | Query, display and manage real-time or historical vessel positions, including AIS reports, anchorage and berthing status. |
| **触发词** | 船位、位置、报位、在哪、轨迹、AIS 位置 |
| **Trigger terms** | ship position, vessel position, location, AIS position, track, where is |
| **实现** | [ship-position/](ship-position/) — 获取（岸基+卫星+移动）最新位置，需配置 `usertoken` |

---

## 2. 档案 / Archive (Vessel Profile)

| 中文 | 英文 |
|------|------|
| **名称** | 档案 |
| **Name** | Archive / Vessel Profile |
| **描述** | 船舶与公司档案的查询与管理，包括船籍、船型、建造年份、船东、管理公司等基础信息。 |
| **Description** | Query and manage vessel and company profiles: flag, type, build year, owner, manager and other basic information. |
| **触发词** | 档案、船舶信息、船籍、船型、船东、管理公司 |
| **Trigger terms** | archive, vessel profile, ship info, flag, ship type, owner, manager |

---

## 3. 港口 / Port

| 中文 | 英文 |
|------|------|
| **名称** | 港口 |
| **Name** | Port |
| **描述** | 港口信息查询，包括港口列表、泊位、锚地、港口设施、靠离泊计划与港口动态等。 |
| **Description** | Port information: port list, berths, anchorages, facilities, berthing/unberthing plans and port updates. |
| **触发词** | 港口、泊位、锚地、靠港、离港、港口信息 |
| **Trigger terms** | port, berth, anchorage, port call, arrival, departure, port info |

---

## 4. 性能 / Performance

| 中文 | 英文 |
|------|------|
| **名称** | 性能 |
| **Name** | Performance |
| **描述** | 船舶航行与主机性能分析，如航速、油耗、主机负荷、能效指标（EEOI 等）及性能报告。 |
| **Description** | Vessel and main engine performance: speed, fuel consumption, engine load, EEOI and performance reports. |
| **触发词** | 性能、油耗、航速、主机、能效、EEOI |
| **Trigger terms** | performance, fuel consumption, speed, main engine, EEOI, efficiency |

---

## 5. 航程 / Voyage

| 中文 | 英文 |
|------|------|
| **名称** | 航程 |
| **Name** | Voyage |
| **描述** | 航次与航程管理：航次创建、航程段、挂港顺序、预计到港/离港时间及航程统计。 |
| **Description** | Voyage and leg management: create voyage, legs, port call sequence, ETA/ETD and voyage statistics. |
| **触发词** | 航程、航次、挂港、ETA、ETD、航程段 |
| **Trigger terms** | voyage, voyage leg, port call, ETA, ETD, voyage segment |

---

## 6. 航线 / Route

| 中文 | 英文 |
|------|------|
| **名称** | 航线 |
| **Name** | Route |
| **描述** | 航线规划与查询：推荐航线、航路点、距离与航时估算、历史航线与航线对比。 |
| **Description** | Route planning and query: recommended routes, waypoints, distance and time estimates, historical routes and comparison. |
| **触发词** | 航线、航路、推荐航线、距离、航时、航路点 |
| **Trigger terms** | route, shipping route, recommended route, distance, sailing time, waypoint |

---

## 7. 租船 / Charter

| 中文 | 英文 |
|------|------|
| **名称** | 租船 |
| **Name** | Charter |
| **描述** | 租船业务支持：租约信息、租家、租金、租期、合同条款及租船市场相关查询。 |
| **Description** | Charter support: charter party, charterer, hire, period, contract terms and charter market queries. |
| **触发词** | 租船、租约、租家、租金、租期、合同 |
| **Trigger terms** | charter, charter party, charterer, hire, period, contract |

---

## 8. 航运 / Shipping

| 中文 | 英文 |
|------|------|
| **名称** | 航运 |
| **Name** | Shipping |
| **描述** | 航运综合信息：运价、运力、市场动态、船舶买卖、航运新闻与行业数据。 |
| **Description** | General shipping: freight rates, tonnage, market updates, sale & purchase, shipping news and industry data. |
| **触发词** | 航运、运价、运力、市场、买卖、航运新闻 |
| **Trigger terms** | shipping, freight rate, tonnage, market, sale and purchase, shipping news |

---

## 9. 气象海况 / Weather & Sea Conditions

| 中文 | 英文 |
|------|------|
| **名称** | 气象海况 |
| **Name** | Weather & Sea Conditions |
| **描述** | 海上气象与海况：风、浪、涌、能见度、台风/气旋路径及航行气象建议。 |
| **Description** | Maritime weather and sea state: wind, wave, swell, visibility, typhoon/cyclone tracks and voyage weather advice. |
| **触发词** | 气象、海况、风、浪、台风、能见度 |
| **Trigger terms** | weather, sea conditions, wind, wave, typhoon, visibility |

---

## 10. 船队 / Fleet

| 中文 | 英文 |
|------|------|
| **名称** | 船队 |
| **Name** | Fleet |
| **描述** | 船队级视图与管理：多船监控、船队分布、船队统计、报警汇总及船队报表。 |
| **Description** | Fleet-level view and management: multi-vessel monitoring, fleet distribution, statistics, alerts and fleet reports. |
| **触发词** | 船队、多船、船队分布、船队统计、船队报表 |
| **Trigger terms** | fleet, multi-vessel, fleet distribution, fleet statistics, fleet report |

---

## 11. AIS / AIS

| 中文 | 英文 |
|------|------|
| **名称** | AIS |
| **Name** | AIS (Automatic Identification System) |
| **描述** | AIS 数据与解析：AIS 报文、船舶识别、动态/静态数据、AIS 轨迹回放与 AIS 数据导出。 |
| **Description** | AIS data and parsing: AIS messages, vessel identification, dynamic/static data, track replay and AIS export. |
| **触发词** | AIS、报文、MMSI、轨迹回放、AIS 数据 |
| **Trigger terms** | AIS, message, MMSI, track replay, AIS data |

---

## 技能实现顺序建议 / Suggested Implementation Order

可按业务依赖与优先级依次实现，例如：

1. **船位** / Ship Position — 基础位置能力  
2. **AIS** / AIS — 与船位强相关  
3. **档案** / Archive — 船舶与公司基础数据  
4. **港口** / Port — 靠离泊与港口上下文  
5. **航程** / Voyage — 航次与挂港  
6. **航线** / Route — 航线与航路  
7. **性能** / Performance — 基于航程与船位  
8. **气象海况** / Weather & Sea Conditions — 航行安全与规划  
9. **船队** / Fleet — 多船聚合  
10. **租船** / Charter — 商业与合同  
11. **航运** / Shipping — 市场与行业  

可根据 ClawHub 与产品规划调整顺序。

---

## 文档信息 / Document Info

| 项目 | 值 |
|------|-----|
| 应用 / Application | HiFleet Claw |
| 目标平台 / Target | ClawHub |
| 语言 / Language | 中文、English |
| 版本 / Version | 1.0 |
