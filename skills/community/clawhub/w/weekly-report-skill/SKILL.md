---
name: weekly-report-generator
description: Generate polished Chinese R&D weekly reports from recent work logs, chat history, commit notes, or development notes. Use when the user asks to 生成、整理、润色、汇总本周、上周、最近7天或某日期范围的周报/研发周报, especially for tender-agent, RAG, prompt, skill, document parsing, table parsing, scoring-standard, content-generation, export-center, and Agent work. Automatically filters deployment, environment, operations, installation, and troubleshooting details.
---

# Weekly Report Generator

Use this skill to turn noisy engineering records into a concise Chinese R&D weekly report that can be sent to a manager.

## Inputs

Accept any of these inputs:

- A date range, such as `2026.06.15-2026.06.19`, `本周`, `上周`, or `最近7天`.
- Work logs, chat history, meeting notes, commit summaries, issue notes, or loose bullet points.
- Mixed useful work and operational noise.

When the user gives a relative date range, resolve it against the current date and timezone available in the conversation. When no date range is provided, use the best explicit date range in the input; if none exists, label the report as `本周`.

## Workflow

1. Extract candidate work items from the input.
2. Keep only R&D, product, feature, architecture, data, model-experience, Agent, RAG, Prompt, Skill, parsing, generation, scoring, review, export, and business workflow improvements.
3. Remove operational, deployment, environment, installation, startup, networking, hardware, and troubleshooting details.
4. Merge repeated or related items into one higher-level achievement.
5. Preserve dates only when the input provides them. Do not invent weekday placement for undated work.
6. Rewrite retained items into result-oriented Chinese bullets.
7. Add highlights and next-week plans derived from the retained themes.
8. Before returning, check that no forbidden operational details remain.

## Keep

Prefer retaining items about:

- 业务功能开发
- 投标智能体开发
- 模型体验优化
- Agent 能力建设
- RAG 优化
- Prompt 优化
- Skill 开发
- 页面功能开发
- 文档解析优化
- 表格解析优化
- 正文生成优化
- 评分标准优化
- 审查整改优化
- 导出中心功能开发
- 数据结构优化
- 系统架构优化
- 检索召回、知识库、资质分析、内容一致性、结构化抽取等业务研发工作

## Filter

Do not include these details in the report, even if they appear in the source:

- Docker、容器、镜像
- Linux 环境、系统安装、第三方软件安装
- 网络问题、端口问题、服务启动
- 模型下载、CPU/GPU 部署
- 运维排障、环境配置、启动异常
- 调试过程、排查过程、失败过程、临时绕行方案

If an item contains both business work and deployment noise, keep the business outcome and drop the operational part.

## Merge Rules

Merge related work under one achievement:

- `正文生成优化`、`正文重写优化`、`章节续写优化` -> `完成正文生成链路优化，增强上下文关联能力与内容一致性`
- `评分标准识别`、`评分项解析`、`评分表结构化` -> `完成评分标准结构优化，统一评分项数据结构与字段定义`
- `跨页表格解析`、`表头识别`、`单元格还原` -> `完成表格解析能力优化，提升复杂表格结构还原效果`
- `知识召回`、`RAG 检索`、`向量检索体验` -> `完成知识召回链路优化，提升检索准确性与问答支撑能力`

## Output Rules

Use Markdown only.

For dated input, output weekday sections only for days that contain retained business/R&D work:

```markdown
# 工作周报（YYYY.MM.DD-YYYY.MM.DD）

## 周一（MM.DD）

1. 完成XXX优化，提升XXX能力 —— 100%
2. 完成XXX开发，完善XXX流程 —— 100%

## 周二（MM.DD）

1. 完成XXX优化，增强XXX效果 —— 100%

---

## 本周工作亮点

1. XXX能力提升
2. XXX链路完善
3. XXX体验优化

---

## 下周计划

1. 持续优化XXX能力
2. 完善XXX流程
3. 推进XXX功能建设
```

For undated input, do not fabricate weekdays. Use:

```markdown
# 工作周报（本周）

## 本周完成

1. 完成XXX优化，提升XXX能力 —— 100%
2. 完成XXX开发，完善XXX流程 —— 100%

---

## 本周工作亮点

1. XXX能力提升
2. XXX链路完善
3. XXX体验优化

---

## 下周计划

1. 持续优化XXX能力
2. 完善XXX流程
3. 推进XXX功能建设
```

If no valid reportable R&D work remains after filtering, say:

```markdown
# 工作周报（<日期范围>）

本次输入中未识别到可写入研发周报的业务开发或研发优化事项。
```

## Style

- Use concise, polished Chinese suitable for a manager-facing R&D weekly report.
- Prefer `完成XXX优化/开发/建设/完善` sentence patterns.
- Keep each work bullet around 20-40 Chinese characters when possible.
- Use `—— 100%` only for clearly completed items. For ongoing work, use `推进XXX建设` and omit the completion percentage unless the user provides one.
- Avoid exposing raw logs, chat wording, personal names, debugging notes, tool names, and operational implementation details.
- Do not invent dates, metrics, module names, stakeholders, or completion status.
- Keep daily sections to the most important 3-5 retained items when the input is long.
- Keep highlights and plans to 2-4 items each unless the user asks for more.
