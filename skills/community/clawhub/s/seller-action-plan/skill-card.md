## Description:

Prioritizes evidence-based operational actions for an Amazon product using its product details and customer reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and operators use this skill to rank next steps for a single ASIN from product details and review evidence. It does not cover advertising accounts, inventory, or profit decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inconsistent spending controls can turn an expected preview into paid analysis.

Mitigation: Prefer a corrected package with free previews and a fixed workflow. If proceeding, require confirmation before each charge, use the operations quote/run workflow, choose manual collection for one-time work, and do not use deepdive as a quote-only preview.

## Reference(s):

- [Operation workflow](references/operation-workflow.md)
- [ARI CLI and API reference](references/reference.md)
- [ARI operations](https://ari.funewa.com/zh/operations)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Structured operational action plan with evidence-based priorities and checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single ASIN; grounded in product details and customer reviews; excludes advertising, inventory, and profit decisions.]

## Skill Version(s):

1.5.3 (source: server-resolved release evidence, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
