---
name: cold-email
description: 冷启动邮件：高打开率标题、个性化策略、序列编排、A/B 测试、回复率优化
source:
  type: derived
  repo: skills-repo/sales-professional
  path: skills/cold-email/SKILL.md
  url: https://skills.sh/coreyhaines31/marketingskills/cold-email
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
  - cold-email
  - outreach
  - prospecting
  - sales
  - email-marketing
---

# Cold Email — 冷启动邮件

> 87K+ 安装量的顶级冷邮件技能。不是群发垃圾邮件，而是基于研究、个性化和价值主张的精准外联。一封好邮件能打开一扇门。

## 能力

- **邮件撰写**：高打开率标题、钩子句、价值主张（不是自我介绍）、CTA 设计
- **个性化策略**：使用触发事件（融资/招聘/产品更新）定制邮件的具体方法
- **序列编排**：3-4 封跟进邮件的节奏、时机和内容变化（= 基线 4 次触达 / 扩展 5 次触达，首封不计入"跟进"）
- **A/B 测试**：测试标题/正文/CTA 的框架，统计显著性地判断胜出变体
- **回复率优化**：分析回复数据（不是打开/点击），迭代改进邮件
- **规模化工具**：邮件合并技巧、CRM 集成、自动化而不失个性

## 使用方式

在 Claude Code 中使用 `/cold-email` 调用。

```
/cold-email 帮我写一封给 SaaS 公司 CTO 的冷邮件
/cold-email 分析我这封邮件的回复率为什么低
/cold-email 帮我设计一个 5 次触达的跟进序列（首封 + 4 次跟进）
```

## 工作流

1. **目标研究** — LinkedIn/官网/新闻 收集触发事件和个人信息
2. **价值主张** — 用一句话说清「为什么对方应该回复」
3. **邮件草拟** — 标题（英文 ≤10 词 / 中文 ≤20 字，具体+利益点，长度以下方「标题公式」示例为准）+ 钩子（个性化）→ 价值 → 微 CTA；正文 ≤120 词
4. **序列编排** — 扩展序列 Day 0/3/7/14/21（5 次触达 = [references/outreach-playbook.md](../../references/outreach-playbook.md) §3 的基线 4 触达 + 第 21 天追加一次），首封一律 **Day 0** 起算，逐次切换角度
5. **测试迭代** — A/B 测试 → 分析 → 改进

## 标题公式

```
[触发事件] + [具体价值] → 例如（均 ≤10 词）：
"Congrats on the Series A — quick question about your infra"
"Noticed you're hiring SREs — how are you managing on-call today?"
```

> 长度口径：以上示例即上限参考（10 词）。不要照搬"4-6 词短标题"这类更严的规则——本库示例与工作流第 3 步统一按 **英文 ≤10 词 / 中文 ≤20 字**。

## 适用场景

- B2B SaaS 公司的冷邮件外联
- 独立开发者向潜在客户推销
- 求职者向目标公司决策者发冷邮件
- 合作伙伴关系拓展

## 限制

- 主要面向 B2B 场景，B2C 邮件营销不在覆盖范围
- 不涉及邮件投递率技术配置（SPF/DKIM/DMARC）
- 不涵盖 Newsletter 或营销自动化（那是营销技能，这是销售技能）

## 相关参考（Playbook）

- 冷邮件结构、回复率杠杆与跟进节奏 → [references/outreach-playbook.md](../../references/outreach-playbook.md)（L2 方法论：怎么写与怎么跟，不替你生成真实邮件）
