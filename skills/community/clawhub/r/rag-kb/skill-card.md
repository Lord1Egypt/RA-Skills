## Description: <br>
Maintains a local, directory-based knowledge base with FAISS, BM25, Alibaba Cloud Bailian text-embedding-v4 embeddings, and optional qwen3-rerank for indexing and querying OpenClaw-prepared text chunks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base operators use this skill to turn OpenClaw-extracted text, summaries, chunks, and T2Q files into local FAISS/BM25 indexes and query one or more knowledge bases with hybrid, semantic, or keyword retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Semantic indexing, semantic queries, hybrid queries, and reranking can send source text, query text, or candidate passages to Alibaba Cloud Bailian. <br>
Mitigation: Use keyword retrieval for local-only querying when external transfer is not acceptable, and enable semantic or rerank modes only for content approved for Bailian processing. <br>
Risk: The skill reads a Bailian API key from BAILIAN_SK or the legacy BAILIAN-SK environment variable for embedding and rerank requests. <br>
Mitigation: Scope the Bailian key appropriately, rotate it if exposed, and avoid placing unrelated secrets in the skill runtime environment. <br>
Risk: The Python runtime depends on packages such as faiss-cpu, jieba, numpy, and requests. <br>
Mitigation: Pin and review dependencies in controlled or sensitive deployments, as recommended by the security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kadbbz/rag-kb) <br>
- [Publisher profile: kadbbz](https://clawhub.ai/user/kadbbz) <br>
- [Path and naming rules](artifact/references/layout.md) <br>
- [Content formatting rules](artifact/references/content-rules.md) <br>
- [Runtime notes](artifact/references/runtime-notes.md) <br>
- [Bailian embeddings endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings) <br>
- [Bailian rerank endpoint](https://dashscope.aliyuncs.com/compatible-api/v1/reranks) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and Markdown query results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Index operations persist local JSONL, FAISS, BM25, manifest, and configuration files; query results return real chunk content rather than generated T2Q questions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
