## Description: <br>
根据提供的数据库表结构和自然语言需求生成规范、高效且包含中文注释的 SELECT 查询语句。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengnian2013](https://clawhub.ai/user/fengnian2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to convert natural-language database questions into formatted SQL SELECT queries using schema information fetched for a quoted product name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch schema information from an external URL based on the quoted product name. <br>
Mitigation: Install only if the schema endpoint is trusted and expected for the deployment context. <br>
Risk: The quoted product name or generated SQL may expose confidential business context. <br>
Mitigation: Avoid sensitive product names in prompts and review the generated SELECT query before running it against a real database. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengnian2013/sql-generator-skill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Schema endpoint base URL](https://open268v.cheyipai.com/img/c) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Markdown or plain text containing SQL SELECT code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SQL is intended to be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
