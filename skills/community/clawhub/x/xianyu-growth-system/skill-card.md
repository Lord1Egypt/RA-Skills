## Description:

A Chinese-language Xianyu operations growth skill that helps sellers evaluate products, model unit economics, design tests, create listings, improve buyer conversations, diagnose data, manage SKU lifecycle, and make growth decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and operators use this skill to plan Xianyu marketplace experiments, evaluate SKU profitability, draft compliant listing and conversation guidance, diagnose operational metrics, and decide when to scale, pause, or stop an item.

### Deployment Geography for Use:

Global; intended for Xianyu marketplace operations where the platform is available.

## Known Risks and Mitigations:

Risk: Xianyu platform rules, fees, thresholds, and enforcement practices may change or vary by account and category.

Mitigation: Verify current Xianyu policy and account status before applying operational recommendations.

Risk: Buyer conversations can contain phone numbers, addresses, names, payment details, or other personal data.

Mitigation: Use only redacted or anonymized chat excerpts when asking the skill to analyze conversations.

Risk: Operational thresholds and recommendations may not fit every category, season, account level, or supply situation.

Mitigation: Treat the skill's thresholds as starting points, compare them with the seller's own data, and review recommendations before acting.

## Reference(s):

- [闲鱼平台规则与算法原理](references/00-platform-rules.md)
- [核心原则与决策引擎](references/01-principles.md)
- [机会发现与选品评分](references/02-opportunity.md)
- [单位经济模型](references/03-unit-economics.md)
- [实验设计框架](references/04-experiment.md)
- [商品页生成（标题 + 图片 + 文案 + 定价）](references/05-listing.md)
- [客服对话优化](references/06-conversation.md)
- [数据诊断](references/07-data-diagnosis.md)
- [SKU生命周期管理](references/08-lifecycle.md)
- [风险管理](references/09-risk.md)
- [产品化与规模化](references/10-productization.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured YAML-style decision blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include product decisions, confidence scores, unit economics, risks, experiment plans, listing drafts, conversation replies, diagnostics, next actions, and stop conditions.]

## Skill Version(s):

1.0.0 (source: release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
