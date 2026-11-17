## Description:

Long-term memory management system for OpenClaw agents that archives conversations, organizes memories, and provides memory search capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiucheng](https://clawhub.ai/user/xiucheng)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw agent operators use this skill to persist conversation history, maintain curated long-term notes, and retrieve prior memory entries during later agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists conversations and selected insights locally, which may retain secrets, regulated data, or other sensitive content.

Mitigation: Avoid saving sensitive data, periodically review and delete memory files, and install the skill only when local persistence is intended.

Risk: Retrieved memories may contain stale or untrusted historical content.

Mitigation: Treat retrieved memory as context for review rather than authoritative instructions.

## Reference(s):

- [Memory Manager ClawHub page](https://clawhub.ai/xiucheng/skills/xiucheng-memory-manager)
- [Memory Manager homepage](https://github.com/xiucheng/memory-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown memory files, Python API results, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily Markdown memory files and a long-term MEMORY.md file in the configured OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
