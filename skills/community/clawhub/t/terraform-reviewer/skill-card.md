## Description: <br>
Review Terraform plans and HCL files for AWS security misconfigurations before deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, cloud engineers, and security reviewers use this skill to review AWS Terraform HCL, Terraform plan JSON, or resource summaries for security misconfigurations before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terraform HCL, plan JSON, or resource summaries may include secrets, account identifiers, or sensitive infrastructure details. <br>
Mitigation: Review and redact sensitive values before sharing inputs with the agent. <br>
Risk: Security findings or corrected HCL snippets may be incomplete or incorrect for a specific environment. <br>
Mitigation: Review recommendations before use and validate changes with normal Terraform, security, and peer review processes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with findings tables, corrected HCL snippets, and a PR review comment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only review output based on user-provided Terraform HCL, plan JSON, or resource summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
