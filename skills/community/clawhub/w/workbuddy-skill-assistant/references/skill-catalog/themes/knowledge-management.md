---
catalog_version: 0.1.0-draft
theme: knowledge-management
title: 知识管理 · 主题积木（≤10 个精华 skill）
last_synced: 2026-08-27
note: >
  笔记 / 知识图谱 / 信息收集 / 归档主题积木。评分二维：usability=实际好用 / composable=可组合 workflow。
  注：ima-skills 已入通用核心，本主题不重复。
---

# 知识管理 · 主题积木

> 使用指引：信息收集 → 笔记沉淀 → 知识图谱 → 人脉归档的个人知识资产闭环。

- name: Obsidian 笔记
  slug: skill_2053082563940843521
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 通过 mcp-obsidian 连接器读写 Obsidian 仓库（纯 Markdown 笔记）
  install_cmd: "skillhub install obsidian --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [ontology, Work_work_diary]

- name: 本体知识图谱
  slug: ontology
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 类型化知识图谱，结构化 Agent 记忆与可组合 skill（Person/Project/Task/Event/Document）
  install_cmd: "skillhub install ontology --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [skill_2053082563940843521, Work_work_diary]

- name: 知识卡片生成
  slug: card-generator
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 从论文/文章/网页/对话生成积木哲学知识信息卡 Markdown
  install_cmd: "skillhub install card-generator --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 3
  workflow_set: [ontology]

- name: 深度研究检索
  slug: "@org-gv4zgi7j/deep-research"
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 资料任务深度检索：选检索方式、收窄路径、盘点归纳、跨文档对比、补齐证据
  install_cmd: "skillhub install deep-research --namespace @org-gv4zgi7j --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [ima-skills]

- name: 信息收集情报员
  slug: info-collector
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 按配置的信息源/关键词收集信息，去重校验后整理成日报/周报
  install_cmd: "skillhub install info-collector --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 3
  workflow_set: [agent-mail]

- name: 工作日记（Obsidian）
  slug: Work_work_diary
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 每日工作记录/决策/研究笔记结构化归档至 Obsidian
  install_cmd: "skillhub install Work_work_diary --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [skill_2053082563940843521, ontology]

- name: 联系人归档（Obsidian）
  slug: Work_contact_manager
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 名片/微信/CSV 导入，生成带交叉链接的结构化联系人笔记
  install_cmd: "skillhub install Work_contact_manager --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [wecom-unified, tencent-docs]

> 待补充：双链笔记增强、RSS 聚合、网页剪藏等（社区有则补入）。
