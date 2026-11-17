## Description:

Voyage AI CLI helps agents use the vai CLI to generate embeddings, rerank search results, manage MongoDB Atlas vector search indexes, and run semantic search workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrlynn](https://clawhub.ai/user/mrlynn)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to generate embeddings, rerank results, store vectors in MongoDB Atlas, create vector search indexes, and run retrieval workflows through the Voyage AI CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents an unpinned global CLI install.

Mitigation: Install only if the voyageai-cli package and publisher are trusted, and prefer a pinned package version.

Risk: Embedding, reranking, storage, search, and ingest workflows can send text to external services.

Mitigation: Do not send private or sensitive text unless that external transfer is approved for the use case.

Risk: Atlas store, ingest, index create, and index delete commands can affect real databases and indexes.

Mitigation: Use least-privilege Atlas credentials, test in non-production environments, and review data-changing commands before execution.

## Reference(s):

- [Model Catalog](artifact/references/models.md)
- [Vector Search Patterns](artifact/references/vector-search.md)
- [MongoDB AI API](https://ai.mongodb.com/v1/)
- [ClawHub skill page](https://clawhub.ai/mrlynn/skills/voyageai-skill)
- [Publisher profile](https://clawhub.ai/user/mrlynn)
- [Publisher website](https://mlynn.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI commands, configuration notes, and JSON-oriented examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that call external embedding, reranking, and MongoDB Atlas services.]

## Skill Version(s):

1.4.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
