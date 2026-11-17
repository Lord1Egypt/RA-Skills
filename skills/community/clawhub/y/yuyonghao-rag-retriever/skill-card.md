## Description:

Rag Retriever helps agents build and query a retrieval-augmented generation index with document chunking, vector and BM25 search, Chinese tokenization, source citations, and RAG-ready context output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to index local documents or code and retrieve relevant passages for RAG prompts. It is suited to multilingual knowledge bases that need Chinese and English search, source attribution, and configurable local or API-based embeddings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexed documents, embeddings, vocabulary files, and model caches may persist locally.

Mitigation: Use local-only embeddings for sensitive documents where possible, choose cache paths deliberately, and clear local indexes or caches when they are no longer needed.

Risk: OpenAI embedding mode sends configured text to OpenAI.

Mitigation: Avoid API-based embeddings for sensitive documents unless the text has been reviewed, redacted as needed, and approved for that service.

Risk: Optional transformer model downloads and locked dependencies introduce supply-chain exposure.

Mitigation: Pin or review model sources before enabling the download path and update the locked dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-rag-retriever)
- [LanceDB documentation](https://lancedb.github.io/lancedb/)
- [jieba tokenizer](https://github.com/napi-rs/jieba)
- [Hugging Face all-MiniLM-L6-v2 model](https://huggingface.co/Xenova/all-MiniLM-L6-v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown and plain text with retrieved passages, source citations, and optional CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local LanceDB indexes, vocabulary files, model caches, and embedding caches depending on configuration.]

## Skill Version(s):

0.1.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
