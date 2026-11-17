## Description:

Build database schemas with SQL generation and relationship modeling. Use when designing databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Schema Builder to design database tables, model relationships, and generate SQL, migrations, seed data, schema comparisons, and related guidance for application databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL, migrations, and schema comparison output may be unsafe or unsuitable for staging or production databases.

Mitigation: Review all generated database changes manually, test them in an isolated development environment, and apply normal migration, backup, and rollback controls before deployment.

Risk: Generated seed data can include hardcoded administrator-style credentials or privileged roles.

Mitigation: Do not import generated seed credentials into staging or production; replace credentials, emails, and roles with approved test data before use.

Risk: The security evidence flags the skill as suspicious because richer generator behavior is under-disclosed.

Mitigation: Review the skill before installation and limit execution to trusted workspaces until the generated database artifacts have been validated.

## Reference(s):

- [Schema Builder on ClawHub](https://clawhub.ai/ckchzh/skills/schema-builder)
- [BytesAgain](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with shell commands, SQL snippets, JSON schema examples, and ASCII diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SQL, migration snippets, seed data, ER diagrams, optimization notes, and MongoDB schema JSON.]

## Skill Version(s):

3.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
