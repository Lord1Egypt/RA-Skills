## Description: <br>
A local SQL helper for formatting SQL, checking syntax, analyzing query structure and EXPLAIN output, and drafting SQL from natural-language prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to inspect, format, and reason about SQL locally without database access. It supports PostgreSQL EXPLAIN output and partial MySQL and SQLite analysis, plus template-based natural-language to SQL drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL is a draft and may include INSERT, UPDATE, or DELETE statements that could alter real data if run without review. <br>
Mitigation: Review all generated SQL before execution, especially write operations, and validate it against the target database and permissions model. <br>
Risk: The artifact README includes an optional external curl download path. <br>
Mitigation: Prefer the packaged artifact, and use any external download only when the source is trusted and independently verified. <br>
Risk: Static syntax checks and rule-based EXPLAIN analysis can miss database-specific behavior. <br>
Mitigation: Treat analysis as advisory and confirm important query plans, indexes, and syntax in the target database environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/sql-explain-cli) <br>
- [Artifact README](README.md) <br>
- [Artifact skill design](SKILL.md) <br>
- [sqlparse package](https://pypi.org/project/sqlparse/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Plain text, JSON, Markdown-style reports, and SQL snippets from local CLI or Python API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with sqlparse and does not require API keys or network access for normal use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
