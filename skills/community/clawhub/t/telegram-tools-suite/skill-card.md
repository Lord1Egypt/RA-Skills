## Description:

Telegram Tools Suite provides Telegram account automation for group monitoring, group search, batch group joining, scheduled messages, and account queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[testman2025](https://clawhub.ai/user/testman2025)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run Telegram automation workflows for monitoring selected groups, searching groups by keyword, querying account or group data, joining groups from a list, and sending scheduled messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Telegram session credentials can expose the connected account if the workspace is shared, archived, or published.

Mitigation: Use a test account, keep the workspace private, exclude userdata and .env files from archives, and review session-file permissions after login.

Risk: Scheduled sending and bulk group joining can risk account enforcement or misuse.

Mitigation: Keep high-risk operations disabled unless needed, explicitly enable them only for reviewed tasks, and verify target lists, message content, and frequency before execution.

## Reference(s):

- [Telegram API development tools](https://my.telegram.org)
- [ClawHub skill page](https://clawhub.ai/testman2025/skills/telegram-tools-suite)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce operational guidance for long-running Telegram commands and local configuration files.]

## Skill Version(s):

1.3.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
