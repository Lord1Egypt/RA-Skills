## Description:

Smart Memory Plus gives OpenClaw agents a local memory system with WAL-backed session state, conversation compaction, type classification, temporal decay, BM25 search, and a SQLite memory graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgjq](https://clawhub.ai/user/zgjq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to persist conversation-derived facts, summarize long sessions, search prior memory, track task state, and maintain local memory hygiene.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists conversation-derived facts and task context locally, which can retain sensitive or stale information if used on shared machines or sensitive workspaces.

Mitigation: Use it only in trusted workspaces, avoid storing credentials or private third-party information, and periodically review the generated memory files and archives.

Risk: Server security evidence reports that several scripts can write, move, restore, or expose files outside the intended scope.

Mitigation: Review or patch the temporary cache handling, health-report filename handling, restore path containment, classify file writes, and archive destination controls before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zgjq/skills/smart-memory-plus)
- [Extraction prompt template](references/extraction_prompt.md)
- [Compaction prompt template](references/compaction_prompt.md)
- [Decay and archival rules](references/decay_rules.md)
- [Memory schema reference](references/memory_schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python commands plus local file outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory artifacts such as MEMORY.md, daily notes, session state, compacts, JSON cache/index files, and a SQLite graph database.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
