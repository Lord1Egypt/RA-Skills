# CHANGELOG — shizheng-suanliang

## 1.1.1 (2026-11-17) — ClawHub 扫描问题修复

- 哈希链状态机器可读：guard 输出新增 `hash_chain_status`（verified / unverified_no_embedded_hash /
  require_hash_off），算量结果 stamp 透传；缺内嵌哈希的警告升级为可程序判定的显式状态。
- 新增 `--strict-hash`：require_hash=True 且契约未内嵌 contract_sha256 时按硬失败拒入（exit 2），
  供正式链路需要强校验时使用；默认行为不变（警告放行，兼容识图直连形态）。
- formal bus 分支修复：`--from-contract` 现在正确透传 `--unit-scale` / `--road-width` 手工参数
  （此前静默忽略，与文件入口行为不一致）。
- 底座同步：contract_guard.py 更新后经 sync_base.py 同步 5 个兄弟 skill，全族 self-test 6/6。
- 回归：单测 44/44（新增 HashChainTests 3 项）、entry_gate 19/19、self-test 10/10、guard 6/6、
  lint 112 文件 0 问题、run_regression.sh 全 PASS。

## 1.1.0 (2026-11-17) — 遗留问题优化批次 + 蓝标图示

- 识图层 rules 增强：municipal-geometry component_rules 新增消防车道类图层直接映射——
  road_centerline += 消防车道/消防道路/消防通道/消防环路/消防车道中心线/FIRE LANE/FIRE TRUCK ROUTE；
  road_edge += 消防车道边线/消防道路边线/FIRE LANE EDGE（防误收）。合成用例 17 项命中与无误伤全过；
  真图缓存回归确认既有分类无扰动。两侧（workbuddy/codex cad-file-reader 副本）同步。
- 底座同步：新增跨 skill 同步工具 `sync_base.py`（--status/--verify/--sync）；contract_guard.py 全族统一到
  shizheng 版（空 unit 分支修复 + audit 形态放行），5 个兄弟 skill 同款 bug 修复并回归通过。
- 哈希链：识图契约 source_sha256 由 null(source_not_found) 修复为真实原图哈希（从 detail.source_paths 取
  DWG 算 sha256，与 shasum 比对一致），formal 链路可校验。
- 弧段口径：市政识图新增 ARC 弧段提取（ezdwg decode_arc_entities + 图层归属，弧长=半径×圆心角），
  弧长替代弦长；真图对比道路中线 14360.9 → 16839.9 m（+17%）；review 弧段按管道同口径计入+警告；
  unclassified 直线段不归类（可能是边线/红线）。SPLINE 曲线暂不支持（边界已记录）。
- 蓝标图示：输出按管线综合国标色系的系统色标图例——md 新增「系统色标图例」表格章节 + 同前缀 SVG 图示文件
  （雨水/污水/给水/热力/燃气/电力/通信等色标）。
- 回归：单测 41/41、entry_gate 19/19、self-test 10/10、guard 6/6、lint 103 文件 0 问题、run_regression.sh 全 PASS。

## 1.0.0 (2026-11-17) — 首个正式版（三平台发布）

阶段 A/B/C 全部完成后的正式版：

- 完整性：CLI 退出码全覆盖（19/19）、内置自检（10/10）、真实形态 fixture 回归（单测 35/35）、交叉平台 lint。
- 实用性：2 张真实 DWG 全链路验证（管网+竖向），口径含管道延米带、管径分档、井规格/密度、
  道路面积双口径、survey 复核表、图层级弱配对；缺项与警告全程如实。
- 生产能力：bus 正式链路（push→pull→formal，contract_id 可追溯）、5 万段 1.32s 性能基准、
  一键回归 run_regression.sh。

## 0.3.0 (2026-11-17) — 阶段 B 口径增强 + 阶段 C1-C3

- C1 bus 正式链路实测：真图契约 push → --from-contract pull → formal 算量（contract_mode=formal，
  formal_ledger_eligible=true，contract_id=cadc1-8bbdf93fcdf3b261 可追溯）；量与 manual 路径完全一致；
  修复 bus 路径 contract_id 取值（嵌套 contract.contract_id）。
- C2 性能基准：5 万段几何 + 800 构件 + 2000 标注，_extract 0.49s、build 0.83s，合计 1.32s。
- C3 一键回归：scripts/run_regression.sh（6 项套件一键跑，FAIL 即整体 FAIL）。

- B2 井规格分档：井 raw 提取 φ/DN 规格，表外只计数。
- B3 管径×图层级弱配对：`pipe_length_by_layer_ref`，evidence_grade=weak，不进主口径。
- B4 桩号/标高/坡度复核表：`survey_review_table` 全量透传不算量。
- B5 道路面积双口径：中线 vs 边线/2，偏差>10% 警告；新增 `--road-width` 显式传参。
- B6 井密度：按系统输出座/百米（常规 2.5~3.3）。
- B7 文档同步：references/on-demand.md §6-10、README 参数说明。
- 回归：单测 35/35（新增 CaliberEnhancementTests 6 项）、entry_gate 19/19、self-test 10/10、guard 6/6、lint 33 文件 0 问题。
- 真图复核：经十一路管网图 + --road-width 20 输出中线 14360.9 m × 20 m = 28.7~33.0 万 m²。

## 0.2.0 (2026-11-17) — 真图全链路验证通过

用 2 张真实 DWG（经十一路室外管网、总平面竖向图）跑通 cad_scan → 市政识图 → 算量全链路，据此修复：

- 闸门：嵌套 contract.contract_id 识别（此前误报 GuardError 3）；空 coordinate_unit 误入非 mm 分支；
  缺 coordinate_unit 但带 scale_unit_audit（市政识图形态）放行为警告。
- 单位：新增推断链 audit 证据 → 坐标量级（≥1e5 测量坐标判 m）→ 歧义区停算；m 图按固有 1m=1000mm 换算；
  新增 --unit-scale 手工兜底。
- 交叉核对：新增井密度警告（>100 m/座提示识图层漏检井类图块，井计数仅作下限）。
- 回归：新增 tests/fixtures/real_contract_no_unit.json 真实形态 fixture + RealFormTests 3 项（单测 29/29）。

真图结果：管网图 7 系统 24.7~28.4 km、管径 4 档、井 18 座（识图层漏检已提示）；竖向图道路中线 23.9 km、
宽度标注缺 → 面积 unavailable（正确不默认）。

## 0.1.2 (2026-11-17)
## 0.1.2 (2026-11-17)

阶段 A（代码完整性）落地：

- 内置 `--self-test`（10 项自检，合成数据+临时目录，不依赖 fixtures 目录）。
- CLI 退出码全覆盖测试 `tests/test_entry_gate.py`（19 项：20/21/22/23/24/3/5 + manual/回退/validate/self-test 真实子进程路径）。
- guard 退出码映射对齐 SKILL.md：guard 1-4 → 22、guard 5 → 24（此前直接透传 2/3/4/5）。
- manual 模式 provenance 空串回填为 `manual`（契约未写 provenance 时结果溯源缺失）。
- municipal_geometry 同段去重（layer+图幅+几何四元组一致），防识图层去重失效双计，去重数进警告。
- 段长优先用识图包 `length_drawing_units` 现成字段。
- `tests/fixtures/` 落盘 5 个合成契约 + `scripts/make_fixtures.py` 再生器。
- `scripts/lint_cross_platform.py`（BOM/CRLF/非 ASCII 文件名/语法，32 文件 0 问题）。
- 补 `docs/runtime.md`（排障速查表 + 真图全链路命令）。
- 测试 25/25 单测 + 19/19 入口闸门 + 10/10 self-test + lint 0 问题。

## 0.1.1 (2026-11-17)

对齐真实识图契约（发布前修复，基于对 cad_municipal_geometry.py/rules.json 的静态实测）：

- 真实契约 `category`/`system`/`label_type` 是英文枚举（`road_centerline`/`rainwater`/`dimension`），初版中文正则全部落空——新增英文键映射表（SYSTEM_EN_TO_ZH，22 个系统）+ 中文文本回退双路径。
- 管道几何段真实形态：`category=unclassified_municipal` + `system=rainwater` 等英文键 + `status=review`——按 system 键归类计入，并出 review 状态警告。
- 井类真实形态：`category=manhole`，子类（检查井/雨水口/跌水井/阀门井/泵站）从 raw 原文细分。
- 段长优先用识图包现成的 `length_drawing_units` 字段，缺了再按 geometry 四元组算。
- 宽度标注：真实契约无 width 类型，改查 `dimension` 标注的 value+raw 原文。
- 修复：`_extract` 内部警告未并入最终输出的 warnings（review/管径/未分类提示丢失）。
- 测试 fixture 重写为真实 schema 形态，保留中文回退用例；17/17 OK。

## 0.1.0 (2026-11-17)

初版：

- contract-only 入口：消费 `cad-municipal-geometry/v1`（cad-file-reader `municipal-geometry` 识图包产物），输出 `cad-municipal-qty/v0.1`（json/md/csv + site_handoff）。
- 口径：管道延米按系统（图面段长 ×[1.00,1.15] 估算带）；管径 DN/De/d/Φ 分档只计数不与段长强配；井类按系统计数；道路面积带＝中线段长 × labels 宽度标注多数档；路面材料只列清单。
- 入口闸门 vendored（exit 20/21/22/23/24），文件入口强制 `--allow-manual`（manual 降级，`final_quantity=false`）。
- m 单位图纸缺 `unit_scale` 时不出长度/面积，只出计数与缺项清单。
- 土方、桥隧构件量明确不做；缺依据项一律进缺项清单。
- 单测 16 项（validate/extract/build/gate）+ contract_guard 自检 6/6。
