## Description: <br>
Helps users manage and operate Volcengine RDS PostgreSQL by interpreting natural-language requests, calling the bundled RDS PostgreSQL script for live results, and explaining responses or errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ybAmazing](https://clawhub.ai/user/ybAmazing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and database administrators use this skill to query Volcengine RDS PostgreSQL instances, databases, accounts, parameters, VPCs, subnets, and pricing from an agent conversation. It is suited for read-oriented operational inspection and troubleshooting with user-provided Volcengine credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses user-provided Volcengine cloud keys to perform live RDS PostgreSQL and VPC metadata queries. <br>
Mitigation: Use a dedicated least-privileged AK/SK with only the RDS PostgreSQL and VPC read permissions needed for the intended workflow. <br>
Risk: Returned instance, account, database, VPC, subnet, pricing, and configuration data may be sensitive. <br>
Mitigation: Treat command output as sensitive operational data and avoid sharing it outside approved environments. <br>
Risk: Unpinned SDK dependencies can change behavior across installs. <br>
Mitigation: Pin the Volcengine SDK version for repeatable deployments. <br>


## Reference(s): <br>
- [Volcengine RDS PostgreSQL Product](https://www.volcengine.com/product/rds-postgresql) <br>
- [Volcengine Access Key User Guide](https://www.volcengine.com/docs/6291/65568?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script output that may be JSON or table-formatted text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY environment variables and defaults to the cn-beijing region unless configured otherwise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
