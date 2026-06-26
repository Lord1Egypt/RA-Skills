## Description: <br>
RAG Retriever V3 provides document retrieval with local or OpenAI embeddings, hybrid vector and BM25 search, cross-encoder reranking, and source citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to index documents, retrieve relevant passages, and prepare cited RAG context for downstream answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document chunks and search queries may be sent to OpenAI when OpenAI is configured or OPENAI_API_KEY is present. <br>
Mitigation: Use the Xenova/local embedding provider for private documents and avoid exposing OPENAI_API_KEY in the runtime environment. <br>
Risk: The skill can download local model files and create local LanceDB collections during normal operation. <br>
Mitigation: Run it in an approved workspace with controlled storage and review generated data directories before sharing or publishing artifacts. <br>
Risk: Collection deletion paths can remove indexed data. <br>
Mitigation: Restrict access to code paths or wrappers that call collection drop operations and keep backups of important indexes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown and CLI/API text output with cited retrieval results and RAG context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local LanceDB collections and model cache files during use.] <br>

## Skill Version(s): <br>
3.0.0 (source: release metadata and package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
