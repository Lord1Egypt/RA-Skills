## Description: <br>
Vector memory search and RAG skill for OpenClaw. Provides vector_search tool backed by Qdrant, auto-syncs memory .md files and Postgres records via nomic-embed-text embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbojer](https://clawhub.ai/user/mbojer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to retrieve relevant prior memory, daily logs, and tool documentation through semantic vector search, and to keep local memory sources synchronized into Qdrant for RAG workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private prompts and stored memory content can be sent to configured embedding and vector services. <br>
Mitigation: Use only trusted or self-hosted embedding and Qdrant endpoints, and install the skill only when those services are approved for the memory data being indexed. <br>
Risk: Auto-inject can prepend memory search results to prompt context for sufficiently long user messages. <br>
Mitigation: Review the auto_inject setting before enabling the plugin and set it to false when automatic memory lookup is not desired. <br>
Risk: Syncing arbitrary files with --file can store their contents in the vector database. <br>
Mitigation: Use --file only for content intended to be embedded and retained in Qdrant. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mbojer/rag-memory) <br>
- [Operational Guide](references/operational.md) <br>
- [Config Paths Reference](references/config-paths.example.md) <br>
- [Example Memory Entry](examples/memory-entry.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown, including vector_search result summaries and operational shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include source metadata and relevance scores; auto-injected context is capped by configuration.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
