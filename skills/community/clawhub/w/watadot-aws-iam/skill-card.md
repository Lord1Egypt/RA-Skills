## Description:

IAM security patterns by Watadot Studio. Manage users, roles, and policy verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordiy](https://clawhub.ai/user/ordiy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, and security practitioners use this skill to ask an agent for AWS IAM audit commands, role operations, policy inspection steps, and concise security best practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can suggest AWS IAM CLI commands against a configured AWS account, and IAM listings or policy documents may reveal sensitive account structure.

Mitigation: Use a least-privileged AWS profile where possible and review every command before execution.

Risk: IAM audit and policy lookup output may include usernames, role names, ARNs, access-key metadata, and policy details.

Mitigation: Handle command output as sensitive operational data and avoid sharing it outside approved channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ordiy/skills/watadot-aws-iam)
- [Publisher profile](https://clawhub.ai/user/ordiy)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the AWS CLI and an appropriately configured AWS account profile.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
