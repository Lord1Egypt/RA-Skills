## Description: <br>
Helps an agent use a Volcengine RDS MySQL helper script to query RDS MySQL instances, databases, accounts, parameters, VPCs, subnets, and pricing with user-provided Volcengine credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and support engineers use this skill to inspect Volcengine RDS MySQL and related network metadata during operations and troubleshooting. The agent can prepare and run supported shell commands, then summarize JSON results and suggest follow-up checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Volcengine cloud credentials and can expose RDS, VPC, subnet, account, parameter, and pricing metadata to the agent session. <br>
Mitigation: Use a dedicated least-privilege IAM key scoped to the needed read APIs and regions, and avoid sharing returned infrastructure details in untrusted contexts. <br>
Risk: Live API responses can include operational details that may be sensitive for production environments. <br>
Mitigation: Review command intent before execution and redact identifiers or configuration details before copying results outside trusted systems. <br>
Risk: The Volcengine SDK dependency is specified with a lower bound, so future installs may resolve to newer SDK behavior. <br>
Mitigation: Pin the SDK version in controlled deployments when reproducible behavior is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/volcengine-rds-mysql) <br>
- [Volcengine RDS MySQL product page](https://www.volcengine.com/product/rds-mysql) <br>
- [Volcengine access key user guide](https://www.volcengine.com/docs/6291/65568?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the user's Volcengine credentials, selected region, and live RDS or VPC API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
