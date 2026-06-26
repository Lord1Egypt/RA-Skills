---
name: sansheng-liubu-skill-map
description: 将三省六部组织架构映射为可落地的多 Agent 技能协作配置。用于按中书省、门下省、尚书省与六部标签整理技能分工、职责边界、标准流程、GitHub 对象映射与数据分析分层，适合构建面向现代工程团队的三省六部协作体系。
---

# 三省六部技能映射

本 skill 用于把“三省六部 × 技能库”整理为可落地的协作框架，适用于：
- 设计三省六部多 Agent 架构
- 为部门分配技能与职责边界
- 将技能映射到 GitHub、数据分析、测试、审核、文档等对象
- 统一规划、审核、调度、执行、复盘的标准链路

## 使用方式

当用户要求以下任一事项时，使用本 skill：
- 整理三省六部技能配置
- 设计三省六部与技能库的匹配关系
- 按中书省/门下省/尚书省/六部标签规划多 Agent 分工
- 为古典官制风格的多 Agent 系统建立工程化协作框架
- 输出三省六部的职责矩阵、流程图、技能映射表、配置文件

## 核心规则

1. 三省负责治理，六部负责执行。
2. 同一技能可以被多个部门使用，但必须区分主责、审核、协同。
3. GitHub 相关能力必须映射到明确对象，如 Issue、PR、Milestone、Project、Docs、Release。
4. 数据分析相关能力必须区分为战略分析、经营分析、执行分析。
5. 输出结果优先沉淀为结构化配置文件，而非只给口头说明。

## 三省匹配

### 中书省
- 定位：创意生成 → 方案撰写 → 目标制定
- 典型技能：`brainstorming`、`writing-plans`、`docx`、`pptx`、`pdf`
- 输出：战略摘要、方案文档、目标定义、Epic/Issue 草案

### 门下省
- 定位：方案审核 → 风险校验 → 质量把关
- 典型技能：`verification-before-completion`、`requesting-code-review`、`pdf`、`docx`
- 输出：审核意见、风险结论、评审报告

### 尚书省
- 定位：任务分发 → 多 Agent 协同 → 进度监控
- 典型技能：`executing-plans`、`dispatching-parallel-agents`、`subagent-driven-development`、`mcp-builder`
- 输出：任务拆解、调度计划、执行看板、阶段汇报

## 六部匹配

### 吏部（人事 / 组织管理）
- 典型技能：`subagent-driven-development`、`dispatching-parallel-agents`
- 职能：子 Agent 角色分配、权限管理、团队协作调度

### 户部（财务 / 数据管理）
- 典型技能：`xlsx`、`data-analysis`、`pdf`
- 职能：成本核算、数据统计、报表生成与可视化

### 礼部（品牌 / 沟通 / 文化）
- 典型技能：`brainstorming`、`writing-plans`、`docx`、`pptx`、`pdf`、`canvas-design`、`algorithmic-art`
- 职能：品牌宣传、活动策划、文案输出、视觉设计

### 兵部（项目攻坚 / 应急）
- 典型技能：`systematic-debugging`、`webapp-testing`、`executing-plans`
- 职能：线上问题处理、技术攻坚、应急响应

### 刑部（合规 / 风控 / 审核）
- 典型技能：`verification-before-completion`、`requesting-code-review`、`xlsx`、`pdf`
- 职能：合规检查、代码审核、风险预警、违规处理

### 工部（技术落地 / 开发）
- 典型技能：`test-driven-development`、`systematic-debugging`、`webapp-testing`、`frontend-design`、`canvas-design`、`algorithmic-art`、`web-artifacts-builder`、`mcp-builder`、`subagent-driven-development`、`github-integration`
- 职能：前端设计、代码开发、测试部署、工程交付

## 标准流程

1. 中书省：`brainstorming` → `writing-plans` → 导出 `docx/pptx/pdf`
2. 门下省：`verification-before-completion` → `requesting-code-review` → 输出审核报告
3. 尚书省：`dispatching-parallel-agents` → `mcp-builder` → 分发任务至六部
4. 六部执行：
   - 工部：`github-integration` → `test-driven-development` → `systematic-debugging`
   - 户部：`data-analysis` → `xlsx` → `pdf`
   - 礼部：`canvas-design` → `pptx`
   - 兵部 / 刑部：全程监控质量与合规
5. 收尾：`verification-before-completion` 最终校验 → 复盘 → GitHub 归档

## 需要时再读

如需结构化配置，读取：
- `references/sansheng_liubu_skill_map.yaml`：完整 YAML 映射
- `references/publishing_notes.md`：发布与维护说明
