## Description: <br>
Deep RAG workflow covering document ingestion, chunking, metadata, retrieval and reranking, grounding and citations, evaluation, and common failure modes for retrieval-augmented generation systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codekungfu](https://clawhub.ai/user/codekungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building or debugging RAG systems for internal docs, support assistants, copilots, PDFs, HTML, or code repositories. It helps structure work across success criteria, ingestion, chunking, retrieval, grounding, evaluation, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RAG systems can expose or retrieve content beyond the intended audience if document sources and permissions are not defined. <br>
Mitigation: Define allowed document sources and enforce access-control filtering for retrieved content before generation. <br>
Risk: Embeddings, retrieved context, citations, logs, and audit records may retain sensitive information longer than intended. <br>
Mitigation: Set retention rules for embeddings, retrieved context, citations, logs, and audit records before production use. <br>
Risk: RAG answers may be misleading when retrieval is stale, citations are wrong, or the source is unavailable. <br>
Mitigation: Use explicit grounding, citation behavior, refusal behavior, offline evaluation, and production monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codekungfu/rag-pipelines) <br>
- [Publisher profile](https://clawhub.ai/user/codekungfu) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with checklists and implementation criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow recommendations, review checklist items, and RAG debugging guidance; it does not execute code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
