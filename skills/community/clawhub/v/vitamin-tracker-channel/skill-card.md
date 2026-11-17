## Description:

Manage vitamin and supplement reminders across configurable daily time slots with OpenClaw cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdmichaelb](https://clawhub.ai/user/cdmichaelb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a local supplement schedule and sync it into channel reminder cron jobs. It is suited for adding, removing, or rescheduling vitamin reminders in a configured OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the update script changes persistent OpenClaw cron state by removing existing vitamin reminder jobs and recreating them.

Mitigation: Review the configured schedule before syncing and back up or inspect existing vitamin reminder jobs when preservation matters.

Risk: Reminder content is read from the local VITAMINS.md schedule file and may be posted to the configured channel.

Mitigation: Keep VITAMINS.md writable only by trusted users and verify VITAMIN_CHANNEL_ID before creating cron jobs.

Risk: Cron delivery posts reminders to the configured channel and requires network access when the cron job fires.

Mitigation: Install only when channel-based supplement reminders are intended and monitor the configured OpenClaw cron entries after changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cdmichaelb/skills/vitamin-tracker-channel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cron-management guidance and reminder text based on a user-maintained VITAMINS.md schedule.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
