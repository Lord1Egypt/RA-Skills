## Description:

Build vector search with Weaviate using v4 syntax, proper module configuration, and production-ready patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate or review Weaviate vector search implementations that use current v4 client syntax, module configuration, batch import patterns, hybrid search, filtering, and HNSW tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-based vectorizer, generative, or reranker examples can send indexed or queried data to external providers.

Mitigation: Confirm the data is approved for the selected provider before use, and prefer local modules when external data transfer is not acceptable.

Risk: Incorrect or outdated Weaviate client syntax can lead to broken vector search code or misleading implementation guidance.

Mitigation: Use the documented v4 client patterns, context-managed connections, module checks, and batch error handling described in the artifact references.

## Reference(s):

- [Weaviate ClawHub Skill](https://clawhub.ai/ivangdavila/skills/weaviate)
- [v3 to v4 Migration Reference](artifact/v4-syntax.md)
- [Weaviate Module Configuration](artifact/modules.md)
- [Weaviate Operations Guide](artifact/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is scoped to Weaviate client v4 patterns and module configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
