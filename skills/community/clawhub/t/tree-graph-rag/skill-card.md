## Description:

Guide for designing and implementing a PostgreSQL database that fuses PageIndex-style document trees with LightRAG-style entity-relationship anchors for hybrid RAG retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4444433333](https://clawhub.ai/user/h4444433333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design PostgreSQL schemas, ingestion flows, graph anchoring logic, and retrieval SQL for hybrid tree-graph RAG systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended database pattern can allow one workspace to overwrite another workspace's indexed content if used as-is.

Mitigation: Before shared or production use, add workspace-scoped composite keys and foreign keys, and ensure upserts check workspace ownership.

Risk: Answer synthesis may receive retrieved document content that should not be trusted as instructions.

Mitigation: Treat retrieved content as untrusted context in prompts and apply application-level filtering, escaping, and review before synthesis.

## Reference(s):

- [Integration Pattern](references/integration-pattern.md)
- [Common Query Patterns](references/queries.md)
- [PostgreSQL Schema](references/schema.sql)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with SQL and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PostgreSQL DDL, ingestion code, retrieval SQL, and concise design rationale.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
