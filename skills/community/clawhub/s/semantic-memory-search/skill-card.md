## Description:

Adds vector-driven semantic search for OpenClaw Markdown memory files using memsearch with hybrid dense-vector and BM25 retrieval, SHA-256 deduplication, and local embeddings without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to index local Markdown memory files and retrieve semantically related memory snippets with memsearch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can index private OpenClaw memory content, and documented Discord reporting conflicts with the offline privacy claim.

Mitigation: Review configuration before enabling integrations, confirm exactly what is sent externally, and disable or audit Discord reporting before use.

Risk: Installing or running memsearch without version controls can change retrieval behavior or dependency exposure over time.

Mitigation: Install in an isolated environment with pinned versions and review the generated index location before indexing sensitive files.

## Reference(s):

- [Semantic Memory Search on ClawHub](https://clawhub.ai/sunnyhot/skills/semantic-memory-search)
- [memsearch GitHub](https://github.com/zilliztech/memsearch)
- [memsearch Documentation](https://zilliztech.github.io/memsearch/)
- [Milvus](https://milvus.io/)
- [Semantic Memory Search Use Case](https://github.com/AlexAnys/awesome-openclaw-usecases-zh/blob/main/usecases/semantic-memory-search.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on local memory files, the memsearch installation, and configured top_k.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
