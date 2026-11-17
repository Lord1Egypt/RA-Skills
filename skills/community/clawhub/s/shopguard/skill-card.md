## Description:

Cross-platform shopping risk and after-sales decision skill for mainland China that evaluates merchant credibility, hidden post-purchase friction, refund difficulty, and evidence-retention needs across Taobao, Tmall, JD, PDD, Meituan, elm, and similar marketplaces, then tells the user whether to buy, switch seller, use the low-price path carefully, or avoid the order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping assistants use ShopGuard to pressure-test seller paths before purchase, especially where a low price may trade off against refund friction, after-sales hassle, gifting suitability, urgency, or evidence-retention needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat shopping risk advice as authorization to take account, seller-contact, or checkout actions.

Mitigation: Keep the skill limited to public listing inspection, seller and policy comparison, risk guidance, and evidence advice unless the user gives separate explicit direction for any account or checkout step.

Risk: Marketplace signals can be incomplete, stale, or only directional, which may lead to overconfident seller-risk conclusions.

Mitigation: Separate confirmed facts from inferences, avoid claiming private complaint statistics, and tell users what visible evidence to save before ordering.

## Reference(s):

- [ShopGuard ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/shopguard)
- [Evidence Checklist](references/evidence-checklist.md)
- [Risk Signals](references/risk-signals.md)
- [Verdict Cards](references/verdict-cards.md)
- [Example Prompts](references/example-prompts.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Analysis]

**Output Format:** [Markdown with clear verdict sections and practical evidence-retention steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces direct buy, switch-seller, use-carefully, or avoid recommendations; does not produce checkout actions.]

## Skill Version(s):

1.0.0 (source: frontmatter, clawhub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
