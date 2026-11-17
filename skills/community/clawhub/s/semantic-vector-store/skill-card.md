## Description:

Provides text embedding, persistent vector storage, and cosine-similarity semantic search with incremental indexing and multiple backend adapters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whoisme007](https://clawhub.ai/user/whoisme007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add semantic memory retrieval to agent systems by embedding text, storing vectors, and searching memories by similarity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted FAISS sidecar files or vector database contents can trigger unsafe pickle loading if modified by an untrusted user or process.

Mitigation: Use only trusted local vector-store files, restrict file permissions, and replace pickle persistence with a safe serialization format before broad deployment.

Risk: Sensitive memory text may be exposed if embeddings are generated with a remote model or service.

Mitigation: Confirm whether embeddings are local or remote before storing sensitive memories, and avoid sending regulated or confidential content to unapproved services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whoisme007/skills/semantic-vector-store)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe or use local SQLite and FAISS vector-store files, embedding model configuration, and semantic search results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
