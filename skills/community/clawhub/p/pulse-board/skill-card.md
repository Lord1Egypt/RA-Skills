## Description:

Universal operational digest for agent skill stacks. Every scheduled skill logs its outcome with log-append.sh; twice daily, digest-agent.sh reads the log, composes a human-readable summary via the configured OpenClaw agent, delivers it to Telegram, Discord, or a log file, and clears the pending log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littlejakub](https://clawhub.ai/user/littlejakub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Pulse Board to collect outcomes from scheduled agent-skill cron jobs, summarize recent activity, and deliver operational digests through a configured channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and plug workflow can add persistent entries to the user's crontab.

Mitigation: Review the proposed cron entries before accepting installation, plug only trusted jobs, and periodically inspect the user crontab for Pulse Board entries.

Risk: Runtime scripts can source a shared secrets file as shell code and may store notification credentials in local configuration.

Mitigation: Use tightly permissioned config and secrets files, keep the secrets file limited to trusted assignments, and avoid sharing the Pulse Board home directory with untrusted users.

Risk: Operational log content can be sent to the configured OpenClaw agent, Telegram, or Discord.

Mitigation: Use a local or low-privilege summarization agent when privacy matters, choose log-only delivery for sensitive environments, and prevent plugged cron jobs from writing secrets or incident-sensitive data to logs.

Risk: Cron command construction depends on the trusted command and schedule values supplied during setup or plug-in registration.

Mitigation: Validate cron expressions and command strings before registration, and avoid registering commands from untrusted sources.

## Reference(s):

- [Pulse Board on ClawHub](https://clawhub.ai/littlejakub/skills/pulse-board)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and shell-oriented operational digest output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local configuration, registry, and digest log files, and may deliver digest text to Telegram or Discord when configured.]

## Skill Version(s):

1.1.3 (source: server evidence and CHANGELOG.md, released 2026-03-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
