## Description:

Analyze differences between knowledge graph schema versions and generate migration plans and scripts for safe schema evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge graph engineers use this skill to compare RDF, OWL, or property graph schema versions, classify entity, property, relationship, and constraint changes, and draft migration plans and scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or copied migration commands may modify or remove graph data if run without review.

Mitigation: Treat migration commands as drafts, test them on staging data, back up production data, verify counts and relationships, and require explicit review and rollback planning before running REMOVE, DELETE, or DROP steps.

Risk: Schema diff output can miss domain-specific data constraints or relationship semantics.

Mitigation: Validate the proposed changes against the source and target schemas, review affected entity and relationship counts, and adapt the migration plan before execution.

## Reference(s):

- [Migration Patterns](references/migration-patterns.md)
- [Schema Migration Examples](examples/example-migrations.md)
- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/schema-migration-diff)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with Cypher, SPARQL, or Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft schema diff reports, migration plans, risk assessments, and executable migration examples that require review before use.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
