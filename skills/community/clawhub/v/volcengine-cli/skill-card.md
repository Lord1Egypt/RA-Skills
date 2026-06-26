## Description: <br>
Create and manage Volcengine cloud resources using the Volcengine CLI (`ve` command), including services such as ECS, VPC, CLB, RDS, and Redis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect, configure, create, modify, and troubleshoot Volcengine resources through CLI commands and API helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent manage real Volcengine cloud resources, including write, destructive, domain-registration, security-workflow, and billing-related operations. <br>
Mitigation: Install only for agents expected to manage Volcengine resources, require review before approving high-impact commands, and follow the skill's confirmation rules. <br>
Risk: Cloud credentials may grant broad access if long-lived keys or overly permissive profiles are used. <br>
Mitigation: Use least-privilege Volcengine credentials and prefer temporary or profile-based login over pasting AK/SK values into chat. <br>


## Reference(s): <br>
- [ClawHub Volcengine Cli Release](https://clawhub.ai/volc-sdk-team/skills/volcengine-cli) <br>
- [Common Error Handling](references/common-errors.md) <br>
- [Extended APIs](references/extend-apis.md) <br>
- [ECS Service Notes](references/ecs.md) <br>
- [VPC Service Notes](references/vpc.md) <br>
- [IAM Service Notes](references/iam.md) <br>
- [RDS Service Notes](references/rds.md) <br>
- [Redis Service Notes](references/redis.md) <br>
- [VKE Service Notes](references/vke.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run Volcengine CLI commands, request user confirmation for write or destructive operations, and use helper scripts for API discovery or extension calls.] <br>

## Skill Version(s): <br>
1.0.11 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
