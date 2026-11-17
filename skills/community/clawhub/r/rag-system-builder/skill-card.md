## Description:

Build and deploy local RAG (Retrieval-Augmented Generation) systems with offline document processing, embedding models, and vector storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexfeng75](https://clawhub.ai/user/alexfeng75)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scaffold a local retrieval-augmented generation system for document ingestion, embedding generation, FAISS vector storage, semantic search, and CLI or web-based document Q&A.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's offline claims are overstated because model download and runtime fallback behavior can contact Hugging Face.

Mitigation: Pin model revisions, download models through a trusted path, and remove runtime remote fallback when true offline operation is required.

Risk: Generated vector indexes and metadata may persist document text or sensitive source material.

Mitigation: Store indexes in protected directories and avoid ingesting sensitive documents unless retention and access controls are acceptable.

Risk: The Flask example runs with debug mode enabled and should not be exposed as-is.

Mitigation: Disable debug mode and apply normal production web-server controls before exposing any web interface.

## Reference(s):

- [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance and starter code for local document ingestion, embedding, vector indexing, retrieval, and optional Flask serving.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
