## Description:

Session Sync helps agents keep memory and task state consistent across Feishu, webchat, and other sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdt328606](https://clawhub.ai/user/sdt328606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to synchronize recent context, active tasks, decisions, and durable memory across multiple conversation channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-session memory sharing can expose conversation history or task state outside the intended audience.

Mitigation: Install only where all shared sessions and memory files belong to the same trusted user or team, with authorization-enforced access.

Risk: Broad memory writes can persist sensitive or unnecessary conversation-derived state.

Mitigation: Review, redact, and scope memory writes before using the skill for sensitive conversations.

Risk: The cleanup script moves dated memory logs into an archive directory, which may change where retained conversation records are stored.

Mitigation: Confirm the workspace path and retention expectations before running cleanup, and ensure valuable content has already been consolidated intentionally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdt328606/skills/session-memory-sync)
- [Publisher profile](https://clawhub.ai/user/sdt328606)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to read and write shared memory files and optionally run a cleanup script.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
