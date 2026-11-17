## Description:

Applies pending database migration files against the target database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to apply schema migration or index-maintenance recommendations in deployment and maintenance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly drop database indexes based on a local recommendation file, and the release security summary says the headline understates this destructive behavior.

Mitigation: Review the recommendation file, intended index deletions, backups, rollback plan, and target database before running the skill.

Risk: Using the skill as a general migration runner without added controls could apply unwanted schema changes.

Mitigation: Add confirmation, change review, and rollback controls before using it in automated deployment workflows.

## Reference(s):

- [Schema Migrator ClawHub page](https://clawhub.ai/ink5725/skills/schema-migrator)
- [Publisher profile](https://clawhub.ai/user/ink5725)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON execution reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe database migration actions, index cleanup results, errors, and completion status.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
