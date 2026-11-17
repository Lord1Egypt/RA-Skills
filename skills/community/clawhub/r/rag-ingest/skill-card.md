## Description:

Ingests agent-prepared document text into a Qdrant knowledge base by chunking content, generating embeddings, and writing vectors; it does not fetch or refine source content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seal-re](https://clawhub.ai/user/seal-re)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to persist already-processed document text into Qdrant for later retrieval. It is intended for RAG knowledge-base ingestion after upstream tools have handled fetching, extraction, and summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document chunks and embedding credentials may be sent to the configured embedding service, and defaults can route OPENAI_API_KEY to a non-OpenAI endpoint.

Mitigation: Use dedicated low-privilege embedding keys, explicitly set EMBED_BASE_URL with the matching key, avoid unrelated OPENAI_API_KEY values in the runtime environment, and ingest confidential data only when that storage and embedding flow is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seal-re/skills/rag-ingest)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command examples and parameter descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node plus QDRANT_URL and EMBED_API_KEY-compatible embedding credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
