## Description:

SharpAgent Layered Memory System provides a six-layer memory hierarchy with dream processing, TF-IDF semantic search, and Chinese tokenization support for agent memory retrieval and retention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to design layered persistent memory, retrieval, consolidation, archiving, and forgetting behavior for agents that need cross-session continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The memory design stores durable agent history across sessions, which may include sensitive or confidential content.

Mitigation: Require explicit user consent, avoid storing secrets or regulated data, and add review controls before committing items to long-term memory.

Risk: Archive entries are described as permanent and forget requests are handled as soft deletion, which may conflict with deletion or retention expectations.

Mitigation: Add hard-delete support, retention limits, and archive access controls before using this skill with regulated personal data or confidential business records.

Risk: Bulk history import can move data directly into the archive.

Mitigation: Validate imported content and apply retention, sensitivity, and access checks before archival ingestion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/sharpagent-memory-system)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with architecture diagrams, tables, and inline Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes memory layer definitions, storage layout guidance, search behavior, dream-processing rules, edge cases, and quality gates.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
