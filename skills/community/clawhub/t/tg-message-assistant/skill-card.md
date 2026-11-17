## Description:

Generate topic briefings from Telegram channels for briefings, newsletters, digests, message summaries, channel recaps, reports, scheduled pushes, and channel roundups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[telyclaw](https://clawhub.ai/user/telyclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to collect Telegram channel messages over a selected time range, turn them into structured briefings, and deliver them through Telegram or Gmail. It also supports recurring scheduled briefing generation when the user wants a regular digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access Telegram content, Gmail accounts, or browser sessions containing private messages and contacts.

Mitigation: Use dedicated low-privilege Telegram and email accounts where possible, restrict source channels and recipients, and review account permissions before enabling the workflow.

Risk: The skill can deliver messages or email and can create recurring scheduled briefings.

Mitigation: Require preview and explicit final approval before sending messages, sending email, or creating recurring tasks; periodically review active schedules.

Risk: Optional MCP or ClawHub dependencies can expand the agent's access to Telegram, Gmail, or scheduling tools.

Mitigation: Pin and review dependencies before use, avoid broad credentials, and disable unused integrations.

## Reference(s):

- [TelyClaw Skills Repository](https://github.com/TelyAgent/telyclaw-skills)
- [TelyClaw Gmail Plugin](https://github.com/TelyAgent/telyclaw-plugin-gmail)
- [Multi-platform Research](references/multi-platform-research.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefings with optional plain-text Telegram or email delivery and setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports digest, detailed, topical, and insights briefing templates; Telegram delivery may split long briefings into 4096-character segments.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
