## Description: <br>
Simplify SQL querying and troubleshooting for MySQL, PostgreSQL, and SQLite. Use when users ask to inspect schema, convert natural language to SQL, debug SQL errors, run explain plans, lint risky SQL, or validate data with safe read-only execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GaussZhu](https://clawhub.ai/user/GaussZhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect database schemas, generate or troubleshoot SQL, run lint and explain checks, and execute read-only queries against MySQL, PostgreSQL, or SQLite with summarized results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for database access, and write or lint safeguards can be bypassed with explicit flags. <br>
Mitigation: Review before installing, use a dedicated read-only database account, and avoid --allow-write and --no-lint unless that authority is intentionally granted. <br>
Risk: Natural-language ask mode can send schema metadata to the configured LLM provider. <br>
Mitigation: Do not use ask mode with confidential schemas unless policy allows sharing that metadata with the configured provider. <br>
Risk: Audit logs can contain command metadata, generated SQL, target labels, and error details. <br>
Mitigation: Keep audit log paths private and handle generated logs according to the database environment's data-handling policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/GaussZhu/sql-guard-copilot-zhu) <br>
- [Query Patterns](references/query_patterns.md) <br>
- [Chanquant Templates](references/chanquant_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and shell command snippets; command output may be table, JSON, or CSV when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May connect to MySQL, PostgreSQL, or SQLite using a user-provided DSN.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
