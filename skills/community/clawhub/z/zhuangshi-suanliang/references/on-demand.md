# zhuangshi-suanliang 详细说明（由 SKILL.md 原样外移）

> 2026-11-10 瘦身：只搬未删。SKILL.md 保留硬规则、入口闸门、边界与口径摘要；命中下列主题时按需读取本文对应小节。

## 版本演进

0.7.0 测量候选接入记录见 `docs/history.md`；概算、物资计划、扣减、损耗和六表台账仍由本技能计算。

## 适用

- 快速概算：按办公室、会议室、卫生间、走廊、楼梯间、屋面、外墙等房间类型展开。
- 明细算量：按楼层、区域、房间、部位、做法编号和节点逐行输入。
- 物资计划：输出主材/辅材分类、净量、损耗量、需求量和供货方式参考。
- 防水：计算上翻、附加层、卷材搭接，并按内置规范参考校验。

## 前置

- 表格输入（主路径）：只需 Python（CSV/TSV 纯标准库；读 `.xlsx` 需 `openpyxl`），不需要 `cad-file-reader`/`lis-skill-bus`。
- 图纸链路（可选）：`--contract` 契约必须由已安装的 `cad-file-reader >= 0.41.0` 生成、经 `lis-skill-bus >= 0.1.11` 传入；缺依赖时停止并回显安装命令，`--check-deps` 返回 `20`/`21`。
- 只有 `scripts/cad_measure_to_input.py`（测量候选转输入表）需要 `cad-file-reader`；缺依赖时它停止，不自行解图。
- 不自行解析大 DWG，也不提供任何直读兜底；读 Word/Excel/PDF 用 `markitdown`。
- 项目做法表、节点详图、项目专属规则、企业定额、现行规范优先于内置默认值；项目专属做法必须绑定节点编号和节点详图，缺节点进待确认项，不用默认材料层凑数。
- 完整架构与安装/降级细节见 `references/base-contract.md`。

## 使用流程

1. **圈定范围**：确认楼层、区域、房间、部位和房间类型，不把全楼混算。
2. **读取依据**：交叉读取房间装修做法表、建筑总说明、建筑图、结构图、门窗表、节能/防水/防火说明和节点详图。  
   优先级：节点详图/大样图 > 项目专属节点规则 > 房间装修做法表 > 建筑总说明 > 建筑图/结构图 > 默认参考值。
3. **快速输入**：若只需初稿，填 `templates/快速概算输入表.csv`；脚本按房间模板展开为多条做法。
4. **明细输入**：正式核对时填 `templates/装饰算量输入表.csv`，逐行绑定尺寸和做法。
5. **计算**：概算取基面量；材料需求量乘损耗、搭接、附加层和单耗；块料向上取整。
6. **复核**：检查待确认项、重复行、防水参数、清单口径和单价来源。
7. **输出**：用六表 Excel 台账做商务和现场核对。

## 脚本用法

```bash
# 快速概算
python3 \
  scripts/decor_qty.py \
  --input templates/快速概算输入表.csv \
  --out-dir ./概算结果 \
  --project-rules templates/项目专属规则示例.json \
  --project "项目名" --allow-manual

# 明细算量
python3 \
  scripts/decor_qty.py \
  --input ./输入.csv \
  --out-dir ./明细结果 \
  --project-rules templates/项目专属规则示例.json \
  --project "项目名" --level "二层" --allow-manual
```

可用规则参数：

- `--room-templates rules/标准房间模板.json`
- `--quantity-rules rules/清单工程量规则.json`
- `--price-rules rules/概算综合单价.json`
- `--material-rules rules/物资分类规则.json`

## 输出

- `装饰概算物资计划台账.xlsx`：固定包含 `概算`、`物资计划`、`明细`、`汇总`、`缺项`、`依据`。
- `概算明细.csv`：清单编码、清单工程量、参考单价、概算合价、计算式和状态。
- `概算汇总.csv`：按清单项汇总工程量和合价。
- `物资计划.csv`：净量、损耗率、损耗量、需求量、完成状态需求量、分类和供货方式。
- `明细.csv`、`材料汇总.csv`：基面量、订货量、计算式和依据。
- `缺项核对.csv`、`依据.csv`、`装饰概算物资计划报告.md`。

## 输入校验

- 明细必填列：楼层、区域、房间、部位类型、做法编号、做法名称、做法类型、依据、间数。
- 快速输入按 `房间类型` 展开成明细；未知房间类型不静默跳过，进入待确认项。
- 数字列必须填数字，不带文字单位；不允许负数；间数必须大于0。
- 完全重复行标记为“重复”，不重复计入计算。
- 防水行要求附加层宽度、搭接宽度、涂膜厚度字段；卫生间/厨房还要求上翻高度。
- 项目专属做法必须填写节点编号、节点详图并匹配项目节点规则。

## 防水与规范复核

内置值是参考下限和校验提示，不替代条文原文；现行规范、设计文件、节点详图和项目规则优先。

- 卷材搭接参考下限 80mm；涂膜厚度参考下限 1.5mm；附加层宽度室内 0.25m、屋面/地下 0.5m；室内有水房间上翻 0.25m，淋浴区按设计另核（常见参考 1.8m）；屋面不少于 2 道。
- 卷材用搭接系数：`幅宽 /（幅宽 - 搭接宽度）`；附加层可填直接面积或按长度×宽度计算。
- 引用的国标/行标全清单（GB 50500、GB 50854、GB 55030、GB 50207/50208、JGJ 298 等 15 部）见 `references/waterproof-standards.md`。

## CAD 测量候选交接

先用 `cad-file-reader` 生成带比例、单位、计算式和证据的测量候选：

```bash
# 在识图底座 cad-file-reader 技能目录执行：
scripts/cad_measure.sh 描述几何/图纸详情.descriptive.json --out-dir 测量候选
```

再把候选转成装饰算量输入表草稿：

```bash
scripts/cad_measure_to_input.py --measurements 测量候选/cad-measurement-candidates.json   --out CAD导入_待核对.csv --floor 二层
```

导入行会保留房间/部位候选、面积或长度候选和证据，但**做法编号留空、需核对固定为“是”**；做法映射、洞口扣减、侧壁、损耗、材料台账和正式清单量仍由本技能计算。

## 依赖与入口策略（contract-only）

- 强依赖 `cad-file-reader >= 0.41.0` 与 `lis-skill-bus >= 0.1.11`，Python >= 3.10；本技能不自动下载、不自带解图器。
- 先跑 `python3 scripts/decor_qty.py --check-deps`：缺依赖 exit 20/21（缺 reader 20、缺 bus 21），并打印可复制的安装命令。
- 正式量走 `--contract`（cad-contract/v1 契约，仅作溯源证据，工程量仍来自 `--input` 表）；手工表必须显式 `--allow-manual`，结果强制 `final_quantity=false`。
- 已删除 `SKILL_NO_BASE=1` 静默降级；`scripts/ensure_base.sh` 下载失败直接报错退出。

## lis-skill-bus 联动

- 算量链必须安装并先查 bus；命中 `cad-contract/v1` 后直接复用，不重复解图。
- 装饰核心 section 为 `rooms` / `room_schedules`；已有契约输入时只读消费，禁止本技能自行解图。
- 安装、路径优先级和 Windows 用法见 `docs/bus-integration.md`。

## QTO 联动

可选目录级登记规则见 `docs/integration.md`；只登记输入、输出与缺口，不替代本技能算法和复核。

