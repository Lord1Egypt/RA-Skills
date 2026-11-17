## Description: <br>
Helps agents draft, explain, optimize, and review SQL queries, schema designs, indexes, ER diagrams, and migration SQL for common relational databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to turn natural language requirements into SQL, tune slow queries, and draft database schemas or migration scripts for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL or migration scripts could alter or damage production data if executed without review. <br>
Mitigation: Require human approval before execution and test against read-only replicas or disposable databases first. <br>
Risk: The skill requests execution and write-capable tooling while producing database design and DDL guidance. <br>
Mitigation: Install it only in constrained agent environments and avoid granting production database credentials or unrestricted write access. <br>
Risk: Schema, index, and optimization suggestions may be incomplete or unsuitable for a specific database version, workload, or dialect. <br>
Mitigation: Validate generated SQL with the target database, review execution plans, and adapt dialect-specific syntax before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/sql-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SQL, DDL, migration scripts, and execution suggestions should be treated as advisory until reviewed and tested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
