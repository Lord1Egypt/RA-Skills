## Description:

Helps agents manage and operate Volcengine RDS PostgreSQL by querying instances, databases, accounts, parameters, network resources, and pricing through the bundled CLI script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ybamazing](https://clawhub.ai/user/ybamazing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to inspect and explain Volcengine RDS PostgreSQL resources, including instance details, databases, accounts, parameters, VPCs, subnets, and price estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed cloud requests can be directed to a custom API endpoint.

Mitigation: Use least-privilege Volcengine credentials, do not allow natural-language requests to set --endpoint unless it is restricted to an official trusted Volcengine API host, and prefer a locked dependency environment before running with real cloud credentials.

## Reference(s):

- [Volcengine RDS PostgreSQL](https://www.volcengine.com/product/rds-postgresql)
- [Volcengine access credential guide](https://www.volcengine.com/docs/6291/65568?lang=zh)
- [ClawHub skill page](https://clawhub.ai/ybamazing/skills/volcengine-rds-postgresql)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stderr status lines and stdout JSON returned by the Volcengine SDK.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
