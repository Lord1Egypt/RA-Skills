## Description:

MySQL database design assistant that reads business-rule documents and existing SQL DDL scripts to generate MySQL 5.7/8.0 CREATE TABLE statements following Alibaba and Alibaba Cloud RDS conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2320117707](https://clawhub.ai/user/2320117707)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to turn business requirements, Markdown rule documents, or existing SQL scripts into MySQL table designs. It produces DDL, table-structure explanations, indexing guidance, and compatibility notes for MySQL 5.7 and 8.0.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL defaults can include DROP TABLE IF EXISTS statements that may remove database objects if executed in a real environment.

Mitigation: Review generated SQL before use, remove or explicitly approve DROP TABLE statements, confirm the target environment, and verify backups before execution.

Risk: The skill may search or read local Markdown and SQL files broadly while gathering requirements or existing schema context.

Mitigation: Constrain the agent's file access to the intended workspace and provide only the requirement and SQL files needed for the design task.

## Reference(s):

- [Alibaba Java Development Manual - Database Rules](https://github.com/alibaba/p3c)
- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [MySQL 5.7 Reference Manual](https://dev.mysql.com/doc/refman/5.7/en/)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Markdown with SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include table structure explanations, index design notes, business-rule summaries, compatibility notes, and best-practice recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
