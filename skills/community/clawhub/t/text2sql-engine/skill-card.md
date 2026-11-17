## Description: <br>
Text2sql Engine helps data engineers and DBAs turn natural-language requirements into SQL, explain and compare queries, analyze execution plans, and recommend indexes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, data engineers, analysts, and DBAs use this skill to generate relational SQL from natural language, adapt queries across dialects, explain query logic, analyze execution plans, and draft index or performance-tuning recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad command and file-writing authority in a database workflow can increase impact if the agent receives production database credentials. <br>
Mitigation: Use read-only credentials by default, scope DATABASE_URL to non-production unless approved, and require explicit approval before DDL, shell commands, or file writes. <br>
Risk: Generated SQL, DDL, index, and optimization recommendations can be incorrect or disruptive if executed without review. <br>
Mitigation: Have a DBA review generated statements, test against representative data, and execute DDL only through normal change-control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/text2sql-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL code blocks, JSON-like status objects, shell command snippets, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL explanations, execution-plan analysis, alternative queries, security audit notes, and index recommendations; generated SQL and DDL should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
