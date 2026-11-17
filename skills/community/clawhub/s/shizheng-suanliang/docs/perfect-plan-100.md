# shizheng-suanliang 完善计划（三维度 100%）

制定日期：2026-11-17 · 当前版本 v0.1.1 · 状态：v0.1.1 已对齐真实契约形态，17/17 单测

> "100%" 的定义：不是代码行数，而是**每个维度下列出的验收标准全部达成、且有证据**。
> 达成一项勾一项，未达成不标完成。

## 一、需求

| 维度 | 100% 验收标准 |
|---|---|
| 代码完整性 | 全部固定退出码有测试覆盖；真实契约 fixture 落盘；内置 `--self-test`；文档引用零死链；边界用例（多段折线/重复段/脏标注/单位异常）全过 |
| 功能实用性 | 真图验证 ≥2 张市政施工图全链路通过；新增 4 项实用口径（井规格分档、管径×图层级弱配对参考口径、桩号/标高/坡度复核表、井密度指标）且全部带证据标注 |
| 生产能力 | bus 正式链路 push/pull 实测通过；万段级 geometry 性能基准有数；SkillHub 发布并回查 approved/isLatest（须用户明确下令）；回归脚本可复跑 |

## 二、现状（诚实基线）

**已达成**：contract-only 架构 + 入口闸门（exit 20/21/22/23/24/3/5）+ 真实契约英文枚举对齐 + 中文回退 + 17 项单测 + contract_guard 自检 6/6 + 示例端到端 + 口径文档。

**未达成（按维度）**：

- 完整性：CLI 层退出码只测了 3/23（20/21/22/24 未测）；无 tests/fixtures 落盘 fixture；无内置 `--self-test`；无交叉平台 lint；SKILL.md 曾引用不存在的 docs/runtime.md（已补，2026-11-17）。
- 实用性：**零真图验证**；井类无规格分档；管径与段长零配对；桩号/标高/坡度标注未透传；道路面积只有中线单一口径。
- 生产能力：statesync 薄壳未实测；无性能基准；无回归脚本；未发布（等用户指令）。

## 三、可行性

- 识图层（cad-file-reader municipal-geometry）已产出全部所需证据：`length_drawing_units`、`labels`（station/elevation/slope/dimension）、`connectivity`、`pipe_network[].pipe_size/layer`——新增口径**只消费已有契约字段，不需要改识图层**。
- 井规格从 `raw` 原文提取（φ1000/1250 类），与管径提取同一套正则思路，风险低。
- 管径×段长只做**图层级弱配对**（同 layer+sheet 的几何段合计 × 该层管径候选），不虚构"哪段属于哪根管"，证据等级明标 `weak`。
- 性能：算量层是 O(n) 求和，万段级无风险；基准只为留证据。
- bus 接线复用 cad_statesync_core 共享核心，钢结构侧已实测可用，市政侧预期一次跑通。

## 四、设计与步骤（三个阶段，顺序执行）

### 阶段 A · 代码完整性 → 100%（纯本地，无外部依赖）【已完成 2026-11-17，v0.1.2】

| # | 任务 | 验收证据 | 状态 |
|---|---|---|---|
| A1 | `tests/fixtures/` 落盘：real_contract.json（真实 schema）/ legacy_chinese.json / empty_evidence.json / m_unit_scale.json / forged_no_id.json + `make_fixtures.py` 再生器 | 5 个 fixture 已落盘，可 `python3 scripts/make_fixtures.py` 再生 | ✅ |
| A2 | CLI 退出码全覆盖：20/21（CODEX_SKILLS_ROOT 沙箱）、22（伪造来源/版本 v0）、24 路径、3、23、5 | `tests/test_entry_gate.py` 19/19 PASS | ✅ |
| A3 | `municipal_qty.py --self-test`：内置 10 项自检 | exit 0，10/10 PASS | ✅ |
| A4 | 边界单测：polyline 拆段累加、同段重复去重、geometry 缺四元组、labels 脏值、多宽度档取多数、unit_scale=1 非 mm、井多系统分组、length_drawing_units 优先 | BoundaryTests 8 项，单测合计 25/25 OK | ✅ |
| A5 | 交叉平台 lint：BOM/CRLF/非 ASCII 文件名/语法 | `scripts/lint_cross_platform.py`：32 文件 0 问题，exit 0 | ✅ |
| A6 | 文档死链扫描：SKILL.md/README 引用的文件全部存在 | 扫描通过（另补齐缺失的 docs/runtime.md） | ✅ |

> 附带修复：guard 退出码映射（1-4→22、5→24）对齐 SKILL.md；manual 模式 provenance 空串回填；段长优先用识图包 length_drawing_units。

### 阶段 B · 功能实用性 → 100%（依赖阶段 A 的 fixture + 真图）

| # | 任务 | 验收证据 |
|---|---|---|
| B1 | **真图验证 ×2**：道路类 1 张 + 管网类 1 张，跑 `cad_scan → municipal-geometry → municipal_qty` 全链路（本机）；人工核对：管径命中率、井数与图面清点、延米合理性、缺项清单如实 | 两次运行的 md 报告 + 核对结论（数据不出本机） | ✅（2026-11-17 完成：2 张真图全链路）
| B2 | 井规格分档：raw 提取 φ/DN 规格（1000/1250/1500…），表外只计数 | 单测 + 真图输出含规格列 | ✅（2026-11-17 完成，v0.3.0）
| B3 | 管径×段长图层级弱配对：同 layer+sheet 几何段合计 × 管径候选，单独输出 `pipe_length_by_layer_ref`，证据等级标 `weak`，不进主口径 | 单测：配对与不配对两口径并存 | ✅（2026-11-17 完成，v0.3.0）
| B4 | 桩号/标高/坡度复核表：透传 labels 的 station/elevation/slope 进输出（复核用，不算量） | 输出含三列表 | ✅（2026-11-17 完成，v0.3.0）
| B5 | 道路面积双口径交叉核对：中线口径 vs 边线口径（road_edge/kerb 段长×宽），偏差 >10% 出警告 | 单测 + 真图验证 | ✅（2026-11-17 完成，v0.3.0）
| B6 | 汇总页新增井密度（座/百米）按系统输出 | md 报告可见 | ✅（2026-11-17 完成，v0.3.0）
| B7 | README/口径文档同步 B2~B6 新口径 | 文档与输出一致 | ✅（2026-11-17 完成，v0.3.0）

### 阶段 C · 生产能力 → 100%

| # | 任务 | 验收证据 |
|---|---|---|
| C1 | bus push/pull 实测：statesync push 契约 → `--from-contract` 正式入口拉回计算，formal 模式全字段正确 | 一次成功会话日志 | ✅（2026-11-17 完成）
| C2 | 性能基准：合成 5 万段 geometry + 2 万 components，记录耗时/内存 | benchmarks.md 有数（预期 <5s） | ✅（2026-11-17 完成）
| C3 | 回归脚本 `run_regression.sh`：对同一契约两次运行 diff 输出（确定性校验） | 脚本 exit 0，diff 为空 | ✅（2026-11-17 完成）
| C4 | SkillHub 发布 v1.0.0 + 回查 approved/isLatest（**须用户明确说"发布"后才执行**；发布前用户核对源码） | skillhub 回查记录 |
| C5 | 版本冻结：发布前 CHANGELOG 补齐、LICENSE/NOTICE 复核 | — |

## 五、边界（本计划不做什么）

- 不给识图层提需求：`municipal-geometry` 识图能力不动，市政算量只消费其契约。
- 不做土方、桥隧构件量、水力/结构计算——证据不足，维持"明确不做"边界。
- 不做管径×段长强配——只加 weak 参考口径，不污染主口径。
- 不承诺正式清单量——所有输出保持 `final_quantity=false` 定位。
- 公司项目数据不上云：真图验证全程本机，报告脱敏后才可进发布内容。

## 六、风险

| 风险 | 影响 | 对策 |
|---|---|---|
| 真图图层命名超出识图层规则覆盖 | 管道段识别率低，延米失真 | B1 先行；识别率 <60% 时先给识图层补规则建议（单独任务，不改算量层） |
| 真图无宽度标注 | 道路面积持续 unavailable | 缺项清单如实提示 + 人工 `--road-width` 参数（B5 一并加，显式传参不默认） |
| statesync sections 与 bus 实际 schema 不匹配 | pull 命中失败 | C1 先小样演练，失败则对照 bus schemas/ 调 sections |
| 弱配对被用户误当正式量 | 口径误用 | 输出字段名带 `_ref`、md 里加粗标注"仅供参考" |

## 七、验证与完成判定

- 每阶段跑全量测试：`python3 scripts/tests/test_municipal_qty.py` + `tests/test_entry_gate.py` + `--self-test`，全绿才勾项。
- 总验收 = 一张表：A1~A6 / B1~B7 / C1~C5 逐项"证据链接 + PASS/FAIL"，FAIL 不得标完成。
- 三维度各自 100% 后，版本升 v1.0.0。

## 八、不要做什么

- 不为凑 100% 放宽口径（不给默认宽度、不做强配、不编桥隧量）。
- 不在用户明确下令前发布任何平台。
- 不把真图验证的公司项目内容写进发布包/示例。
- 不跳过 FAIL 项继续往后做。
