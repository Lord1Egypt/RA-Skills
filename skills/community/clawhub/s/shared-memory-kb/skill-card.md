## Description:

A shared memory knowledge-base skill for OpenClaw agents that stores, retrieves, browses, links, and reviews personal knowledge across agent personas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ludiansheng](https://clawhub.ai/user/ludiansheng)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and their agents use this skill to maintain a persistent personal knowledge base across work, learning, personal, and general-purpose personas. It supports storing reusable insights, retrieving past experience, browsing taxonomy-based memory structure, linking related memories, and generating periodic review data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and retrieve personal memories across agent personas, including sensitive work, health, family, or personal details.

Mitigation: Require explicit confirmation before storing memories, avoid sensitive details unless intentional, and tune automatic write sensitivity before regular use.

Risk: Persistent local memory files may expose personal knowledge if stored in a shared or weakly protected location.

Mitigation: Store the knowledge base in a private local directory with restrictive permissions and set MEMORY_KB_PATH only to trusted storage.

Risk: Cross-persona retrieval may surface information outside the context where it was originally recorded.

Mitigation: Use persona filters for retrieval and separate storage paths when stronger isolation between identities or contexts is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ludiansheng/skills/shared-memory-kb)
- [Data Model](artifact/references/DATA_MODEL.md)
- [Taxonomy](artifact/references/TAXONOMY.md)
- [Configuration](artifact/references/CONFIG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSONL memory files and JSON index files under the configured memory directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
