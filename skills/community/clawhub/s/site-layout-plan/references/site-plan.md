# 完整平面布置与三阶段

> 本文件由 SKILL.md 按需加载；内容与 0.7.2 代码同步。

### 设施分类（37 类）

| 组 | 分类键 |
|---|---|
| 起重/垂直运输 | `tower_crane` 塔吊、`construction_elevator` 施工电梯 |
| 道路/出入口 | `site_access` 大门、`permanent_road` 永久道路、`temporary_road` 临时道路、`fire_access` 消防车道、`hoarding` 围挡 |
| 临水临电/消防 | `temporary_power` 临时用电、`distribution_room` 配电室、`transformer` 变压器/箱变、`primary_distribution_box` 一级箱、`temporary_water` 临时给水、`drainage_ditch` 排水沟、`fire_water` 消防给水、`fire_hydrant` 消火栓、`fire_pump_room` 消防泵房、`fire_water_tank` 消防水池 |
| 生产/堆场 | `steel_processing` 钢筋加工区、`wood_processing` 木工加工区、`mortar_processing` 砂浆/砌体加工区、`processing_zone` 通用加工区（旧数据兼容，生成器不主动生成）、`material_yard` 材料堆场、`wheel_wash` 洗车池、`weighbridge` 地磅 |
| 办公生活 | `staff_dormitory` 员工宿舍区、`worker_living_zone` 工人生活区、`canteen` 食堂、`toilet_shower` 卫生间/淋浴间、`drying_area` 晾晒区、`site_office` 办公区、`parking` 停车场；`temporary_dormitory` 临时宿舍、`temporary_building` 食堂/厕所等旧临建仅保留兼容读取 |
| 文明施工 | `notice_board` 九牌一图、`safety_podium` 安全宣讲台、`waste_pool` 垃圾池 |
| 周边条件 | `site_boundary_neighbor` 相邻地貌/周边 |

别名（`crane`、`gate`、`hydrant`、`dormitory`、`nine_boards` 等）自动归一；未收录分类直接报错，不静默归到“其他”。

### 设施 JSON（`cad-site-facility/v1`）

```json
{
  "schema": "cad-site-facility/v1",
  "project": "示例项目",
  "coord_unit": "mm",
  "contract": {"contract_id": "...", "source_sha256": "...", "reader_version": "0.41.0"},
  "facilities": [
    {"id": "F-ROAD-01", "category": "temporary_road", "name": "西侧临时主路",
     "geometry": {"type": "polyline", "points": [[0, 0], [90000, 0]]},
     "width_m": 4.5, "source": "reader", "confidence": "candidate",
     "active_stages": ["earthwork", "structure", "finish"],
     "evidence": [{"kind": "layer", "layer": "临时道路"}]}
  ]
}
```

- `geometry.type`：`point`（`xy`）、`polyline`（`points`，可 `closed`）、`polygon`（`points`）。
- 坐标按 `coord_unit` 声明换算；无单位或单位冲突 → exit 4，不猜。
- `width_m` 用于道路/消防车道宽度校核；未给时按 `temporary_road_default_width_m=4.0` 计并标 `manual`。
- `active_stages` 缺省按分类默认阶段；显式给空数组表示该设施不进入任何阶段。
- 塔吊默认阶段为 `["structure"]`：土石方阶段尚未安装、装饰阶段通常已拆除；确需跨阶段使用（如幕墙、大型设备吊装）时显式写 `active_stages: ["structure","finish"]`。
- 自动候选的阶段约定：钢筋加工区只进 `structure`；木工、砂浆/砌体加工区进 `structure+finish`（装饰阶段仍需少量砂浆/砌体）；材料堆场、施工电梯进 `structure+finish`；变压器、消防泵房、消防水池、排水沟、垃圾池、办公生活区、临水临电、消防设施进全阶段；洗车池/沉淀池默认进 `earthwork+structure+finish`（施工全过程车辆冲洗），仅土方阶段设置时须显式改 `active_stages`。
- `source`/`confidence`/`evidence` 原样保留，便于回图核对；`candidate` 不等于已确认。

### 三阶段

| 阶段 | 键 | 默认必备（缺 → rule 13 fail） |
|---|---|---|
| 土石方 | `earthwork` | 出入口、临时道路、消防车道、临时用电、洗车池 |
| 主体 | `structure` | 出入口、临时道路、消防车道、临时用电、塔吊、施工电梯、加工区（任一拆分加工区可满足）、办公区 |
| 装饰 | `finish` | 出入口、临时道路、消防车道、临时用电、施工电梯、垃圾池、办公区 |

阶段是**布置生效范围**，不是施工进度计划；`stage-changes.json` 只反映 `active_stages` 的增减（含塔吊进场/退场），不代表已审批的工序穿插。

### 自动候选布置

`generate_site_layout.py` 可在红线、主体轮廓、道路骨架和周边条件内自动生成 A/B/C 三套候选，并逐套跑本文件的 26 条规则、道路 R1~R4 和周边校核。所有自动设施固定 `source=auto-layout`、`confidence=candidate`；详见 `references/generator.md`。自动布置不是最优解，必须逐项确认。

### 生活区分设（0.7.0）

0.7.0 不再用一个“临时宿舍”混指管理人员宿舍和工人生活区：

- `staff_dormitory` 员工宿舍区：独立区域设施，自动布置时按形心避开塔吊回转半径。
- `worker_living_zone` 工人生活区：作为**生活区包络**，本身没有独立建筑轮廓；食堂、卫生间/淋浴、晾晒区是它的子块。
- `canteen`、`toilet_shower`、`drying_area`：子块必须写 `attrs.parent_id=<工人生活区 id>`、`inside_parent=true`，且多边形完全位于父包络内；规则 25 检查父区域有效性与完全包含，规则 14 通过 `parent_id` 识别父子关系，不把“子块在父区域内”误报成几何冲突。
- 自动生成把三块尺寸组合放在一起搜索（100%/85%/70%/60%/50% 五档），先保证最差一块的保持比例，再比总面积；默认净距 0.8 m，无解时降到 0.6/0.5 m 并写 `assumptions`。
- 生活区包络或子块被场地夹逼降级时写 `size_degraded=true` 和中文 `size_note`。降级只代表“图上放得下”，不代表人数、床位数、食堂面积、消防疏散或上风向已经满足；必须按项目人数、地方临建标准和消防专项重新确认。
- 规则 23 只做平面距离代理，无风玫瑰/未声明上风向证据时恒为 `manual`；规则 24 检查道路是否穿越生活区、消防车道可达性与不少于 2 个疏散口的证据；规则 26 只比最近大门，不替代门禁与人车分流。

### 调用

```bash
cd site-layout-plan
python3 scripts/build_site_plan.py \
  --base-map out/prepared/base-map.json \
  --facilities out/facilities.json \
  --cranes out/塔吊识图/总图.crane.json \
  --stages all \
  --out-dir out/site-plan
```

可选：`--stages earthwork,structure`、`--rule-param fire_lane_min_width_m=4`、`--allow-source-mismatch`（只出比对草稿）。

输出：

```
out/site-plan/
├─ layout-earthwork.dxf / .png
├─ layout-structure.dxf / .png
├─ layout-finish.dxf / .png
├─ stage-earthwork.json / .md
├─ stage-structure.json / .md
├─ stage-finish.json / .md
├─ selfcheck-<stage>.json
├─ titleblock-<stage>.json
├─ layers-<stage>.csv
├─ coordinates-<stage>.csv
├─ stage-changes.json / .md
└─ manifest.json
```

### 出图内容（0.6.7）

- DXF 中尺寸使用真 `DIMENSION` 实体，保留在 `DIM-尺寸` 图层，不炸开；覆盖设施间净距、道路宽度、消防车道宽度、塔吊回转半径、施工电梯距结构边五类（本阶段有数据时）。
- `COORD-坐标` 图层绘制关键定位点，并输出 `coordinates-<stage>.csv`；CSV 必须等于模型坐标点全量，图内表按优先级截取关键点（最多 40 行），不得把弧段上百个点硬塞进图内。
- PNG 同步绘制尺寸线、坐标标记/表格、指北针、20m 比例尺和“设施/线型/标注/说明”四分区图例。
- 缺主体结构轮廓时，施工电梯距结构边不得静默省略，自检第 8 项降级 `manual` 并列出原因；单个 `DIMENSION` 渲染异常同样进入 `dimension_failures`。
- 三阶段自检共 12 条：原 7 条 + 尺寸覆盖、坐标全量/关键点子集、指北针/比例尺/图例分区、无文字重叠/无未放置标注、坐标表文字无横压。
- 设施标签、塔吊型号/臂长、坐标编号统一走 `site_layout/annotate.py` 的确定性排版：贴边直放 → 引线外移 → 换位 → 缩到 60% → 编号入图例；仍放不下记 `unplaced`，第 11 条判 fail，不静默把文字压在图元上。
- 消火栓数量按消防车道长度、保护半径和间距动态计算；图中数量与指标、规则校核使用同一份设施数据。
- DXF 保存后会独立复扫 `TEXT-标注`、`CRANE-塔吊`、`COORD-坐标` 的矩形重叠，复扫结果写 `dxf_label_overlaps`，与排版器自检相互校验。

### 26 条规则

| # | 规则 | 依据 | 缺证据时 |
|---:|---|---|---|
| 1 | 用地红线闭合 | 规范 | fail |
| 2 | 设施锚点在红线内 | 规范 | manual（无红线） |
| 3 | 道路/消防车道宽度 | 规范 | manual（无宽度按默认值） |
| 4 | 临时道路与出入口连通 | 规范 | manual（缺出入口） |
| 5 | 消火栓间距/保护半径 | 规范 | manual |
| 6 | 宿舍/办公避开塔吊回转半径 | 规范 | pass（本阶段塔吊已退场/无临建）；未提供塔吊才 manual |
| 7 | 配电室/一级箱供电距离 | 经验 | manual |
| 8 | 加工区与办公/宿舍分离 | 经验 | pass（本阶段未设加工区，标“不适用”） |
| 9 | 九牌一图/宣讲台位置 | 经验 | manual |
| 10 | 垃圾池卫生间距 | 经验 | pass（本阶段未设垃圾池，标“不适用”） |
| 11 | 永久道路与临时道路结合 | 经验 | manual |
| 12 | 相邻地貌/周边条件 | 经验 | manual |
| 13 | 阶段必备设施齐全 | 规范 | fail |
| 14 | 设施几何冲突 | 经验 | pass/manual |
| 15 | 消防车道净空 | 规范 | 恒 manual（平面图判不了净高） |
| 16 | 钢筋加工区隔离 | 经验 | pass（本阶段未设钢筋加工区）；缺办公/宿舍或距离不足 → manual |
| 17 | 木工加工区隔离与防火 | 经验 | pass（本阶段未设木工加工区）；人员区/配电设施过近 → manual |
| 18 | 砂浆/砌体加工区隔离 | 经验 | pass（本阶段未设砂浆加工区）；缺办公/宿舍或距离不足 → manual |
| 19 | 消防泵房与消防水池 | 经验 | manual（缺泵房/水池）；成组且靠近消防车道才 pass |
| 20 | 变压器安全距离 | 经验 | manual（未提供变压器或距离不足） |
| 21 | 排水沟连续与排放 | 经验 | manual（缺排水沟、未连通、无沉淀池或未接入） |
| 22 | 出入口洗车/称重组织 | 经验 | manual（缺地磅；洗车台未跨接入道路；距门/主路超经验值） |
| 23 | 生活区与作业面分离 | 经验 | manual（无生活区、距离不足或未证明上风向）；重叠 → fail |
| 24 | 生活区道路与消防疏散 | 规范 | pass（本阶段无生活区）；缺消防车道/超距/疏散口证据 → manual；道路穿越 → fail |
| 25 | 生活区配套完整性 | 经验 | manual（缺宿舍载体/食堂/卫生间，子块未声明有效父区域或超出父区域） |
| 26 | 办公区靠近主出入口 | 经验 | manual（缺办公区/出入口或超距）；50 m 仅提示，不设硬性 fail |

阈值可用 `--rule-param key=value` 覆盖；默认值见 `site_layout/siteplan.py::DEFAULT_PARAMS`。规则只做“候选问题定位”，不替代规范审查。规则 26 的 50 m 是经验提示，超距写 `manual` 供人工判断，不阻断出图。

规则 13 的阶段必备“加工区”可由 `steel_processing`、`wood_processing`、`mortar_processing` 任一满足；`processing_zone` 仅为旧数据兼容，生成器不再主动生成。

规则 16-20 的距离不足当前判 `manual`（不是 `fail`），因为属于经验控制值，需现场噪声、防火和电气专项复核；规则 20 的安全距离按矩形边到边净距计算，不按中心距。规则 21 在本阶段无洗车池/沉淀池时同样判 `manual`，不伪写 `pass`。排水沟连通支持端点相接和 T 形接入；闭合环沟按首尾闭合段参与判断。规则 23 在无风玫瑰时只能 `manual`；规则 24 的道路穿越是 `fail`，消防车道超距或疏散口证据不足是 `manual`；规则 25 的配套缺失和父区域问题均为 `manual`。

### 规则 14 的口径

规则 14 只判**设施与道路带**的占地冲突，不把临时给排水/消防水管线穿越加工区误报为设施冲突；共线消防车道通过 `attrs.shared_with` 标记后不重复报冲突。工人生活区与其食堂/卫生间/晾晒子块必须由 `attrs.parent_id` 明确声明父子关系，规则 14 据此跳过“子块天然落在父区域内”的包含判断；不能靠几何包含关系猜父子。洗车台和地磅按功能必须跨路/压路布置，不按“设施压路”报冲突，其贴路关系由规则 22 单独校核。

### 出入口服务带（0.6.7）

自动布置把出入口作为一条服务带处理，而不是把九牌、洗车台、地磅分散到场地空地：

- **九牌一图**：`notice_board` 是 `area`，按 9 块×1.2 m 宽板直线排布，端部 0.2 m，总长 11.0 m；沿大门侧围挡/红线内侧滑动避让接入道路与洗车台，图内画 8 条内部分隔线；板面朝向场地内侧。板数、朝向、围挡基础和内容仍需现场确认。
- **洗车台**：`wheel_wash` 跨第一个大门接入道路布置，属性 `layout=drive-through`、`on_access_road=true`；长度取 12 m 与接入段余量的较小值、最小按 3.2 m 表达，宽度 5.0 m，小于 6 m 时标 `short_pad=true` 并要求专项确认。沉淀池容积、坡度、循环水和排水去向未定。
- **地磅**：`weighbridge` 沿大门主环道直段布置，长边顺行车方向，属性 `layout=on_main_road`，按 100 t 占位：B 型 14 m×4.8 m 外轮廓（3 m 宽称重台＋引坡/传感器），A 型 12 m、C 型 16 m；型号、基础、排水、检定和超限车绕行未定，且不替代计量检定。
- **多门假设**：当前自动布置默认第 1 个大门为主重车出入口；多门项目在洗车台/地磅 `attrs` 中写 `gate_index=1`、`gate_count`、`main_gate_assumption=true`，必须现场确认主门。规则 22 的经验阈值：洗车台距门≤30 m、距路≤8 m；地磅距门≤60 m、距路≤10 m。

### 三阶段评分

`evaluate_scheme()` 支持三阶段汇总：任一阶段 `fail` 即硬伤；人工项取并集；分数取最不利阶段；输出 `evaluated_stages`、`stage_summary`、`manual_total`。评分是内部比选，不是评标分。

