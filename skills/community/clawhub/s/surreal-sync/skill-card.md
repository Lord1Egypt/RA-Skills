## Description:

Data migration and synchronization to SurrealDB from MongoDB, PostgreSQL, MySQL, Neo4j, Kafka, and JSONL. Full and incremental CDC sync. Part of the surreal-skills collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[24601](https://clawhub.ai/user/24601)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to plan and run database migrations or ongoing CDC synchronization into SurrealDB from supported sources such as PostgreSQL, MongoDB, MySQL, Neo4j, Kafka, and JSONL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact database synchronization or migration operations with weak operational guardrails.

Mitigation: Review plans before running them, test against non-production targets first, and use least-privileged database accounts.

Risk: Examples may place credentials directly in shell commands or connect to non-local SurrealDB endpoints without transport protections.

Mitigation: Avoid putting passwords directly in shell history and use TLS for non-local SurrealDB endpoints.

Risk: The security verdict for this release is suspicious.

Mitigation: Review before installing or using this skill in any real environment, and pin and verify the surreal-sync version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/24601/skills/surreal-sync)
- [Upstream repository reference](https://github.com/surrealdb/surreal-sync)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database migration commands and operational setup guidance.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
