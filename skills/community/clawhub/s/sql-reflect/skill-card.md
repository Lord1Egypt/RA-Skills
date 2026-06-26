## Description: <br>
sql-reflect helps developers trace a SQL query back to the PHP/Laravel code that likely generated it by comparing table names, fields, conditions, relationships, and call paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willing-lin](https://clawhub.ai/user/willing-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers maintaining PHP/Laravel applications use this skill to investigate which files, methods, model relationships, and calling paths may have generated a given SQL statement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose snippets or paths from proprietary PHP/Laravel source while searching for SQL origins. <br>
Mitigation: Use it only in repositories where source-code inspection and sharing matching snippets are acceptable. <br>
Risk: Static table, field, and relationship matching can misidentify dynamically generated SQL or ambiguous query builders. <br>
Mitigation: Treat findings as candidate locations and verify them against runtime logs, bindings, and application call paths before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/willing-lin/sql-reflect) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with PHP and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, method names, line numbers, Laravel relationship chains, SQL structure notes, and multiple candidate source locations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
