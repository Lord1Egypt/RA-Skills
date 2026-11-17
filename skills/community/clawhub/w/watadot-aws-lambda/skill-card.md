## Description:

Serverless compute orchestration by Watadot Studio. Manage functions, triggers, and cloud rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordiy](https://clawhub.ai/user/ordiy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to get AWS Lambda CLI commands and operational guidance for function lifecycle management, deployment, configuration, scaling, and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS Lambda update and provisioned concurrency commands can change cloud resources or affect cost.

Mitigation: Review the AWS account, region, function names, IAM permissions, and cost-impacting parameters before executing changes.

Risk: Function configuration or deployment guidance may be applied to the wrong function or environment.

Mitigation: Confirm function names, aliases, environment variables, payloads, and deployment artifacts before running commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ordiy/skills/watadot-aws-lambda)
- [Publisher Profile](https://clawhub.ai/user/ordiy)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AWS CLI access and user review before cloud-changing commands are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
