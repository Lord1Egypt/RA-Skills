## Description:

Extract and cluster defect signals from ecommerce reviews and social feedback into actionable quality and fix priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Product, quality, content, and voice-of-customer teams use this skill to analyze low-star reviews, comments, support tickets, and return notes. It turns defect themes into prioritized fixes, evidence tables, and short execution plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review, ticket, or return-note inputs may contain personal or sensitive data.

Mitigation: Use appropriately filtered or de-identified inputs and follow internal data handling rules before analysis.

Risk: Small or skewed review samples can lead to overgeneralized defect priorities.

Mitigation: Report sample size and confidence, preserve evidence snippets, and validate high-priority fixes with additional data.

Risk: Defect clusters can mix product quality issues with logistics or service issues.

Mitigation: Separate quality, packaging, delivery, usability, and expectation-mismatch categories before assigning owners.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leooooooow/skills/review-defect-miner)
- [Publisher profile](https://clawhub.ai/user/leooooooow)
- [Output template](references/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with an executive summary, prioritized actions, evidence table, and 7-day plan.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves evidence snippets, separates defect categories from logistics or service issues, and avoids over-generalizing from small samples.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
