## Description: <br>
This skill helps agents generate candidate SQL indexes from table DDL and slow SQL for MySQL, Oracle, and PostgreSQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houyalei](https://clawhub.ai/user/houyalei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database engineers, and agents use this skill to analyze schema DDL with slow SQL and produce candidate CREATE INDEX statements with reasons for review before database changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CREATE INDEX statements are static suggestions and may not improve a real production workload. <br>
Mitigation: Review every statement with database execution plans and workload context before applying it. <br>
Risk: The skill reads local DDL and slow-query files and writes an output report to the chosen path. <br>
Mitigation: Run it in a project workspace, provide only intended SQL files, and choose an output path that will not overwrite important files. <br>
Risk: Additional indexes can increase write amplification and maintenance cost on high-write tables. <br>
Mitigation: Evaluate write impact, storage cost, and rollback plans before deploying suggested indexes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/houyalei/sql-index-optimizer-multi-db) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON report with SQL CREATE INDEX statements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided DDL and slow SQL files, then writes the selected report file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
