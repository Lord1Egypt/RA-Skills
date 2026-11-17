## Description:

Create, list, and cancel channel-scoped reminders and cron jobs with automatic channel, chat, and timezone handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youpele52](https://clawhub.ai/user/youpele52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, inspect, and cancel reminders or recurring cron jobs from chat while preserving the originating channel and timezone context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cancellation by name or ID can remove reminders without verifying they belong to the current chat.

Mitigation: Require channel and chat ownership checks before cancellation, especially in shared or multi-chat OpenClaw environments.

Risk: Timezone preferences may be read from or saved to USER.md.

Mitigation: Disclose timezone handling to users and confirm before saving a new timezone preference.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/youpele52/skills/remind-me-pro)
- [Publisher Profile](https://clawhub.ai/user/youpele52)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces chat-facing reminder confirmations, reminder lists, cancellation results, and OpenClaw cron commands.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
