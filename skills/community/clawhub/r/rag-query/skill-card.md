## Description:

Query the RAG knowledge base (Qdrant kb_main) by semantic search. Returns top-k chunks with text, doc_id, source, text_type, topic_tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seal-re](https://clawhub.ai/user/seal-re)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to retrieve semantically relevant chunks from a Qdrant RAG knowledge base and inject the returned JSON results into an agent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries and embedding credentials may be sent to an external embedding service.

Mitigation: Explicitly set EMBED_BASE_URL to an approved provider and use a dedicated embedding credential.

Risk: The skill can fall back to OPENAI_API_KEY when a dedicated embedding credential is not provided.

Mitigation: Set EMBED_API_KEY or VECTORENGINE_API_KEY for this skill and avoid relying on OPENAI_API_KEY fallback.

Risk: Sensitive internal queries may leave the approved environment through the embedding provider or Qdrant endpoint.

Mitigation: Do not submit sensitive queries unless both the embedding provider and Qdrant endpoint are approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seal-re/skills/rag-query)
- [Publisher profile](https://clawhub.ai/user/seal-re)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON array returned by a Node command, with setup and usage guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns top-k chunks with text, doc_id, source, text_type, and topic_tags fields.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
