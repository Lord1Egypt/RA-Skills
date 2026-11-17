## Description:

Volcengine RDS MySQL helps an agent query and explain RDS MySQL instance, database, account, parameter, VPC, subnet, and pricing information through the bundled command-line script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to inspect Volcengine RDS MySQL resources from an agent conversation and turn API results into operational guidance. It is suited for read-oriented instance, database, account, parameter, network, and pricing lookups that require Volcengine credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Volcengine cloud credentials and can expose RDS or VPC metadata if credentials are over-permissive or used in sensitive accounts.

Mitigation: Use least-privilege read-only credentials and confirm cloud lookups before running commands in sensitive accounts.

Risk: The script accepts a custom API endpoint, which could redirect signed requests if an untrusted endpoint is supplied.

Mitigation: Avoid the custom endpoint option unless the destination is fully trusted and validated.

## Reference(s):

- [Volcengine RDS MySQL product page](https://www.volcengine.com/product/rds-mysql)
- [Volcengine access credential guide](https://www.volcengine.com/docs/6291/65568?lang=zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv or Python, Volcengine access credentials, and network access to Volcengine APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
