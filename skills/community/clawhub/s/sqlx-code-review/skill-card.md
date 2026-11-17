## Description:

Reviews Rust sqlx database code for compile-time query checking, connection pool management, migration safety, type mapping, and PostgreSQL-specific usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to review Rust projects that use sqlx for query safety, connection pooling, migrations, transaction handling, and PostgreSQL type mapping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separate unbundled review-verification-protocol skill that was not included in the reviewed package.

Mitigation: Review and vendor the referenced protocol, or otherwise control its content and integrity, before installation.

## Reference(s):

- [Migrations and Pool Management](references/migrations.md)
- [Queries](references/queries.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown review findings with file-line anchors and severity labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are gated by inspected evidence and reported with Critical, Major, Minor, or Informational severity when issues are present.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
