## Description:

Rag Retriever provides a JavaScript RAG retrieval system with document chunking, local or API-based embeddings, LanceDB vector storage, BM25/vector hybrid search, Chinese tokenization, and citation-aware context generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to index local documents or code, retrieve relevant passages across English and Chinese corpora, and prepare source-linked context for RAG answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexed corpora can contain secrets, credentials, personal data, or proprietary text that may be stored locally or embedded.

Mitigation: Review source documents before ingestion, avoid sensitive corpora unless storage and embedding paths are approved, and remove local indexes and caches when they are no longer needed.

Risk: Optional external embedding/model sources can introduce data-transfer and supply-chain risk.

Mitigation: Use the local/simple embedding path for sensitive data, require explicit approval before enabling OpenAI embeddings, and pin and verify model artifacts before use.

Risk: The hardcoded Hugging Face mirror can fetch model artifacts from an under-disclosed endpoint.

Mitigation: Make the mirror opt-in or replace it with an approved model source, and document the endpoint used for model downloads.

Risk: Retrieved document text can contain prompt-injection content.

Mitigation: Treat retrieved passages as untrusted evidence with citations, not as instructions for the agent to follow.

Risk: Vulnerable transitive dependencies can affect runtime security.

Mitigation: Update vulnerable dependencies and re-run dependency and security checks before deploying in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/rag-retriever)
- [LanceDB Documentation](https://lancedb.github.io/lancedb/)
- [Transformers.js](https://huggingface.co/blog/transformersjs-v4)
- [Xenova all-MiniLM-L6-v2](https://huggingface.co/Xenova/all-MiniLM-L6-v2)
- [jieba Tokenizer](https://github.com/napi-rs/jieba)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text retrieval context with source citations, plus JavaScript API examples and CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist indexed content, vector data, vocabulary files, and embedding caches under configured local data paths.]

## Skill Version(s):

0.1.0 (source: server release metadata, target metadata, and package.json; artifact/SKILL.md lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
