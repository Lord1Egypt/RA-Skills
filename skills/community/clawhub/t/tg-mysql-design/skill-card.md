## Description: <br>
tg-mysql-design helps agents design MySQL 5.7/8.0 CREATE TABLE DDL from business requirements, Markdown documents, and existing SQL scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2320117707](https://clawhub.ai/user/2320117707) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and database engineers use this skill to turn business rules or existing schema notes into MySQL table designs with fields, indexes, audit columns, comments, and compatibility guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DDL may include destructive statements such as DROP TABLE examples or rebuild plans. <br>
Mitigation: Review generated SQL before use, require backups and explicit confirmation, and avoid running destructive statements against production databases. <br>
Risk: Broad activation wording may cause the skill to inspect local Markdown or SQL files beyond the intended design task. <br>
Mitigation: Point the skill at specific files or folders and avoid giving it unrestricted workspace context when only a narrow schema design is needed. <br>


## Reference(s): <br>
- [Alibaba Java Development Manual](https://github.com/alibaba/p3c) <br>
- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/) <br>
- [MySQL 5.7 Reference Manual](https://dev.mysql.com/doc/refman/5.7/en/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with SQL code blocks and explanatory notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated DDL should be reviewed before database execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
