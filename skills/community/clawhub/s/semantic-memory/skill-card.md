## Description:

Semantic Memory provides a Chinese-first long-term memory retrieval system for OpenClaw agents using jieba TF-IDF, ChromaDB vector search, keyword boosting, and collection routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackxc2026](https://clawhub.ai/user/jackxc2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to import Markdown memory files into ChromaDB and retrieve relevant Chinese-language memories across routed collections. It is intended for OpenClaw agent memory workflows that need hybrid semantic, lexical, and keyword search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled ChromaDB startup path can expose the database beyond localhost when bound to 0.0.0.0.

Mitigation: Bind ChromaDB to 127.0.0.1 for local use; add authentication, firewall rules, and TLS before any non-local deployment.

Risk: TF-IDF cache files use pickle and can be unsafe if loaded from shared or untrusted directories.

Mitigation: Keep TFIDF_CACHE in a trusted local directory and remove existing .pkl cache files before running in a new or untrusted environment.

Risk: Imported Markdown contents and absolute file paths are stored in the memory database.

Mitigation: Import only files approved for storage and retrieval, and review memory directories for sensitive content before ingestion.

## Reference(s):

- [Semantic Memory Skill Page](https://clawhub.ai/jackxc2026/skills/semantic-memory)
- [ChromaDB](https://www.trychroma.com/)
- [Python](https://www.python.org/)
- [artifact/README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python APIs, shell commands, and search result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search returns ranked top-k memory results with source, agent, collection, vector similarity, TF-IDF similarity, and combined score.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
