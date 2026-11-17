## Description:

Reviews SQLAlchemy code for session management, relationships, N+1 queries, and migration patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review SQLAlchemy 2.0 code for session lifecycle issues, relationship loading problems, query anti-patterns, and Alembic migration risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to recommend database or migration changes that affect production behavior.

Mitigation: Review proposed code edits before applying them to production systems and test query or migration changes in CI or staging.

Risk: SQLAlchemy review findings can be overstated if they are not tied to concrete source evidence.

Mitigation: Use the skill's gates to anchor each finding to file:line evidence, then withdraw, downgrade, or rephrase unsupported claims.

## Reference(s):

- [Sessions](references/sessions.md)
- [Relationships](references/relationships.md)
- [Queries](references/queries.md)
- [Migrations](references/migrations.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown review findings with file:line citations and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should be anchored to repository evidence before being asserted.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
