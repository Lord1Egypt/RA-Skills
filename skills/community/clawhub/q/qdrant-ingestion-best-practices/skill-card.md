## Description:

Use this skill whenever building, designing, or debugging a RAG pipeline using Qdrant as the vector store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, implement, and review Qdrant-based RAG ingestion and retrieval pipelines. It provides guidance for chunking, metadata schema design, embedding selection, hybrid retrieval, payload filtering, access control, and operational standards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production snippets may weaken tenant isolation or access boundaries if copied without adaptation.

Mitigation: Require review before installation and add tenant-qualified IDs and filters, internally derived collection placement, and security-metadata change detection before production use.

Risk: Delete, retention, and migration examples can affect stored Qdrant chunks if adapted without safeguards.

Mitigation: Use explicit safeguards for delete and migration operations, privacy-aware audit logging, scoped filters, and a tested rollback or recovery path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/encryptshawn/skills/qdrant-ingestion-best-practices)
- [Quick Reference](QUICK_REFERENCE.md)
- [RAG Pipeline Overview](guides/01-rag-pipeline-overview.md)
- [Metadata Schema Standards](guides/02-metadata-schema.md)
- [Ingestion Pipeline](guides/07-ingestion-pipeline.md)
- [Retrieval Architecture](guides/08-retrieval-architecture.md)
- [Access Control Patterns](guides/09-access-control.md)
- [Operational Standards](guides/10-operational-standards.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code snippets, checklists, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; generated implementation snippets require review before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
