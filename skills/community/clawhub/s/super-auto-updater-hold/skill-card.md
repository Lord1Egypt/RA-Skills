## Description:

Sets up a scheduled routine that checks for Clawdbot and installed skill updates, applies them, and reports the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to configure recurring update checks for Clawdbot and installed skills, with a summary of version changes or failures after each run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended updates can change Clawdbot and every installed skill without direct review.

Mitigation: Use a dry-run or notify-only schedule first, require approval before applying updates, and review or pin versions where possible.

Risk: A scheduled updater can apply changes under the permissions of the account running the cron job.

Mitigation: Run the updater under a low-privilege account, keep backups, and verify the timezone and schedule before enabling it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-auto-updater-hold)
- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate scheduled-update instructions and human-readable update summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
