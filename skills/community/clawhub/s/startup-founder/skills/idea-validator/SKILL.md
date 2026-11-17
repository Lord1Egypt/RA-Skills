---
name: idea-validator
description: 创业点子验证 — 用市场时机、商业数学和用户需求框架评估点子是否值得投入
source:
  type: derived
  repo: skills-repo/startup-founder
  path: skills/idea-validator/SKILL.md
  url: https://skills.sh/refoundai/lenny-skills/evaluating-startup-ideas
  version: 1.0.0
  updated: 2026-07-29
metadata:
  author: hope
  category: 创业
  platform: 通用
  difficulty: 入门
  version: 1.0.0
  created: 2026-07-29
tags:
  - startup
  - validation
  - idea
  - product-market-fit
---

# Idea Validator — 创业点子验证

> 90% 的创业点子死在不该开始的地方。本技能用系统化框架帮你区分「坑」和「机会」，确保在写代码前先确认有人愿意付钱。

## 能力

- 评估问题紧迫性：是救火级痛点还是锦上添花
- 分析市场时机：技术、监管、用户行为是否有「为什么是现在」的拐点
- 审核商业可行性：用基础数学验证是否有路径达到可持续收入
- 设计验证实验：从头脑风暴过渡到手动测试，确认付费意愿
- 识别 tarpit ideas：看起来吸引人但实际无法盈利的点子类型

## 使用方式

```
/idea-validator 我在考虑做一个 AI 客服 SaaS，帮我验证这个点子
/idea-validator 帮我分析这个市场有没有"为什么是现在"的时机
/idea-validator 我想做个人财务管理工具，这是 tarpit idea 吗
```

## 工作流

1. **问题定位** — 谁有这个问题？有多痛？他们现在怎么解决的？
2. **市场分析** — 为什么是现在？技术/监管/行为有什么变化？
3. **商业数学** — 客单价 × 目标用户数 × 转化率 → 能到 $100K ARR 吗？
4. **竞品扫描** — 现有解决方案是什么？你的差异化在哪？
5. **付费验证** — 在写代码前，找到至少 3 个愿意付钱的人

## 核心框架

### 寻找无竞争利基
> 「竞争等于低利润。竞争者越多，价格越低，生意越难做。」— Andrew Wilkinson

在 pest control、政府软件等被忽视的行业，缺乏竞争意味着更高的利润和更简单的增长。

### 追求自主结果
> 「AI 时代最好的机会是交付自主结果，而不是做生产力工具。」— Bret Taylor

不要数字化旧流程，要创造全新体验。用户要的是「问题解决了」，不是「我帮你了」。

### 等待外部转折点
> 「突破性成功依赖于识别技术或行为的具体变化。」— Mike Maples Jr

成功的创业往往踩中了某个 inflection point：新技术普及、法规变化、用户行为迁移。

### 先卖再建
在写一行代码之前，确认有人愿意为你的人工服务付费。如果没人买你的手工版，也没人会买你的自动化版。

## 适用场景

- 有多个创业想法，不确定先做哪个
- 想验证一个点子是否值得投入 3-6 个月
- 被投资人/朋友质疑点子但需要客观评估
- 在做 side project，想确认不是自嗨

## 限制

- 无法预测黑天鹅事件（政策突变、技术突破）
- 验证结果取决于样本质量（问错人会得到错误结论）
- 消费级和企业级验证方法不同，需区分场景
- 有些好点子早期看起来像坏点子（反之亦然）

## 相关参考（Playbook）

- 上游方法论：`../../references/validation-methodology.md` — 三问前置、验证阶梯与失败信号；**本子技能只做逐项评估与结论输出，「该不该继续/什么时候止损」的判据以该 playbook 为准**。
- 验证通过后：`../../skills/mvp-builder/SKILL.md` 承接构建；结论为「暂缓」时回 playbook 第 4 节检查清单补前置条件。
