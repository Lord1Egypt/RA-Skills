## Description:

Provides AI agents with persistent, file-based memory for cross-session recall and storage, with shared FACT entries and owner-isolated private memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use it to persist useful context between sessions, retrieve task-relevant memories, and keep private memory scoped to its owner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious and reports serious transport, credential, installer, memory, and filesystem risks; artifact analysis is incomplete.

Mitigation: Review the findings and setup before use; verify transport encryption, protect tokens, pin installer versions, and restrict memory and file access.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/yottameta/skills/yotta-memory)
- [Memory store protocol](artifact/references/protocol.md)
- [Provider protocol](artifact/references/provider-protocol.md)
- [FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions]

**Output Format:** [Plain text, Markdown, JSON, and CLI or MCP responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory results depend on the configured store, identity, and access scope.]

## Skill Version(s):

0.24.3 (source: release evidence, package.json, skill-manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
