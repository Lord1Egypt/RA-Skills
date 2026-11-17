## Description:

Recommend optimal Reserved Instance and Savings Plan portfolio based on AWS usage patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers, cloud engineers, and finance stakeholders use this skill to analyze user-supplied AWS usage exports and plan Reserved Instance or Savings Plan commitments. It helps compare conservative and aggressive coverage scenarios, estimate savings, and flag workloads that are poor commitment candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS cost and usage exports can reveal sensitive infrastructure and spending patterns.

Mitigation: Use sanitized exports where possible and avoid sharing AWS access keys, secret keys, session tokens, or unrelated account data.

Risk: Recommendations based on incomplete or stale usage data can lead to unsuitable AWS commitment purchases.

Mitigation: Review the generated recommendations against current workload stability, pricing, and finance policy before purchasing Reserved Instances or Savings Plans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmolnagpal/skills/ri-savings-advisor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with AWS CLI command examples and structured recommendation sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces coverage gap analysis, a recommendation table, risk assessment, scenario comparison, and finance summary from user-provided AWS usage data.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
