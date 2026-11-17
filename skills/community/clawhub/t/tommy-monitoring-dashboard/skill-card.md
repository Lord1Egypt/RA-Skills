## Description:

Zero-token real-time Discord monitoring dashboard for OpenClaw that displays system health, cron jobs, sessions, and performance analytics via persistent Discord messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keylimesoda](https://clawhub.ai/user/keylimesoda)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to maintain an OpenClaw Discord dashboard for activity, system health, cron status, session state, and performance trends. It is suited for monitoring an OpenClaw environment where publishing host and workflow status to Discord is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hard-coded Discord channel, message, guild, or user IDs can publish monitoring data to an unintended destination.

Mitigation: Replace all Discord destination IDs with verified values before enabling posting or scheduled updates.

Risk: Direct bot-token handling can expose Discord credentials or grant broader access than needed.

Mitigation: Avoid zero-token-dashboard-v2.sh unless direct bot-token handling is acceptable, and use a least-privilege bot scoped to the intended channel.

Risk: Scheduled automation can repeatedly publish host activity and OpenClaw metadata outside the user's control.

Mitigation: Run local-only dry tests first, review the scheduled task, and add the cron job only after confirming the data and destination are appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keylimesoda/skills/tommy-monitoring-dashboard)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown dashboard text, shell command invocations, and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent Discord dashboard updates and local performance tracking data when configured.]

## Skill Version(s):

2.0.0 (source: package.json and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
