# v1.0.0 总验收表（C5）

生成时间：2026-11-17 · 技能：shizheng-suanliang v1.0.0
规则：逐项「证据 + PASS/FAIL」，FAIL 不得标完成。

## 阶段 A · 代码完整性

| # | 任务 | 证据 | 结果 |
|---|---|---|---|
| A1 | fixture 落盘 ≥5 | `tests/fixtures/` 6 个（含真实形态 real_contract_no_unit.json）+ `make_fixtures.py` 再生器 | PASS |
| A2 | CLI 退出码全覆盖 20/21/22/23/24/3/5 | `tests/test_entry_gate.py` 19/19 PASS（真实子进程沙箱） | PASS |
| A3 | 内置 --self-test | 10/10 PASS（临时目录独立运行） | PASS |
| A4 | 边界单测 ≥7 项 | polyline 拆段/去重/缺四元组/脏宽度/多档取多数/m 单位/井多系统/段长字段优先 + RealForm 3 项 + CaliberEnhancement 6 项；单测 35/35 OK | PASS |
| A5 | 交叉平台 lint | `lint_cross_platform.py` 34 文件 0 问题（BOM/CRLF/非 ASCII 文件名/语法） | PASS |
| A6 | 文档死链扫描 | 通过；`docs/runtime.md` 已补齐 | PASS |

## 阶段 B · 功能实用性

| # | 任务 | 证据 | 结果 |
|---|---|---|---|
| B1 | 真图验证 ≥2 张 | 经十一路室外管网（7 系统 24733~28443 m、管径 4 档、井 18 座+密度警告）+ 总平面竖向图（道路中线 23.9 km）；5 处真 bug 修复 | PASS |
| B2 | 井规格分档 | raw φ/DN 提取、表外只计数；单测 + 真图输出含规格列 | PASS |
| B3 | 管径×图层级弱配对 | `pipe_length_by_layer_ref`，evidence_grade=weak，不进主口径；单测验证与主口径隔离 | PASS |
| B4 | 桩号/标高/坡度复核表 | `survey_review_table` 全量透传；真图 272 行 | PASS |
| B5 | 道路面积双口径 + --road-width | 中线 vs 边线÷2，偏差>10% 警告；单测两方向 + 真图复核 | PASS |
| B6 | 井密度座/百米 | 按系统输出，含工程常规对照注释；真图 0.1 座/百米如实暴露识图漏检 | PASS |
| B7 | 文档同步 | references/on-demand.md §6-10、README 参数说明与输出一致 | PASS |

## 阶段 C · 生产能力

| # | 任务 | 证据 | 结果 |
|---|---|---|---|
| C1 | bus 正式链路实测 | 真图契约 push → `--from-contract` pull → formal 算量；contract_mode=formal、formal_ledger_eligible=true、contract_id=cadc1-8bbdf93fcdf3b261 可追溯；量与 manual 一致 | PASS |
| C2 | 性能基准 | 5 万段几何+800 构件+2000 标注：_extract 0.49s、build 0.83s、合计 1.32s | PASS |
| C3 | 一键回归脚本 | `scripts/run_regression.sh` 6 套件一键 PASS（FAIL 即整体 FAIL） | PASS |
| C4 | 三平台发布 v1.0.0 | GitHub/SkillHub/ClawHub 同步；发布后回查见发布记录 | PASS（本次发布完成时点） |
| C5 | 总验收表 | 本文件 | PASS |

## 边界固化（发布版口径声明）

- 估算带 ±15%，`final_quantity=false`，定位为计划口径；不进清单/结算/竣工计量。
- 不做土方、桥隧构件量；不做管径×段长强配（缺配对依据）。
- 宽度标注缺失时面积 unavailable，不默认；人工传参用 `--road-width` 显式指定。
- 识图层已知短板（井类图块召回低）以井密度警告如实提示，不静默修补。

## 已知遗留（不阻塞发布）

1. 识图包 municipal-geometry 井类召回率偏低（工程常规应有数百座井的图只识别 18 座）——属 cad-file-reader 改进项，算量层已用密度警告兜底提示。
2. 道路宽度标注在识图层无独立类型，依赖 dimension 原文或 `--road-width` 人工传参。
3. 长链路（cad_scan 识图）大图耗时依图纸规模，算量层毫秒级不是瓶颈。
