## Description:

Automatically update Clawdbot and all installed skills once daily, using cron to check for updates, apply them, and send the user a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-din](https://clawhub.ai/user/a-din)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to configure unattended daily updates for Clawdbot and installed skills, then receive a concise report of updated, current, or failed components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended daily updates can change Clawdbot and all installed skills without review at each run.

Mitigation: Use a dry-run or notification-only schedule first, pin or approve versions before installation, and keep the Daily Auto-Update cron job easy to list and remove.

Risk: Update failures can leave Clawdbot or skills only partially updated.

Mitigation: Review each delivered update summary, check logged errors, and run manual update commands when the report shows partial success or failure.

## Reference(s):

- [Xiaopi Auto Updater ClawHub Page](https://clawhub.ai/a-din/skills/xiaopi-auto-updater)
- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and cron configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions and update-summary guidance for Darwin and Linux Clawdbot environments.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
