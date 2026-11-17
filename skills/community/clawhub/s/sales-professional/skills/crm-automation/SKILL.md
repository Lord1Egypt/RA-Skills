---
name: crm-automation
description: CRM 自动化：数据质量治理、工作流设计、报表与仪表板、管道管理与销售效率提升
source:
  type: derived
  repo: skills-repo/sales-professional
  path: skills/crm-automation/SKILL.md
  url: https://skills.sh/claude-office-skills/skills/crm-automation
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 销售
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - crm
  - automation
  - sales-ops
  - pipeline
  - data-quality
---

# CRM Automation — CRM 自动化

> 销售不是靠记忆力。CRM 自动化帮你把重复操作变成自动流程，让销售把时间花在跟人打交道上，而不是填表。

## 能力

- **数据质量治理**：重复记录合并、字段标准化、缺失数据检测和修复规则
- **工作流自动化**：Lead 分配、阶段推进触发、提醒和通知、审批流
- **报表与仪表板**：销售管道报表、预测分析、团队绩效仪表板
- **管道管理**：交易阶段跟踪、停滞机会检测、流失风险预警
- **集成策略**：CRM ↔ 邮件/日历/LinkedIn/电话系统的双向同步

## 使用方式

在 Claude Code 中使用 `/crm-automation` 调用。

```
/crm-automation 帮我设计一个 Lead-to-Opportunity 的自动流转规则
/crm-automation 我的 CRM 里有 5000 条重复数据，怎么清理？
/crm-automation 搭建一个销售管道仪表板
```

## 工作流

1. **审计现状** — 检查当前 CRM 配置、数据质量、已有自动化
2. **流程设计** — 画出销售流程的每个阶段和触发条件
3. **自动化实现** — 工作流规则、字段更新、通知触发
4. **报表配置** — 定义关键指标（转化率、周期长度、胜率）
5. **验证与迭代** — 跑一周数据 → 检查自动化是否按预期执行

## 关键检查清单

```
[ ] 所有必填字段都有默认值或自动化填充逻辑
[ ] Lead 来源字段统一（不是 "LinkedIn" + "linkedin" + "linked in"）
[ ] 每个管道阶段有明确的进入/退出标准
[ ] 超过 30 天未活动的 Opportunity 自动标记
[ ] 重复检测规则基于 email + company domain 组合
```

## 适用场景

- 销售团队从 2 人扩展到 10+ 人时需要流程化
- CRM 数据混乱影响报表准确性
- 从 Excel 迁移到 HubSpot/Salesforce/Pipedrive
- 销售运营（Sales Ops）搭建自动化基础

## 限制

- 覆盖 HubSpot、Salesforce、Pipedrive 三大主流 CRM
- 不涉及 CRM 二次开发（自定义对象、Apex 代码等）
- 不涵盖 Marketing Automation（那是营销自动化系统的事）
- 报表假设 CRM 已有足够数据量（至少一个完整销售周期）

## 相关参考（Playbook）

- 跟进节奏自动化、CRM 打点与停滞商机处理 → [references/outreach-playbook.md](../../references/outreach-playbook.md)（L2 方法论：跟进节奏与发送前清单）
- 管道阶段定义、停滞商机自动跟进触发 → [references/sales-pipeline.md](../../references/sales-pipeline.md)（L2 方法论：管道阶段与 GTM 决策）