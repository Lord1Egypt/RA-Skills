## Description: <br>
Build and deploy local RAG (Retrieval-Augmented Generation) systems with offline document processing, embedding models, and vector storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexfeng75](https://clawhub.ai/user/alexfeng75) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build local RAG systems that ingest documents, generate embeddings, store vectors, and provide CLI or web-based document Q&A. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's offline privacy claims may not hold if model loading falls back to Hugging Face network access. <br>
Mitigation: Pre-seed the embedding model locally, disable or review remote fallback behavior, and verify network behavior before using private or regulated documents. <br>
Risk: The local vector-store directory may contain readable copies of ingested document text. <br>
Mitigation: Protect, encrypt, or delete the vector-store directory according to data sensitivity and avoid ingesting regulated documents without appropriate controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexfeng75/rag-system-builder) <br>
- [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes configurable chunk size, chunk overlap, top-k retrieval, local model path, and vector store path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
