## Description:

Lints .sql migration files for missing idempotency guards, unsafe DML or DDL, transaction issues, reserved-word identifiers, and dialect-specific migration risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to lint SQL migration files before pull request, pre-commit, or CI release checks. It supports generic, Postgres, MySQL, and SQLite migration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The linter reads SQL files under the paths passed to it, including nested .sql files when a directory is provided.

Mitigation: Pass explicit files or scoped migration directories, and avoid broad directories unless recursive inspection is intended.

Risk: Regex-based SQL linting can miss or misclassify complex migration behavior because it is not a full SQL parser and has no schema knowledge.

Mitigation: Treat findings as review aids and keep human review, database-specific validation, and migration testing in place for complex changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/sql-migration-linter)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text, JSON, or summary text with CI-oriented exit codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads .sql files from user-provided files or directories; supports generic, postgres, mysql, and sqlite dialect options.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
