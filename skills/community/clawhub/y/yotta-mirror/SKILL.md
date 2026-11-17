---
name: yotta-mirror
slug: yotta-mirror
version: 0.1.3
displayName: 学情分析·元镜
summary: 本地、确定性的学情分析：成绩 / 答题表 → 知识点掌握率、学生分层与临界生、薄弱点诊断；每条结论带题号 / 样本量 / 掌握率 / 阈值，学生数据不出本机，零依赖。
description: '学情分析（元镜）—— 把成绩 / 答题表与题目-知识点映射，变成可复算、可追溯的诊断报告：数据质量闸门、逐题统计、按分值加权的知识点掌握率、A/B/C 分层与临界生识别、薄弱点诊断（低样本自动降级为人工复核），支持阈值配置、学生标识匿名化与 CI 闸门；零依赖本地运行，不联网、不调用模型，不用于学生评价或排名。'
tags: [学情分析, 成绩分析, 作业诊断, 知识点掌握, 班级报告, 分层教学, 临界生, 数据本地化, 证据链, education, learning analytics]
category: education
license: MIT
homepage: https://github.com/YottaMeta/yotta-mirror
---
# 元镜（yotta-mirror）

本地、确定性的学情分析技能。元镜把成绩 / 答题表与题目-知识点映射变成一份**可复算、可追溯**的
诊断报告：既给结论，也给结论背后的题号、样本量、比例与阈值。

可信契约：

- 每条薄弱点结论都带证据（涉及题号、样本量、掌握率、所用阈值）；
- 同一份数据、同一份配置得到同一份结论（仅生成时间不同）；
- 样本量低于阈值、分界线附近的判断一律降级为人工复核项；
- 核心路径不联网、不调用模型、不写外部路径；学生数据只在本机流转。

## 何时使用

- 分析班级测验 / 作业结果，找薄弱知识点与临界生；
- 把「统计 + 写分析报告」这段耗时的杂活交给自动化流程；
- 需要一份下发给备课组 / 年级组的学情报告，且要求结论可核查；
- 把学情分析接入 CI 或批处理（`--gate weak=<n>` 提供退出码）。

**Do NOT trigger**：

- 不生成学生评语、排名榜、奖惩建议，不给学生贴能力或性格标签；
- 不预测升学结果，不做学业结论性判断；
- 不解析图片 / 扫描件试卷（不做 OCR），输入必须是结构化表格；
- 不上传、不联网、不同步学生数据；跨设备同步属另一条需显式开启的分支，本版不实现；
- 不替代教师判断：报告输出的是数据事实与待复核清单。

## 快速使用

Windows 使用 `python`，Linux / macOS 使用 `python3`。

```bash
# 生成录入模板（成绩表 + 题目映射 + 阈值配置）
python3 scripts/yotta_mirror.py template --output-dir ./mirror-template

# 分析一次测验，输出 Markdown 报告
python3 scripts/yotta_mirror.py analyze --input scores.csv --items item-map.json

# 输出 JSON（自动化 / 存档），并按薄弱点数量设闸门
python3 scripts/yotta_mirror.py analyze --input scores.csv --items item-map.json \
  --config thresholds.json --format json --out report.json --gate weak=3

# 从标准输入读取，学生标识匿名化后再分享
cat scores.csv | python3 scripts/yotta_mirror.py analyze --stdin --items item-map.json --anonymize

# 校验阈值配置
python3 scripts/yotta_mirror.py config validate --pack thresholds.json
```

退出码：`0` 正常 ｜ `1` 触发 `--gate` ｜ `2` 输入错误 ｜ `3` 配置或映射错误 ｜ `4` 运行时错误。

## 输入与输出

- **成绩 / 答题表**：CSV / TSV，首行表头，第一列 = 学生标识，其余列 = 题目；单元格 = 该题得分，留空 = 缺失；
- **题目映射**：JSON，声明每题 `id` / `max_score` / `knowledge`（一题可挂多个知识点）与可选 `difficulty`；
- **阈值配置**（可选）：`mastery.weak_below` / `mastery.solid_at_or_above` / `layers.*` / `min_respondents` / `critical_margin`；
- **报告**：Markdown（人读）+ JSON（稳定契约，`schema_version`），字段定义见 `references/report-format.md`。

字段规范与常见报错对照见 `references/data-format.md`。

## 分析模型

1. **数据闸门**：列与映射不一致、学生重复、非数值、得分越界 → 立即报错并指出行 / 列；
2. **逐题统计**：作答数、缺失数、平均分、得分率、满分人数、零分人数；
3. **知识点聚合**：按题目分值加权计算掌握率，输出题号清单与样本量；
4. **学生分层**：A / B / C 三档 + 分界线附近的临界生标记；
5. **薄弱点诊断**：掌握率低于阈值 → 生成诊断项（高 / 中严重度）；样本不足 → 人工复核项；
6. **报告**：结论 + 证据 + 复核清单 + 免责声明。

## 数据与隐私

- 学生数据默认只在本机读取、分析与落盘：核心路径零网络、零模型调用；
- `--anonymize` 用可复算代号（SHA-256 前 8 位）替换学生标识，便于对外分享；
- 对外分享前建议只带结论与证据，不带原始姓名；
- 报告固定免责声明：仅用于教学改进，不用于学生评价、排名或升学判断。

详见 `references/privacy.md`。

## 家族协同

- **元呈 yotta-present**：把学情报告渲染成统一格式（表格 / 结论卡）再交付；
- **元忆 yotta-memory**：按需保存报告摘要与阈值配置版本（学生明细自决是否入库）；
- **元规 yotta-compliance**：对涉及学生个人信息的材料做条款级合规审查；
- **元真 yotta-humanize**：需要发给家长 / 教师的叙述性文字去 AI 味；
- **元阁 yotta-skills**：作为编排层把「分析 → 呈现 → 记录」串成一条工作流。

## 渐进披露

- 字段与报错对照：`references/data-format.md`
- 报告与 JSON 契约、退出码、闸门：`references/report-format.md`
- 数据边界与匿名化：`references/privacy.md`

按需读取，不必每次全读。
