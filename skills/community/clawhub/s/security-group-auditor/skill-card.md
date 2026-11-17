## Description:

Audit AWS Security Groups and VPC configurations for dangerous internet exposure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers, cloud engineers, and security teams use this skill to review exported AWS security group, EC2, VPC, and subnet data for risky internet exposure and overly broad network access. It helps produce prioritized findings, tightened rule suggestions, and monitoring recommendations without requiring account credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS networking exports may reveal infrastructure layout, and suggested replacement rules could affect connectivity if applied without review.

Mitigation: Do not provide credentials or secret keys; manually review proposed security group changes before applying them in AWS.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmolnagpal/skills/security-group-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown findings with tables, JSON rule examples, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only analysis based on user-provided AWS networking exports; does not request credentials or access AWS accounts directly.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
