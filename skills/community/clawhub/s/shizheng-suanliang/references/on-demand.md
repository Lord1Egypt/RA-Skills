# 口径全文（on-demand）

## 0. 真实契约形态（重要）

真实识图契约（`cad_municipal_geometry.py` 产物）的枚举值是**英文键**，不是中文：

- `system`：`rainwater/sewage/water_supply/reclaimed_water/heating/gas/power/telecom/drainage/fire_protection/road/bridge/...`（映射表 SYSTEM_EN_TO_ZH，22 键）。
- `components[].category`：`manhole` 等 component_rules 英文键；井的子类（检查井/雨水口/跌水井/阀门井/泵站）从 `raw` 原文细分。
- `municipal_geometry[].category`：命中 component_rules 的英文键（如 `road_centerline`）；**管道图层**不命中时 `category=unclassified_municipal`、`system=英文键`、`status=review`——管道延米主要靠这类行。
- `labels[].label_type`：`station/elevation/coordinate/pipe_size/slope/dimension`，**没有宽度类型**；宽度从 `dimension` 标注的 value+raw 原文捞。
- `municipal_geometry[].length_drawing_units`：识图包现成段长，优先直接用，缺了再按 geometry 四元组算。

手工/旧版中文形态（category="雨水管" 等）走中文正则回退路径，两路结果一致（单测覆盖）。

## 1. 管道延米

- 证据来源：`municipal_geometry[]` 中 `_is_pipe_geometry()` 命中的行——英文 `system` 键 ∈ 管道系统键集，或 category/system/layer 文本命中中文回退正则（管道/管线/管网）。
- `status=review` 的管道段（市政图层未映射到构件类别，真实图里这是管道段常态）**计入延米**并单独出警告，提示人工核对。
- 单段长 = `length_drawing_units`（缺则 geometry 欧氏距离）× `unit_scale`（非 mm 单位时），合计后 ÷1000 → m。
- 分组：category+system+layer 文本命中 雨水/污水/给水/再生水/热力/燃气/电力/通信/排水 → 对应系统；全部未命中 → 「未分类」并出警告（不硬套）。
- 估算带：合计 ×[1.00, 1.15]。图面口径偏低的已知原因：工作井内接管、预留支管、图幅外管线、双线表示法重复计数与否各家不一。
- `connectivity.summary.open_endpoints` 非零时追加警告：管道不连通处（断头/图幅边界），延米可能偏少。

## 2. 管径分档（只计数）

- 证据来源：`pipe_network[].pipe_size / raw / system` 文本，正则 `(?:DN|De|d|D|Φ)\s*[=＝]?\s*(\d{2,4})`。
- 分档：≤300 / ≤400 / ≤500 / ≤600 / ≤800 / ≤1000 / ≤1200 / ≤1500 / >1500。
- **不做管径×几何段强配**：契约没有"哪段几何属于哪根管径"的配对证据，强配即编造。
- 未提取到管径的管道候选：计数进警告，不进分档。

## 3. 井类计数

- 证据来源：`components[]` category 命中 检查井/雨水口/跌水井/阀门井/泵站/井。
- 按系统分组计数；`connectivity.summary.junction_candidates` 只作交叉核对展示，不并入计数（汇聚点是几何候选，不等于井）。
- 同名多口径（如"检查井 φ1000"与"检查井 φ1250"）不细分规格——缺规格统计依据，只出类别总数。

## 4. 道路面积带

- 中线段长：`municipal_geometry[]` category 命中 道路中线/中线/边线/路缘石 的段长合计。
- 宽度：`labels[]` 文本命中 宽/车道/红线/断面 且含 `(\d+(\.\d+)?)\s*(m|米)`，值域 2~100 m 过滤；取**多数档**（出现次数最多的宽度值）。
- 面积带 = 中线长 × 宽度 ×[1.00, 1.15]。
- 缺中线段或缺宽度标注 → 对应项进缺项清单，面积 `unavailable`，**不默认宽度**（城市次干路 40m、支路 20m 之类经验值一概不用）。

## 5. 路面材料/做法清单

- 证据来源：`materials[]`（category/value/layer）。
- 只列清单；文本含层厚（如 4cm）不提取分层面积——分层面积需要该层铺筑范围证据，契约没有，算了就是编造。

## 6. 单位与换算

- 契约 `coordinate_unit=mm` → 直接算。
- 其他单位必须有顶层 `unit_scale`（换算到 mm 的系数，如 m 图给 1000）；缺 `unit_scale` 抛 `GuardError(4)`，本批次只出计数与缺项清单，不出长度/面积。

## 7. 输出

- `<out-prefix>.json`：全量结果（schema `cad-municipal-qty/v0.1`），带 provenance/contract_id/哈希/warnings/缺项清单/待复核透传。
- `<out-prefix>.md`：可读复核报告（管道带、管径档、井表、道路面积带、材料清单、缺项、连通性、警告）。
- `<out-prefix>.csv`：台账（item_type/system/category/quantity_low/quantity_high/unit/basis/final_quantity）。
- `site_handoff.json`：下游用交接（管道系统行）。
- 所有量行 `final_quantity=false`；manual 模式整体 `formal_ledger_eligible=false`。

## 8. 明确不做

- 土方（挖/填）：无横断面填挖数据。
- 桥梁/涵洞/隧道构件量：缺配筋/截面/标高证据。
- 水力计算、结构计算、交通组织、设计合规。
- 正式清单量、竣工计量、结算量。

## 9. 缺项清单机制

任何缺证据的项写明「算什么 + 缺什么」，例如：
- `管道延米：市政管道图层无几何段（缺 municipal_geometry 管道段证据）`
- `道路面积：labels 无宽度标注（车道/红线宽），不默认宽度，面积 unavailable`

按缺项清单回 cad-file-reader 补参数或人工给值，不要相信"跑通了就是对的"。

## 6. 井规格分档（B2）

- 证据来源：井类 components 的 raw 原文（φ/DN/纯数字 600~3000）。
- 输出 `wells_count` 中以「井规格 φNNNN」行呈现，仅计数；表外规格只计数不归档。
- 真图注意：连接性文字（如「排至市政污水井」）不产规格，规格列可能为空——如实呈现。

## 7. 管径×图层级弱配对（B3）

- 输出 `pipe_length_by_layer_ref`：同 layer 的管道几何段长合计 × 该 layer 管径候选。
- 每条 `evidence_grade: weak`，仅供参考，**不进主口径**；主口径仍是系统延米带。

## 8. 桩号/标高/坡度复核表（B4）

- 输出 `survey_review_table`：labels 的 station/elevation/slope 全量透传，不算量，供人工复核。

## 9. 道路面积双口径交叉核对（B5）

- 中线口径 = 中线段长 × 宽度；边线口径 = 边线段长 ÷ 2 × 宽度。
- 两口径偏差 >10% 出警告（道路图层可能混入非道路线段）。
- `--road-width M` 显式传参替代缺失标注，**不默认**；`edge_crosscheck.evidence_grade=weak`。

## 10. 井密度（B6）

- `wells_count` 中按系统输出「井密度（座/百米）」= 井数 ÷（管道 m/100）。
- 工程常规 2.5~3.3 座/百米；显著偏低配合井密度警告提示识图层漏检。
