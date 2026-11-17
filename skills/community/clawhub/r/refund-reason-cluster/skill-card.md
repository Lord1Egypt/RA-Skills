## Description:

Clusters refund and return reasons into actionable root-cause groups and prevention plans.

This skill is for research and development only.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Ecommerce, support, and operations teams use this skill to analyze refund logs, return reason text, support transcripts, and order metadata so they can find recurring refund drivers and prioritize prevention actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refund, return, support, and order data may include customer identifiers or sensitive commercial details.

Mitigation: Redact unnecessary customer identifiers and sensitive details before using the skill.

Risk: Small samples or low-quality refund reason text may lead to unreliable root-cause clusters.

Mitigation: Review sample-size, data-quality, and confidence caveats before acting on recommendations.

Risk: Fraud or policy-abuse signals can be confused with genuine product dissatisfaction.

Mitigation: Separate policy abuse from product dissatisfaction before prioritizing product, operations, or messaging changes.

## Reference(s):

- [Output Template](references/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured as an executive summary, priority actions, evidence table, and 7-day execution plan.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
