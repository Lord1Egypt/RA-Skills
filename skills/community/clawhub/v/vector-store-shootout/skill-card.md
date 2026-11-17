## Description:

Provides eight interchangeable vector store implementations behind a common interface for evaluating RAG backends, building vector search, and comparing embedding stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to compare vector database backends and swap implementations behind a shared Python interface for RAG and vector search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive text may be shared with embedding or vector database services if deployments use remote Ollama, OpenAI, or managed database endpoints.

Mitigation: Use non-sensitive test data by default, and deliberately configure local embedding and vector database endpoints before indexing private corpora.

Risk: Unsafe PostgreSQL table handling could expose or delete data when pgvector table names are untrusted.

Mitigation: Do not pass untrusted pgvector table names, restrict database credentials, and review cleanup behavior before using shared databases.

Risk: Documented database credentials and anonymous-access settings are unsuitable for shared or networked deployments.

Mitigation: Change default database credentials and tighten or disable anonymous access before any shared or networked deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/vector-store-shootout)
- [Nissan Dookeran publisher profile](https://clawhub.ai/user/nissan)
- [LanceDB documentation](https://lancedb.github.io/lancedb/)
- [pgvector project](https://github.com/pgvector/pgvector)
- [Milvus documentation](https://milvus.io/docs)
- [Weaviate documentation](https://weaviate.io/developers/weaviate)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Python code and Markdown guidance with inline configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes interchangeable vector store classes and backend-specific setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
