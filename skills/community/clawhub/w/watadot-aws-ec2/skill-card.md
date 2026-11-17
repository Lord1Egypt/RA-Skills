## Description:

Elastic compute management by Watadot Studio. Deployment, scaling, and state monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordiy](https://clawhub.ai/user/ordiy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to have an agent propose AWS CLI commands and operational guidance for EC2 instance discovery, lifecycle control, and security group management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated EC2 commands can delete instances or change network access if run with the wrong account, region, resource IDs, or CIDR ranges.

Mitigation: Before running any generated AWS command, verify the AWS account, region, instance IDs, security group IDs, and CIDR ranges, especially for termination and SSH ingress changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ordiy/skills/watadot-aws-ec2)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AWS CLI availability and user validation before command execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
