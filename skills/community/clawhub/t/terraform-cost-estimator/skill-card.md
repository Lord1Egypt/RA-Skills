## Description:

Estimate infrastructure costs from Terraform plans by analyzing resource changes, predicting monthly spend, comparing alternatives, and identifying cost optimization opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and FinOps practitioners use this skill to estimate the cost impact of Terraform plans before applying infrastructure changes. It helps compare resource alternatives and identify optimization opportunities across AWS, GCP, and Azure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terraform plans may use cloud credentials or contain sensitive values.

Mitigation: Run the skill only in the intended Terraform workspace and avoid sharing generated plan JSON outside trusted contexts.

## Reference(s):

- [Terraform Cost Estimator on ClawHub](https://clawhub.ai/charlie-morrison/skills/terraform-cost-estimator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables, prose, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost estimates depend on Terraform plan completeness, provider pricing assumptions, region, and workload inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
