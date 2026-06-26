## Description: <br>
Provides production-grade guidance for designing, ingesting, and retrieving data in Qdrant-based RAG pipelines with best practices for chunking, metadata, access control, embedding model selection, and operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building, designing, or debugging Qdrant-backed RAG systems. It helps them choose ingestion order, metadata schemas, chunking strategy, embedding models, hybrid retrieval patterns, access control filters, and operational checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code snippets and operational patterns may be copied into production without adapting access-control, deletion, and upsert behavior to the target system. <br>
Mitigation: Review the generated implementation details against local data governance, Qdrant collection design, and deletion/upsert requirements before deployment. <br>
Risk: Raw query or retrieval logging can expose sensitive content or user intent. <br>
Mitigation: Use privacy-preserving telemetry and avoid retaining raw queries, payloads, or retrieved sensitive text unless explicitly approved. <br>
Risk: The documented duplicate-chunk metadata refresh behavior may require correction before production use. <br>
Mitigation: Validate duplicate-chunk handling in conformance tests and ensure metadata refreshes are idempotent before enabling ingestion at scale. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/encryptshawn/qdrant-ingestion-best-practices) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Quick Reference](artifact/QUICK_REFERENCE.md) <br>
- [RAG Pipeline Overview](artifact/guides/01-rag-pipeline-overview.md) <br>
- [Metadata Schema Standards](artifact/guides/02-metadata-schema.md) <br>
- [Ingestion Pipeline](artifact/guides/07-ingestion-pipeline.md) <br>
- [Retrieval Architecture](artifact/guides/08-retrieval-architecture.md) <br>
- [Access Control Patterns](artifact/guides/09-access-control.md) <br>
- [Operational Standards](artifact/guides/10-operational-standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code examples and configuration patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; code snippets should be reviewed and adapted before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
