## Description: <br>
Validates migration SQL, analyzes index health, and applies pending schema migrations to the target database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink5725](https://clawhub.ai/user/ink5725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database maintainers use this skill to validate pending SQLite migration files, inspect index health, and apply schema migrations to a target database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a live database schema by writing and executing index-drop migrations. <br>
Mitigation: Require an explicit dry run, confirm the target database, and review the generated SQL before any migration is executed. <br>
Risk: The security review notes weak safeguards and behavior that does not fully match the skill description. <br>
Mitigation: Audit and modify the script before installation, and remove automatic DROP INDEX execution unless a human has approved the exact migration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ink5725/schema-manager) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands] <br>
**Output Format:** [JSON status report, with a generated SQL migration file when redundant indexes are found] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write and execute a cleanup migration named 003_drop_redundant_indexes.sql.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
