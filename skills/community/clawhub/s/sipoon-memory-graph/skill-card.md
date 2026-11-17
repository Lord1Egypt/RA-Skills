## Description:

SQLite-based entity-relationship graph storage that provides add_entity, add_relation, query, traverse, get_path, and stats operations for agent memory workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipoon](https://clawhub.ai/user/sipoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to persist and query an entity-relationship knowledge graph for agent memory, including entities, weighted relationships, graph traversal, path lookup, and graph statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The module persistently writes graph data to a hard-coded, user-specific database path on import.

Mitigation: Review and modify the skill to use a documented, configurable, skill-owned database path, and initialize storage only when explicitly invoked.

Risk: Stored graph contents act as persistent memory and may retain sensitive personal, credential, or private project data.

Mitigation: Avoid storing sensitive data unless the storage location, access controls, and retention behavior are acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sipoon/skills/sipoon-memory-graph)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python API examples and structured graph operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance and code-oriented outputs for creating, querying, traversing, and inspecting a local SQLite knowledge graph.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
