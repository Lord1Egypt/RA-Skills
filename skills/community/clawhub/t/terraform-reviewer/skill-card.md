## Description:

Review Terraform plans and HCL files for AWS security misconfigurations before deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to review AWS Terraform HCL, Terraform plan JSON, or exported resource configuration for security misconfigurations before deployment. It produces prioritized findings, CIS AWS Foundations Benchmark v2.0 mappings, corrected HCL snippets, and a paste-ready PR review comment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste Terraform output that contains secrets or credentials.

Mitigation: Review and redact inputs before analysis; the skill instructs users not to include credentials, access keys, or secret keys.

Risk: Terraform plan output may not show every security implication of deployed infrastructure.

Mitigation: Treat findings as review guidance and validate recommendations against source HCL, plan JSON, and deployed resource context before deployment.

## Reference(s):

- [Terraform Reviewer on ClawHub](https://clawhub.ai/anmolnagpal/skills/terraform-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with findings tables, corrected HCL snippets, shell commands, and a PR review comment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only review guidance; users provide Terraform HCL, Terraform plan JSON, or exported resource configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
