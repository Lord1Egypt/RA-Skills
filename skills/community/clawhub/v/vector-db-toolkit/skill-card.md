## Description:

Vector DB Toolkit helps agents and developers work with vector collections, embeddings, semantic search, and RAG retrieval across Qdrant, Chroma, and in-memory stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create vector collections, upsert embeddings and metadata, run similarity searches, filter results, and test retrieval workflows before integrating them into AI or RAG applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned dependencies can change runtime behavior over time.

Mitigation: Use a virtual environment and pin or lock dependencies before installing the toolkit.

Risk: Delete operations without IDs can remove an entire vector collection.

Mitigation: Test against non-production collections first and review delete calls before running them on production data.

Risk: The OpenAI embedding provider sends input text to an external service.

Mitigation: Use the OpenAI provider only for text that is approved for external processing, or choose local or fallback embeddings.

Risk: Qdrant and Chroma backends may use network services or persistent local storage.

Mitigation: Configure backend endpoints, API keys, and storage paths deliberately before connecting the skill to sensitive collections.

## Reference(s):

- [Vector DB Toolkit on ClawHub](https://clawhub.ai/kaiyuelv/skills/vector-db-toolkit)
- [Qdrant API Patterns](references/qdrant_api.md)
- [Chroma API Patterns](references/chroma_api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include vector database operation guidance, Python client usage, dependency setup, backend configuration, and retrieval workflow examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
