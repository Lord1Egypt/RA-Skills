## Description: <br>
Sql Gen helps agents generate SQL from natural-language requests with schema-aware query drafting, multi-table JOIN support, optimization advice, migration script drafting, and batch/version workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and DBAs use this skill to turn natural-language database requests into SQL, multi-table joins, migration scripts, and optimization guidance for team workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad database authority and command/write capabilities could affect live data or the host environment if used without review. <br>
Mitigation: Use least-privilege database credentials, prefer read-only schema access by default, and require explicit confirmation before migrations, writes, command execution, network calls, or SQL execution. <br>
Risk: Generated SQL, migration scripts, or optimization advice may be incorrect for a schema, SQL dialect, or workload. <br>
Mitigation: Review generated SQL, run dry-run or EXPLAIN checks, and test migrations in a staging environment before applying changes to production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/sql-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL and code snippets, JSON examples, configuration notes, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL queries, migration script drafts, optimization advice, batch generation notes, and database setup commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
