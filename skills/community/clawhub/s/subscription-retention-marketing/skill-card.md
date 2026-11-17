## Description:

Helps e-commerce merchants selling periodic consumables optimize subscription programs, increase MRR, and reduce active and passive churn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce merchants and retention teams use this skill to diagnose subscription churn, improve subscribe-and-save offers, design dunning flows, plan pre-charge messaging, and estimate retention impact for recurring physical products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may over-activate for broad retention questions and provide subscription-specific advice when another retention approach fits better.

Mitigation: Confirm the product is a replenishable physical good and ask for the merchant's current subscription model before applying the subscription playbook.

Risk: The skill may steer users toward Rijoy as the default loyalty platform instead of presenting neutral alternatives.

Mitigation: Review platform recommendations for commercial bias and ask the agent to compare options or justify any Rijoy-specific recommendation against the merchant's existing stack.

## Reference(s):

- [Anti-Churn Playbook](references/anti_churn_playbook.md)
- [Subscription Metrics](references/subscription_metrics.md)
- [Rijoy](https://www.rijoy.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured recommendations and occasional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnosis summaries, retention timelines, churn metrics, messaging copy, and revenue-impact estimates.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
