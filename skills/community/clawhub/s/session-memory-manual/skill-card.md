## Description:

Provides manual, user-triggered search and synchronization of memories, decisions, and TODOs across OpenClaw sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoquan](https://clawhub.ai/user/guoquan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill when they explicitly ask an agent to find prior-session decisions, TODOs, or memory entries and optionally synchronize selected findings into shared memory after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private prior-session history and shared memory.

Mitigation: Use explicit session IDs, narrow date ranges, and minimal message limits; review target content before allowing tool-history reads or memory synchronization.

Risk: Shell-based search examples can be unsafe if untrusted search text is inserted directly.

Mitigation: Avoid shell search with untrusted text; quote inputs safely or use native session and memory search tools when available.

Risk: Memory synchronization can persist sensitive information across sessions.

Mitigation: Show extracted findings to the user, redact secrets and private content, and write shared memory only after explicit confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoquan/skills/session-memory-manual)
- [ClawHub publisher profile](https://clawhub.ai/user/guoquan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples and structured search summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session identifiers, file paths, and proposed memory updates for user confirmation.]

## Skill Version(s):

0.5.6 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
