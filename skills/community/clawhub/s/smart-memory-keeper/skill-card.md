## Description:

Smart Memory Keeper helps OpenClaw agents preserve local task, journal, and project memory across sessions with three-tier loading and periodic consolidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porkapple](https://clawhub.ai/user/porkapple)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to restore task state, daily journals, and project indexes after session resets while loading only the memory tier needed for the current work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can retain stale or sensitive context if users allow too much information to be recorded.

Mitigation: Review the AGENTS.md and HEARTBEAT.md snippets before applying them, avoid storing secrets or personal data, and periodically inspect or delete memory files.

Risk: First-run initialization reads recent session history to bootstrap task state.

Mitigation: Require user confirmation before saving extracted tasks and skip the bootstrap when the user does not want recent session history summarized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/porkapple/skills/smart-memory-keeper)
- [Memory formats](references/formats.md)
- [Dream consolidation guide](references/dream-guide.md)
- [Install snippets](references/install-snippets.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-readable local memory files and startup or heartbeat configuration snippets; no external service is required.]

## Skill Version(s):

1.5.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
