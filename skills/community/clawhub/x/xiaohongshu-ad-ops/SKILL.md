---
name: xiaohongshu-ad-ops
description: Plan, structure, and optimize Xiaohongshu (小红书) advertising workflows for lead generation, ecommerce, brand seeding, and conversion-oriented campaigns. Use when the user wants campaign strategy, account structure, audience angles, note/ad creative briefs, landing page hooks, budget allocation, testing plans, KPI design, creative iteration rules, or a reusable workflow for 小红书广告投放 and 种草转化. Also use when the user wants to turn a product or service into a Xiaohongshu ad operating plan rather than generic marketing advice.
---

# Xiaohongshu Ad Ops

Use this skill to turn a fuzzy ad idea into a practical Xiaohongshu ad workflow.

Default goal:
- clarify the offer
- define the campaign objective
- generate note/ad angles
- structure tests and budget
- improve lead quality and conversion

## What this skill covers

- 小红书信息流 / 笔记广告 planning
- 种草 + 转化 combined workflows
- leads for services, training, local business, AI services, consulting, SaaS, ecommerce
- creatives, hooks, note structure, CTA, landing-page alignment
- testing logic and iteration loops

## Core workflow

1. **Clarify the business first**
   Identify:
   - product / service
   - price band
   - target user
   - sales path
   - conversion action: 私信 / 表单 / 加企微 / 下单 / 留资
   - whether the goal is branding, lead gen, or direct conversion

2. **Choose the ad mode**
   - **Lead-gen mode**: 留资 / 私信 / 企业微信
   - **Seeding mode**: build认知 and搜索心智 first
   - **Conversion mode**: pull direct action with stronger CTA
   - **Hybrid mode**:种草 + 承接页 / 私域 / 销售转化

3. **Build the offer frame**
   Always answer:
   - why click now
   - why trust you
   - who this is for
   - what problem it solves
   - what happens after the click

4. **Design the campaign structure**
   Return when relevant:
   - campaign goal
   - audience buckets
   - angle matrix
   - creative/note directions
   - budget split
   - KPI targets
   - iteration rules

5. **Write ad-ready outputs**
   Prioritize:
   - hook lines
   - note titles
   - note outlines
   - CTA variants
   - landing-page /私信承接 copy
   - sales follow-up suggestions

## Recommended output format

### 1. 投放目标
- 这轮广告到底要拿什么结果

### 2. 用户分层
- 冷用户
- 半热用户
- 高意向用户

### 3. 选题 / 角度矩阵
- 痛点角度
- 结果角度
- 案例角度
- 反常识角度
- 对比角度

### 4. 素材 / 笔记方向
- 标题
- 开头钩子
- 正文框架
- CTA

### 5. 预算与测试计划
- 先测什么
- 每组预算怎么分
- 观察哪些指标
- 什么时候关停 / 放量

### 6. 承接设计
- 落地页重点
- 私信首句
- 销售跟进脚本方向

## What usually goes wrong

Avoid these mistakes:
- 只讲产品，不讲用户情境
- 只做种草，不设计承接
- 只追点击，不看留资质量
- 创意全是同一种角度
- 没有测试节奏和停放规则
- 笔记像广告话术，不像真实内容

## Chinese ad-writing rules

- 开头先打情境或痛点，不先自夸
- 小红书内容要像内容，不像硬广
- 强调“适合谁 / 不适合谁”会更容易筛选线索
- 先让用户产生代入，再谈产品
- CTA 不要一味硬推，优先“先私信 / 先领取 / 先测一下”这类低门槛动作

## Best use cases

This skill is especially strong for:
- AI 安装 / 培训 / 顾问服务
- 本地商家获客
- 高客单服务型产品
- 小团队投流测试
- 想把种草内容和销售承接串起来的业务

## Bundled resources

- `references/xhs-ad-principles.md` — platform-fit ad logic and投放 thinking
- `references/creative-matrix.md` — angle matrix for ad/note ideation
- `references/lead-gen-playbook.md` — lead-generation and conversion handoff patterns
- `references/note-templates.md` — 爆款标题 / 笔记模板 / CTA 模板
- `references/industry-templates.md` — AI服务 / 本地商家 / 教育培训 / 高客单服务行业模板
- `references/landing-and-dm.md` — 落地页与私信承接模板
- `references/review-template.md` — 投放复盘模板
- `scripts/xhs_ad_plan_brief.py` — generate a structured Xiaohongshu ad plan brief from raw business info

## Script usage

```bash
python3 scripts/xhs_ad_plan_brief.py <input.txt>
```

Use the script for a quick first-pass plan, then refine with business judgment.

## Default stance

Small-budget practical.
Less theory, more plan.
Focus on conversion path, not vanity metrics.
