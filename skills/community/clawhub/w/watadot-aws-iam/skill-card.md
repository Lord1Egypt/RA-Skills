## Description: <br>
IAM security patterns by Watadot Studio. Manage users, roles, and policy verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ordiy](https://clawhub.ai/user/ordiy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, and security teams use this skill to audit AWS IAM identities, inspect access keys, assume roles, review attached policies, and check effective policy documents with AWS CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IAM audit and role commands can expose sensitive account, identity, policy, or credential metadata when run in a real AWS environment. <br>
Mitigation: Review commands before execution, use least-privilege AWS credentials, avoid sharing command output externally, and prefer read-only permissions for audit workflows. <br>
Risk: Role assumption and policy inspection workflows can affect security decisions if run against the wrong AWS account, role, or policy ARN. <br>
Mitigation: Confirm the target account, role ARN, policy ARN, and version ID before running commands, and require MFA or approved change controls for privileged sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ordiy/watadot-aws-iam) <br>
- [Publisher profile](https://clawhub.ai/user/ordiy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with AWS CLI command examples and concise best-practice guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the AWS CLI to run the command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
