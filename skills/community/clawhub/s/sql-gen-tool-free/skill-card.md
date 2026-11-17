## Description: <br>
SQL生成器(免费版) helps independent developers, product managers, and AI agents turn natural-language database requests into SQL queries, explanations, DDL, test data, and quick-reference guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, product managers, and AI agents use this skill to draft, explain, validate, and manage SQL for routine database tasks from natural-language requests. It is not intended to make database architecture decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may enable live database execution or data-changing SQL without clear safety guardrails. <br>
Mitigation: Review every generated statement and require explicit confirmation before executing INSERT, UPDATE, DELETE, or DDL. <br>
Risk: Database schemas or credentials could expose sensitive information when used as input. <br>
Mitigation: Use sanitized schema input where possible and avoid production credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/sql-gen-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL, DDL, INSERT examples, and execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated SQL statements, SQL explanations, test data examples, status messages, and logs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
