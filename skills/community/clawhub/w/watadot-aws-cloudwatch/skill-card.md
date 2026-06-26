## Description: <br>
Observability and monitoring by Watadot Studio. Log tailing and metric extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ordiy](https://clawhub.ai/user/ordiy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect AWS CloudWatch logs, metrics, alarms, and dashboard names during observability and troubleshooting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS CloudWatch inspection can expose logs, metrics, alarms, or dashboard metadata outside the intended account, region, or resource scope if the agent uses overly broad credentials. <br>
Mitigation: Use a least-privilege, read-only AWS profile limited to the intended account, region, log groups, alarms, and metrics. <br>
Risk: Live log tailing can continue collecting troubleshooting data longer than needed. <br>
Mitigation: Stop live log tailing when troubleshooting is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ordiy/watadot-aws-cloudwatch) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the AWS CLI and an AWS profile with access to the intended CloudWatch resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
