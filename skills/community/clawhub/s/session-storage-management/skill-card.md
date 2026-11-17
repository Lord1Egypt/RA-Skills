## Description:

Analyze and clean up OpenClaw session storage files. Use when the user wants to manage session files, clean up old sessions, delete cron/heartbeat, or organize session storage. Triggers on phrases like "clean up sessions", "delete old sessions", "manage session storage", "remove cron sessions", "session cleanup".

This skill is ready for commercial/non-commercial use.

## Publisher:

[denq04](https://clawhub.ai/user/denq04)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to review, categorize, and clean up local session storage while preserving the current active session unless separately confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan stored conversation content, which may include secrets or sensitive personal information.

Mitigation: Use it for targeted cleanup and avoid detailed descriptions when session history may contain sensitive content.

Risk: The skill can delete selected session files after confirmation.

Mitigation: Review deletion lists carefully, protect the current session, and confirm deletion only for intended categories or files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/denq04/skills/session-storage-management)
- [Publisher Profile](https://clawhub.ai/user/denq04)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries, deletion plans, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deletion actions require explicit user confirmation, and the skill reports affected files and estimated disk space freed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
