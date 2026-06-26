## Description: <br>
Reviews sqlx database code for compile-time query checking, connection pool management, migration patterns, and PostgreSQL-specific usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review Rust projects that use sqlx for query safety, type mapping, connection pool management, transactions, and migrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review guidance can be misleading if applied without inspecting the relevant Cargo.toml, sqlx configuration, and source lines. <br>
Mitigation: The skill requires scope checks, file-line anchors, and evidence gates before assigning high-severity findings. <br>


## Reference(s): <br>
- [Queries](references/queries.md) <br>
- [Migrations and Pool Management](references/migrations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown review findings with file-line anchors and severity labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires concrete inspected paths and line references before assigning Critical or Major severity.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
