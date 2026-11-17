---
name: yotta-item
slug: yotta-item
version: 0.1.3
displayName: 命题组卷·元题
summary: 本地、确定性的组卷与试卷校验：双向细目表（题型 / 考点 / 难度配额 / 分值 / 限时）+ 题库 → 可复算选题；对已有试卷做缺口检查（总分 / 分节 / 难度分布 / 覆盖 / 限时）；零依赖，不联网、不生成题面。
description: '命题组卷（元题）—— 按双向细目表从本地题库确定性选题组卷：先保证必考考点覆盖，再按难度配额补足，固定 seed 可复算（题库不足时报缺口，不用编造的题顶替）；check 子命令对已有试卷做确定性缺口检查（未知题 / 重复题 / 总分偏差 / 分节题量与分值偏差 / 难度分布漂移 / 考点缺失 / 超出限时），支持 --gate findings=n 接入 CI；零依赖本地运行，不联网、不调用模型、不生成或改写题面、不内置题目与教材原文。'
tags: [组卷, 命题, 试卷, 双向细目表, 题库, 考点覆盖, 难度配比, education, exam paper, 本地化]
category: education
license: MIT
homepage: https://github.com/YottaMeta/yotta-item
---
# 元题（yotta-item）

本地、确定性的组卷与试卷校验技能。元题把「双向细目表 + 题库」变成一份可复算的试卷，
并把「这份卷子达标吗」变成一份带证据的缺口清单。

可信契约：

- 组卷结果来自题库选题，**不生成题面**；同一题库、蓝图与 seed 得到同一份试卷（仅生成时间不同）；
- 每个结论都带证据：题目 id、期望值、实际值（覆盖 / 难度 / 分节 / 时间逐项可核）；
- 题库不足或约束无法满足时，给出缺口清单而不是编造题目；
- 核心路径不联网、不调用模型，题库、蓝图与试卷只在本机流转。

## 何时使用

- 按学校自备题库与双向细目表，快速组一份满足考点覆盖与难度配比的试卷；
- 用 `check` 核对已有试卷：总分对不对、分节题量与配比对不对、必考考点是否都在、时间是否超；
- 教研组统一命题口径（同一题库 + 同一蓝图 = 同一套选题约束）；
- 把组卷与试卷校验接入批处理或 CI（`--gate findings=<n>`）。

**Do NOT trigger**：

- 不生成、不补写题目内容与答案（AI 编题是幻觉高发区；题目内容由题库提供）；
- 不预测难度实测值与区分度（那依赖考后统计，属元镜的学情分析范围）；
- 不做学生排名、评语、升学预测；
- 不联网、不调用模型、不上传题库与试卷；
- 不内置教材与真题原文：示例与模板全部是合成占位数据；
- 不替代命题组与教研组的专业判断：输出是选题结果与缺口清单，试卷定稿由人负责。

## 快速使用

```bash
# 生成题库 / 蓝图 / 试卷模板
python3 scripts/yotta_item.py template --output-dir ./item-template

# 输入校验（CI 前置）
python3 scripts/yotta_item.py bank validate --bank bank.json
python3 scripts/yotta_item.py blueprint validate --blueprint blueprint.json --bank bank.json

# 按蓝图组卷（固定 seed，可复算）；无法满足约束时退出码 1
python3 scripts/yotta_item.py assemble --bank bank.json --blueprint blueprint.json --seed 0

# 组卷结果写入 JSON，可直接喂给 check（兼容组卷输出形态）
python3 scripts/yotta_item.py assemble --bank bank.json --blueprint blueprint.json \
  --format json --out paper.json

# 校验试卷；有缺口即让 CI 失败
python3 scripts/yotta_item.py check --bank bank.json --paper paper.json \
  --blueprint blueprint.json --gate findings=1
```

退出码：`0` 正常 ｜ `1` 触发 `--gate` 或组卷无法满足约束 ｜ `2` 输入错误 ｜
`3` 题库 / 蓝图 / 试卷校验错误 ｜ `4` 运行时错误。

## 输入与输出

- **题库**：JSON，逐题声明 `id` / `type` / `points` / `difficulty` / `knowledge`，
  可选 `minutes` / `source`；`difficulty_levels` 默认 `easy / medium / hard`，可按校情定义 2-5 档；
- **双向细目表（蓝图）**：JSON，`total_points` 必须等于 Σ（题量 × 每题分），
  每节难度配额之和必须等于该节题量；`coverage` 声明全卷必考考点；
- **试卷**：JSON，只记题目 id 引用（`items[].id`，可选 `section`），不复制题目内容；
- **输出**：Markdown（人读组卷报告 / 缺口报告）+ JSON（`schema_version 1.0`，含 `sections` /
  `paper` / `totals` / `coverage` / `difficulty_summary` / `time_budget` / `findings` / `disclaimer`）。

字段与错误表：[references/bank-format.md](references/bank-format.md)、
[references/blueprint-format.md](references/blueprint-format.md)。

缺口类别与报告契约：[references/report-format.md](references/report-format.md)。

隐私与版权边界：[references/privacy.md](references/privacy.md)。

## 配合使用

- **元镜 yotta-mirror**：考后用学情分析拿实测数据；元题只按题库标注做分布控制，不预测实测值；
- **元案 yotta-lesson**：教案骨架里的例题与练习位需要题目时，用元题按考点配额选题；
- **元呈 yotta-present**：把组卷报告渲染成统一格式；
- **元忆 yotta-memory**：按需保存题库版本与组卷摘要（默认只在本机）。
