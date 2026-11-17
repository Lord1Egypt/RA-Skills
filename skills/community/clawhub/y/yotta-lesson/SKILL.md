---
name: yotta-lesson
slug: yotta-lesson
version: 0.1.4
displayName: 教案设计·元案
summary: 本地、确定性的教案骨架与覆盖校验：课标映射包 → 教案骨架（学习目标带来源、环节时间精确到分钟），并对已有教案做缺口检查（知识点 / 环节 / 来源 / 时间）；零依赖，不联网、不内置教材原文。
description: '教案设计（元案）—— 把课标映射包变成可复算的教案骨架：学习目标逐条带课标来源、重难点与易错点、五环节 + 分钟级时间分配（合计恒等于课时 × 每课时分钟）、板书与评价清单；check 子命令对已有教案做确定性缺口检查（未覆盖知识点 / 缺必填环节 / 缺来源 / 未标时间 / 合计时间不一致），支持 --gate findings=n 接入 CI；零依赖本地运行，不联网、不调用模型、不内置教材与题目原文。'
tags: [教案, 学案, 教学设计, 课标对标, 备课, 环节校验, 教学教研, education, lesson plan, 本地化]
category: education
license: MIT
homepage: https://github.com/YottaMeta/yotta-lesson
---
# 元案（yotta-lesson）

本地、确定性的教案骨架与覆盖校验技能。元案把「课标映射包」变成可复算的教案骨架，
并把「这节课的知识点、环节、来源、时间齐了吗」变成一份确定性缺口清单。

可信契约：

- 教案骨架来自映射包与结构配置，同一输入得到同一结果（仅生成时间不同）；
- 时间分配精确到分钟且合计可校验（课时 × 每课时分钟）；
- 每条学习目标都带课标来源；缺口清单给出具体原因与关键词；
- 核心路径不联网、不调用模型，教案与映射包只在本机流转。

## 何时使用

- 按学校自备的课标 / 单元映射，快速起一份结构完整的教案骨架；
- 用 `check` 核对已有教案：知识点是否都覆盖、必填环节是否齐全、是否标了来源与时间；
- 教研组统一教案结构（同一映射包 + 同一结构配置 = 同一套骨架口径）；
- 把教案结构检查接入批处理或 CI（`--gate findings=<n>`）。

**Do NOT trigger**：

- 不生成题目与学案题目内容（组卷属元题，题面由学校题库提供），不生成学生评语；
- 不替代教师的教学设计判断：骨架与清单是备课辅助，最终设计由教师定稿；
- 不联网、不调用模型、不上传教案与校本映射；
- 不内置教材与课标原文，只记录结构性元数据；引用请以官方文本为准。

## 快速使用

```bash
# 生成映射包与结构配置模板
python3 scripts/yotta_lesson.py template --output-dir ./lesson-template

# 生成教案骨架（Markdown）
python3 scripts/yotta_lesson.py plan --map lesson-map.json --lesson L1

# 两课时版本 + JSON 输出
python3 scripts/yotta_lesson.py plan --map lesson-map.json --lesson L1 --periods 2 --format json

# 检查已有教案的覆盖缺口，并在缺口 ≥ 1 时让 CI 失败
python3 scripts/yotta_lesson.py check --plan plan.md --map lesson-map.json --lesson L1 --gate findings=1

# 映射包操作
python3 scripts/yotta_lesson.py map validate --map lesson-map.json
python3 scripts/yotta_lesson.py map list --map lesson-map.json
```

退出码：`0` 正常 ｜ `1` 触发 `--gate` ｜ `2` 输入错误 ｜ `3` 映射或配置错误 ｜ `4` 运行时错误。

## 输入与输出

- **课标映射包**：JSON，逐课题声明 `id` / `title` / `periods` / `knowledge` / `key_points` / `difficulties` / `misconceptions` / `standard`（课标来源，必填）；
- **结构配置**（可选）：`minutes_per_period`、`stages`（环节与比例）、`required_stages`、`check_keywords`；
- **输出**：教案骨架 Markdown + JSON（`schema_version 1.0`，含 `objectives` / `stages` / `checklist` / `findings` / `sources` / `disclaimer`）；
- **缺口检查**：`knowledge_missing` / `stage_missing` / `source_missing` / `time_missing` / `minutes_mismatch`。

字段规范见 `references/map-format.md`；报告契约见 `references/plan-format.md`。

## 版权与边界

- 映射包只存结构性元数据（课题 / 知识点 / 课标条目标识），不存教材正文与题目原文；
- 课标引用以官方文本为准，本技能不做课标解读；
- 输出为备课辅助，不用于教学评价结论。

详见 `references/copyright.md`。

## 家族协同

- **元镜 yotta-mirror**：用学情数据反哺下一轮备课的薄弱点；
- **元题 yotta-item**：按双向细目表从学校自备题库组卷、并做试卷结构校验（不生成题面）；
- **元呈 yotta-present**：把教案骨架渲染成统一格式；
- **元真 yotta-humanize**：教师-facing 叙述文字去 AI 味；
- **元忆 yotta-memory**：按需保存映射包版本与教案骨架摘要。

## 渐进披露

- 映射包与结构配置：`references/map-format.md`
- 骨架 / 检查报告契约与退出码：`references/plan-format.md`
- 版权与使用边界：`references/copyright.md`

按需读取，不必每次全读。
