## Description: <br>
Writes agent-prepared document text into Qdrant, performing chunking, embedding, and vector storage without fetching or refining source content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Seal-Re](https://clawhub.ai/user/Seal-Re) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to ingest already-processed text into a Qdrant-backed retrieval knowledge base. It is suited for RAG pipelines where fetching, extraction, and summarization are handled by other tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ingested text is sent to the configured embedding provider. <br>
Mitigation: Set EMBED_BASE_URL and EMBED_API_KEY explicitly, and use only an embedding provider approved for the document sensitivity. <br>
Risk: Ingested content is stored persistently in Qdrant and existing points for the same doc_id are deleted before upsert. <br>
Mitigation: Use unique doc_id values, maintain backups for important collections, and confirm the target collection before running ingestion. <br>
Risk: Credential fallback can use OPENAI_API_KEY when EMBED_API_KEY is absent. <br>
Mitigation: Prefer a dedicated EMBED_API_KEY for this skill and avoid relying on OPENAI_API_KEY unless the configured embedding endpoint is actually OpenAI. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Seal-Re/rag-ingest) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text CLI status output with persistent Qdrant vector records as the primary side effect.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node, QDRANT_URL, and EMBED_API_KEY; accepts document content through --content or stdin.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
