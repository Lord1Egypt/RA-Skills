## Description:

Observability and monitoring by Watadot Studio. Log tailing and metric extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordiy](https://clawhub.ai/user/ordiy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect AWS CloudWatch logs, metrics, alarms, and dashboards through AWS CLI command patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS CLI use with overly broad IAM permissions can expose more CloudWatch data than intended.

Mitigation: Install and run the skill only where AWS CLI credentials have least-privilege read access for the intended accounts and log groups.

Risk: CloudWatch logs can contain sensitive application or customer data.

Mitigation: Review queried log groups and outputs for sensitivity before sharing or retaining command results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ordiy/skills/watadot-aws-cloudwatch)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AWS CLI access; commands should be adjusted to target AWS account, region, log group, dashboard, metric, or resource identifiers.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
