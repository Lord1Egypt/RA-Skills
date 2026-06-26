## Description: <br>
Manage vector storage and similarity search using TOS Vectors service for embeddings, semantic search, RAG systems, and recommendation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jneless](https://clawhub.ai/user/jneless) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure TOS Vectors, manage vector buckets and indexes, insert embeddings, and query similar vectors for semantic search, RAG, recommendation, and image-search applications. <br>

### Deployment Geography for Use: <br>
China regions listed by the artifact: cn-beijing, cn-shanghai, and cn-guangzhou. <br>

## Known Risks and Mitigations: <br>
Risk: Volcengine credentials can grant access to vector buckets, indexes, and stored embeddings. <br>
Mitigation: Use least-privilege credentials scoped to a dedicated project or test environment before applying the workflows to production data. <br>
Risk: Delete operations can remove vectors, indexes, or buckets used by downstream search and RAG applications. <br>
Mitigation: Review delete examples before execution and keep backups for important vector data. <br>
Risk: RAG workflows may send retrieved content to external LLM providers. <br>
Mitigation: Avoid sharing sensitive retrieved content with external providers unless that data sharing is approved. <br>


## Reference(s): <br>
- [TOS Vectors Agent Skill README](README.md) <br>
- [TOS Vectors API Reference](REFERENCE.md) <br>
- [TOS Vectors Workflows](WORKFLOWS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes TOS VectorClient configuration patterns, workflow snippets, and example utility script usage.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
