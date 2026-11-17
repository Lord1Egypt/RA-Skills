## Description:

Veritas Memory v4.2 provides a four-layer memory architecture with credential indexing, gap detection, deep history retrieval, and deployment verification for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moozechen](https://clawhub.ai/user/moozechen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to initialize and maintain an agent memory system that indexes current state, long-term memory, daily notes, corrections, and operational follow-up. It is intended to help agents recover context from prior sessions and verify work against conversation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to persist and locate secrets across credential indexes, environment files, systemd configuration, and encrypted files without clear approval gates.

Mitigation: Require explicit approval for each secret read or write, redact secret values from memory files and logs, and define retention and deletion rules before use.

Risk: The skill encourages transcript-wide history search, which can expose unrelated private conversation content.

Mitigation: Limit searches to the minimum necessary scope, require user approval for broad transcript searches, and summarize only relevant findings without copying sensitive context.

Risk: The skill includes deployment and service-restart instructions that could change running systems.

Mitigation: Require explicit approval before server changes, show planned commands first, and verify the target environment and rollback path before execution.

## Reference(s):

- [Memory Tender](references/memory-tender.md)
- [STATE.md Format Specification](references/state-format.md)
- [Bidirectional Verification Protocol](references/verification-loop.md)
- [Write-Ahead Log Protocol](references/wal-protocol.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell scripts and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local memory files such as STATE.md, MEMORY.md, daily notes, and memory subdirectories when its scripts are run.]

## Skill Version(s):

4.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
