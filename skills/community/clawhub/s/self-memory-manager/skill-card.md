## Description:

Helps an agent manage conversational context, archive important task information, create daily summaries, and maintain a local work folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyk234](https://clawhub.ai/user/hyk234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to monitor context pressure, decide when to archive work, and retrieve concise local task memory across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived local memory files can retain sensitive account, API, or project information beyond the current session.

Mitigation: Archive only redacted task summaries, avoid credentials and account details, and require explicit user confirmation before writing to or recalling from the archive.

Risk: The skill text includes a command to copy an OpenClaw configuration file into the archive folder.

Mitigation: Do not copy raw configuration files; extract only non-sensitive notes after checking that tokens, API keys, and account identifiers are absent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyk234/skills/self-memory-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/hyk234)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with local file paths and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local long-lived memory notes when the user approves archival behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
