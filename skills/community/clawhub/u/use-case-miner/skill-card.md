## Description:

从 Amazon 评论和商品详情的证据中提炼真实使用场景、限制条件与用户体验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce operators use this skill to turn product details and review evidence into grounded use-case insights, including user needs, limitations, and experiences. It is scoped to scenario analysis and excludes unsupported demographic claims, ad targeting, and marketing promises.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some commands may incur credit charges, and recurring collection can create ongoing costs.

Mitigation: Review before installing; set ARI to ask before every charge and keep collection manual unless recurring costs are explicitly approved.

Risk: The broader account controls may exceed the intended scenario-analysis scope.

Mitigation: Use a build that enforces scenario-only access and review its available operations before use.

## Reference(s):

- [ARI API reference](references/reference.md)
- [Scenario operations workflow](references/operation-workflow.md)
- [ARI Operations](https://ari.funewa.com/zh/operations)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Concise, evidence-grounded Markdown insights or an operations report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connects scenario findings to review evidence and stated limits; does not make unsupported demographic or marketing claims.]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
