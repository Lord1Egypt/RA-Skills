## Description: <br>
Rag Retriever provides a RAG document retrieval system with document chunking, local or remote embeddings, vector and keyword search, reranking, source citations, and Chinese tokenization support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to index documents or code, retrieve relevant passages, and produce citation-oriented RAG context for downstream language-model answers. It supports English and Chinese knowledge bases through configurable chunking, LanceDB-backed retrieval, BM25 search, and optional embedding providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexed documents and derived embeddings may store private material on disk. <br>
Mitigation: Use local storage paths only for material approved for indexing, restrict filesystem access to the index directory, and remove cached indexes when they are no longer needed. <br>
Risk: OpenAI embeddings send embedded text to a remote provider when that provider is selected. <br>
Mitigation: Use the simple or local Transformers.js embedding paths for private material, and select OpenAI embeddings only for text approved for external processing. <br>
Risk: Transformers.js model initialization can contact a Hugging Face mirror to fetch model artifacts. <br>
Mitigation: Preload model artifacts or disable remote model downloads in restricted and air-gapped environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/yuyonghao-rag-retriever) <br>
- [LanceDB Documentation](https://lancedb.github.io/lancedb/) <br>
- [Transformers.js](https://huggingface.co/blog/transformersjs-v4) <br>
- [Xenova/all-MiniLM-L6-v2 Model Card](https://huggingface.co/Xenova/all-MiniLM-L6-v2) <br>
- [jieba Tokenizer](https://github.com/napi-rs/jieba) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI/API examples with RAG context text and source citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces retrieved passages, scores, metadata, statistics, and formatted context suitable for a downstream LLM.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
