## Description: <br>
Backend retrieval skill for querying a local vector knowledge base of occupational health regulations and returning original text with source details and relevance scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Loda666](https://clawhub.ai/user/Loda666) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this backend retrieval component to fetch relevant source passages from an occupational health knowledge base for downstream QA or report-writing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on unreviewed local rag_system code and a local vector database path. <br>
Mitigation: Install only in environments where you control and have reviewed the local rag_system directory, especially search_pipeline.py and embedding_client.py. <br>
Risk: The query processing path is not clearly disclosed and may involve Qwen embedding or rerank clients. <br>
Mitigation: Confirm whether embedding or rerank calls leave the machine before sending sensitive queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Loda666/rag-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Structured search results] <br>
**Output Format:** [JSON object containing retrieved passages, source metadata, relevance scores, query echo, result count, method, and error field] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns original retrieved text without summarizing, rewriting, or reasoning over the content.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact skill.yaml lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
