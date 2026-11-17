---
name: lead-generation
description: 潜客挖掘：数据驱动的 Lead 发现、识别信号、评分模型、列表建设与渠道策略
source:
  type: derived
  repo: skills-repo/sales-professional
  path: skills/lead-generation/SKILL.md
  url: https://skills.sh/apify/agent-skills/apify-lead-generation
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
  - lead-generation
  - prospecting
  - data-enrichment
  - sales-intelligence
  - list-building
---

# Lead Generation — 潜客挖掘

> 销售的第一件事不是打电话，是找到对的人。Lead Generation 帮你系统化地从公开数据中挖掘高质量潜客，告别凭运气翻 LinkedIn 的日子。

## 能力

- **信号识别**：识别购买信号（融资、招聘岗位、技术栈变更、新闻事件）
- **列表建设**：从 LinkedIn/网页/数据库批量提取目标公司和人，构建结构化潜客列表
- **数据增强**：补全 email、公司规模、行业、技术栈等缺失字段
- **评分模型**：Lead Scoring（BANT/MEDDIC/自定义）自动排序优先级
- **多源整合**：LinkedIn Sales Navigator、Crunchbase、BuiltWith、SimilarWeb 等数据源
- **去重与清洗**：跨源合并时自动去重、格式标准化

## 使用方式

在 Claude Code 中使用 `/lead-generation` 调用。

```
/lead-generation 帮我找 50 个使用 React 的电商公司 CTO 联系方式
/lead-generation 设计一个 Lead Scoring 模型
/lead-generation 验证这份 2000 条潜客列表的数据完整性
```

## 工作流

1. **定义 ICP** — 行业 / 规模 / 技术栈 / 角色 / 地理位置
2. **数据抓取** — 从选定数据源批量采集
3. **数据增强** — 补全联系方式、公司信息
4. **评分排序** — Lead Scoring → 优先级列表
5. **列表输出** — 结构化的 CSV / CRM 导入格式

## ICP 定义模板

```
行业：SaaS / Fintech / Healthcare
规模：50-500 人，Series A-C
角色：CTO / VP Engineering / Head of Platform
技术栈：使用 Kubernetes / AWS / React
信号：最近 3 个月有招聘 DevOps 岗位
地理位置：北美 / 欧洲
```

## 适用场景

- 销售团队需要批量获取目标客户列表
- 独立开发者找早期客户
- A/B 测试不同 ICP 定义的响应率
- CRM 中 Lead 数量不足，需要拓展顶部漏斗

## 限制

- 覆盖 B2B 场景，不涉及 B2C 潜客获取（社交媒体广告等）
- 数据采集合规性：遵守 robots.txt 和各地数据保护法规
- 不涉及付费广告获客（Google Ads/LinkedIn Ads）
- 联系方式验证需要第三方工具配合（如 NeverBounce/ZeroBounce）

## 相关参考（Playbook）

- 精准 ICP 与名单挖掘 → [references/outreach-playbook.md](../../references/outreach-playbook.md)（L2 方法论：精准 ICP 是回复率第一杠杆）
- 线索来源可归因、ICP 挖掘 → [references/sales-pipeline.md](../../references/sales-pipeline.md)（L2 方法论：管道健康检查与出海要点）
