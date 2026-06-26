## Description: <br>
Rag Retriever provides a RAG retrieval system with document chunking, vector and keyword search, source citations, context assembly, and Chinese tokenization support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to index local documents, retrieve relevant chunks, and produce cited RAG context or prompts for downstream language model workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexed documents and embedding caches are stored locally. <br>
Mitigation: Use the skill only with files approved for local indexing and clear local LanceDB or cache directories when material should no longer be retained. <br>
Risk: Optional OpenAI embeddings can send document chunks and queries to OpenAI. <br>
Mitigation: Use local/simple or local Transformers embedding modes for private material, and enable OpenAI embeddings only when external processing is acceptable. <br>
Risk: Transformers mode may download model files from hf-mirror.com. <br>
Mitigation: Review or change the model endpoint before use in environments with restricted network or model-source requirements. <br>
Risk: Retrieval quality depends on the embedding provider, tokenizer, chunking, and available indexed content. <br>
Mitigation: Evaluate results on representative documents and review cited context before using retrieved content in downstream answers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/rag-retriever) <br>
- [LanceDB Documentation](https://lancedb.github.io/lancedb/) <br>
- [Jieba Tokenizer](https://github.com/napi-rs/jieba) <br>
- [Transformers.js](https://huggingface.co/blog/transformersjs-v4) <br>
- [Xenova all-MiniLM-L6-v2](https://huggingface.co/Xenova/all-MiniLM-L6-v2) <br>
- [Cross-Encoder Reranking](https://sbert.net/examples/cross_encoder/applications/README.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, JSON-like configuration, retrieval results, citations, and RAG prompt text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local files, persist local indexes and embedding caches, and optionally call OpenAI embeddings or download Transformers model files when those providers are enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
