## Description:

Vector memory search and RAG skill for OpenClaw that provides a Qdrant-backed vector_search tool and syncs Markdown and Postgres memory records through nomic-embed-text embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbojer](https://clawhub.ai/user/mbojer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to retrieve prior memory, daily logs, tool notes, and skill documentation through semantic vector search. It also supports keeping local Markdown files and Postgres memory records synchronized into Qdrant for later retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory contents can be sent to the configured embedding endpoint and stored or queried through Qdrant.

Mitigation: Use only trusted self-hosted endpoints, prefer HTTPS or loopback-only access, and scope credentials narrowly.

Risk: Automatic prompt injection can prepend retrieved memory into prompt context.

Mitigation: Disable auto_inject unless that behavior is intended, and enable it only when Qdrant data is trusted as prompt input.

Risk: The release advertises privileged background service deployment.

Mitigation: Review service deployment before using sudo, and run the sync process under a narrowly scoped account.

## Reference(s):

- [ClawHub Skill Homepage](https://clawhub.ai/mbojer/rag-memory)
- [ClawHub Skill Page](https://clawhub.ai/mbojer/skills/rag-memory)
- [Operational Guide](artifact/references/operational.md)
- [Config Paths Reference](artifact/references/config-paths.example.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with command examples; vector_search returns formatted text results with source metadata and scores.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [vector_search caps top_k at 10; automatic injected results are capped by configuration, with a default of 500 characters.]

## Skill Version(s):

1.1.1 (source: server release evidence, SKILL.md frontmatter, plugin/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
