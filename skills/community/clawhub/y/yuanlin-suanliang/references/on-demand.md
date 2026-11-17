# yuanlin-suanliang 详细说明（由 SKILL.md 原样外移）

> 2026-11-10 瘦身：只搬未删。SKILL.md 保留硬规则、入口闸门、边界与口径摘要；命中下列主题时按需读取本文对应小节。

## 语言与区域范围

本技能面向**中文建筑工程与园林景观图纸**：规则、植物词库与输出证据默认使用简体中文，并对常见英文图例做别名兼容；地域性词表（如西北温带荒漠区植物等）明确按中文/本地场景设计。如需其他语言/区域，可通过 `--plant-library` 传入项目词库扩展，不改算法与口径。

**它解决的一件事**：把 `cad-file-reader` 的园林识图候选复算成可复核的苗木统计与铺装面积概算底稿，并明确区分“苗木表设计给定数量”“有坐标的块级实例计数”“无坐标块实例计数”“块引用总数候选”“图例文字标记次数”“铺装强算候选”等口径。

## 适用

- 苗木统计：按乔木、灌木、地被、其他分类；支持中英文常见植物图例词，并区分苗木表基线、平面图块级计数、底座无坐标块实例计数、块引用总数 P2 候选、图例文字 P2 候选。
- 植物名称参考库：内置区域/素材植物库（`rules/plant_library_*.json` 全部默认加载，含常用园林植物 349 名、西北温带荒漠区 131 条、图块素材 311 名与分区苗木选型 1022 名（去别名后新增约 700 名）），可用 `--plant-library` 叠加项目库；**只做分类**，不读规格/密度/单价，不推断规格或报价。
- 铺装面积：优先按铺装图层识别闭合区域，鞋带公式算面积，含洞/内岛按嵌套深度奇偶扣减；块内闭合铺装环由 `cad-file-reader` 展开后以契约传入，本技能不直读 DXF。
- 概算底稿与物资计划草稿：苗木数量、铺装面积、缺项、依据分层落盘。
- 真图边界验证：图层名/块名缺失的转换版 DWG，不硬出铺装面积；强算结果只标 P3 候选。

## 前置（显式依赖）
## 强依赖底座（cad-file-reader，不做弱化）

`cad-file-reader` 是强依赖底座，不是可选增强：DWG/DXF/DWT/PDF 解析、图层/文字/块/图框/几何与测量候选全部由底座完成，一次解图全项目复用；本技能只做园林专业口径的量算与台账，不重复解析图纸。底座输出候选（`final_quantity=false`），本技能输出概算底稿/物资计划草稿。缺底座或版本不足必须明确报错，不静默用错数据。

- 输入契约：苗木统计吃底座 `cad_landscape_geometry` 的 `plant_block_legends`/`plant_legends`/`plant_schedule_links`/`systems` 与 `cad_scan` 文字/块引用详情；铺装面积吃 `cad_scan --with-geom --with-geom-layer --detail-json` 详情。
- 苗木表数量单位必须来自数量表头括号或单位列，缺失时不默认"株"并降 P1；扫描件/图片型 PDF 只出苗木文字候选，不给铺装面积。
- 图纸入口已封死：`--dxf-block-paving` / `--dxf-block-refs` 不再接受图纸文件，传 `.dxf` 直接退出 `23`；块内铺装与块引用坐标去重改由 `cad-file-reader` 的 `cad_landscape_geometry.sh` 产出契约后消费。
- `lis-skill-bus` 是图纸链路的必需接线：按 `cad-contract/v1` 共享契约，缺 bus 退出 `21`，不降级成本技能自行解图；本地 `state/` 只作 bus 状态缓存。完整输入契约与安装细节见 `references/base-contract.md`。

## 使用流程

1. **识图**：用底座生成园林识图与几何详情。
2. **复算**：运行本技能脚本，得到苗木统计、铺装面积、缺项与台账。
3. **复核**：优先核对 `需核对=是`、P2/P3、含洞/内岛、强算候选行；数量/规格不确定时不猜默认。
4. **交付**：Excel 台账 + CSV + Markdown 报告，用于概算与物资计划核对，不用于结算。

## 脚本用法

```bash
bash scripts/yuanlin_qty.sh --landscape 园林识图/景观详情.landscape.json --scan 景观详情.json --out-dir ./园林概算 --project "项目名"
```

- `--rules <json>` 项目专属图层 token/词库/去重半径；`--scale` / `--drawing-mm-per-unit` 覆盖自动比例与单位（显式指定后不回改）。
- `--paving-all-geometry`（图层缺失时全几何闭环候选）结果强制 P3、`final_quantity=false`、不计主线。
- 块内铺装 / 块引用坐标去重只从 reader 契约读取；`--dxf-block-paving`、`--dxf-block-refs` 传图纸一律退出 `23`。
- `--plant-library` 只读中文名与分类章节，规格/密度/苗价一律不读；`--no-default-plant-library` 关内置区域库（只影响分类不影响数量）。
- 块引用 P2：只有总数、没有坐标的植物块引用只作复核线索，`final_quantity=false`。
- 底座识图命令、四组完整示例与参数全表见 `references/usage.md`。

## 输出

- `Yuanlin概算物资计划台账.xlsx`：固定含 `使用边界`、`苗木统计`、`铺装面积`、`缺项核对`、`汇总`、`依据`。
- `园林苗木统计.csv`：分类、来源、植物名/图例名、数量、单位、计量方式、平面图文字标记数、置信分层、证据坐标、需核对、分类依据、参考库命中、计入主线。
- `园林铺装面积.csv`：图层、区域、角色、面积、嵌套深度、计算式、证据坐标、需核对、计入主线。
- `缺项核对.csv`、`汇总.csv`、`依据.csv`、`园林概算报告.md`。

## 植物名称参考库（v0.4.13）

内置 `rules/plant_library_*.json` 全部默认加载（常用园林植物 349 名、西北温带荒漠区 112 名/131 条别名、CAD 图块素材 311 名、分区苗木选型 8 气候区 1022 名）；项目库用 `--plant-library 文件.{json,csv,xlsx}`；章节→大类顺序：地被→灌木→乔木→其他；参考库**只补原词库缺口**，不改变既有主线路结果，**不含也不读规格/标号/单价**。命中写入 `参考库命中`/`分类依据` 列。完整条目与结构见 `references/plant-library.md`。

## 置信分层

| 层 | 含义 | 处理 |
| --- | --- | --- |
| P0 | 直接证据 0.86–0.95：块名/坐标直中、苗木表文字直读、干净闭环 | 计入主线；苗木表只作设计基线 |
| P1 | 几何模式/无坐标计数 0.6–0.85 | 计入主线并标注 |
| P2 | 名称/文字推断 0.5–0.6 | 只进候选，不进主线 |
| P3 | 需人工核对：苗木表冲突、无法成环、缺图层、块内铺装、强算候选 | 标 `需核对=是`，排除主线 |

## 证据坐标

汇总表记录比例与图纸单位判定来源（用户覆盖/DXF INSUNITS/图纸文字/规则配置/默认）；每条统计/面积行保留 `文件 | 图层 | 块名/图例名 | 坐标(sample_coords/bbox/center) | 计算式 | 需核对原因`，便于按图复核。P2 图例文字也保留出现位置样例；无坐标块计数标 `无坐标；块计数=N`。

## 回归记录

真图回归结论与已知边界见 `docs/history.md`；置信分层和证据坐标规则仍以本文件为准。

## 依赖与入口策略（contract-only）

- 强依赖 `cad-file-reader >= 0.41.0` 与 `lis-skill-bus >= 0.1.11`，Python >= 3.10；先跑 `python3 scripts/yuanlin_qty.py --check-deps`，缺 reader 退出 `20`、缺 bus 退出 `21`，并打印安装命令。
- 本技能不 import `ezdxf`、不自行解 DXF；图纸入口只认 `--contract`，DWG/DXF/DWT 一律退出 `23`，块内铺装由 reader 的 `cad_landscape_geometry.sh` 产出契约。
- 手工契约必须显式 `--allow-manual`，结果强制 `final_quantity=false`、`formal_ledger_eligible=false`。
- 只有 landscape 输出、无几何详情：苗木统计可用，铺装面积降级为 review。
- 只有几何详情、无 landscape 输出：铺装面积可用，苗木分类退回块名/文字推断并标注。
- 块内铺装解析已完全迁到 reader 的 `cad_landscape_geometry.sh`；本技能不再持有 DXF 解析器，也不提供回退开关。
- 无 `openpyxl`：仍输出 CSV/Markdown，台账 xlsx 跳过。

## lis-skill-bus 联动

- 算量链必须安装并先查 bus；命中 `cad-contract/v1` 后直接复用，不重复解图。
- 园林核心 section 为 `plant_schedule_links` / `paving_closed_areas`；已有契约输入时只读消费，禁止本技能自行解图。
- 安装、路径优先级和 Windows 用法见 `docs/bus-integration.md`。

## QTO 联动

可选目录级登记规则见 `docs/integration.md`；只登记输入、输出与缺口，不替代本技能算法和复核。

## 运行时

`scripts/*.sh` 自动解析 Python、cad-file-reader 和依赖路径。排障与手工安装见 `docs/runtime.md`。

