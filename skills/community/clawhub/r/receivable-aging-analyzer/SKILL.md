---
name: Receivable Aging Analyzer
version: v1.0.0
tags: accounts-receivable, collections-strategy, cash-flow-management, aging-analysis, credit-control
---

# Receivable Aging Analyzer

## Overview

Analyzes accounts receivable aging and suggests prioritization strategies for collections. This is a descriptive skill that provides templates, frameworks, and heuristic analysis without executing real code, accessing external APIs, or performing actual financial transactions.

## Trigger

Use this skill when the user wants to:
- get structured guidance on receivable aging analyzer
- apply best-practice frameworks to their financial situation
- generate templates and checklists for financial planning

### Example prompts
- "Help me create a personal budget"
- "Analyze my cash flow forecast"
- "Check my expense categorization"
- "Assess my financial health"
- "Review my receivables aging"
- "Check invoice compliance"
- "Develop a pricing strategy"
- "Find cost reduction opportunities"
- "Optimize my tax deductions"
- "Interpret my financial reports"

## Workflow

1. User provides context and goals.
2. Skill applies built-in templates and frameworks.
3. Skill generates structured output with recommendations.
4. User receives actionable insights and next steps.

## Inputs
- User context (financial situation, goals, constraints)
- Optional data inputs (amounts, categories, timeframes)
- Analysis preferences

## Outputs
- Structured analysis report
- Templates and frameworks
- Actionable recommendations
- Next steps checklist


## Usage Scenarios

1. **User input:** "Analyze our AR aging: 30% is over 60 days. How do we prioritize collections?"
→ **Expected output:** Tiered collection strategy — 0-30 days (automated reminders), 31-60 (personal outreach + payment plans), 61-90 (escalation + late fees), 90+ (collections/legal review) — with expected recovery rates by tier and weekly action plan for top 10 delinquent accounts.
2. **User input:** "Our DSO has climbed from 35 to 52 days. Diagnose the root cause and fix it."
→ **Expected output:** DSO decomposition analysis — identifies that 60% of increase is from 3 large accounts with extended terms, 25% from invoice dispute delays, 15% from slow small accounts — with corrective actions per root cause.
3. **User input:** "Design a proactive credit control system to prevent receivable aging issues."
→ **Expected output:** Credit control framework — customer credit assessment checklist, credit-limit policy, payment-term tiering (Net 15/30/45 based on risk), early-payment discount structure, automated dunning schedule, and monthly AR health dashboard template.



### Scenario 2: 小老板追款讨债指南
**User input:** "我自己开了个小公司，客户拖账拖了半年，现在欠我40多万。每次打电话都说下周付，下周永远不来。怎么系统性地处理这笔应收款？"
**Expected output:** 小微企业应收账款催收体系——第一步：账龄分级（30天以内电话提醒、60天微信正式催、90天发律师函、120天起诉准备）；第二步：催收话术剧本（第一通电话温和确认是否收到发票、第二通问付款障碍、第三通提供分期方案、第四通最后通牒）；第三步：证据链整理（合同+送货单+微信聊天记录录屏+发票+催收记录，装订成册）；第四步：催收外包方案（在催收平台如资产360挂单，催回按比例收费）。关键：所有沟通留痕，对微信记录定期截图保存。

## Safety
- No real financial transactions or API calls
- No access to real bank accounts or financial systems
- Recommendations are informational only
- Users should consult financial professionals for actual decisions

## Acceptance Criteria
- Must return structured markdown/JSON output
- Must include actionable recommendations
- Must clearly state the descriptive/non-executable nature
- Must provide templates or frameworks for user adaptation
