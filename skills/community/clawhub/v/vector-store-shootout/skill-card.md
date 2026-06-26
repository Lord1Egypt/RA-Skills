## Description: <br>
8 vector store implementations behind a common interface: numpy, lancedb, qdrant, pgvector, weaviate, weaviate_hybrid, milvus, and lightrag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to compare vector store backends for RAG, vector search, and embedding-store evaluation through a shared Python interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document text may be sent to embedding services when OpenAI fallback keys are configured or when local embedding endpoints are pointed at non-local deployments. <br>
Mitigation: Leave OpenAI keys unset for local-only use, configure Ollama and backend URLs deliberately, and verify data-flow behavior before indexing sensitive corpora. <br>
Risk: Cleanup methods can delete tables or collections when custom database, table, or collection names are supplied. <br>
Mitigation: Use isolated test databases or UUID-generated default names, and review custom names before calling cleanup methods. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nissan/vector-store-shootout) <br>
- [Publisher profile](https://clawhub.ai/user/nissan) <br>
- [LanceDB documentation](https://lancedb.github.io/lancedb/) <br>
- [pgvector project](https://github.com/pgvector/pgvector) <br>
- [Milvus documentation](https://milvus.io/docs) <br>
- [Weaviate documentation](https://weaviate.io/developers/weaviate) <br>
- [OpenAI embeddings API](https://api.openai.com/v1/embeddings) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Guidance, Configuration] <br>
**Output Format:** [Python source files and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides interchangeable vector store implementations with add, query, cleanup, and backend-identification behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
