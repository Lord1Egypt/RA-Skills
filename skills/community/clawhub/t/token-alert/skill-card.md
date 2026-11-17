## Description:

Monitors Clawdbot session token usage and sends threshold-based alerts with CLI status output, an optional dashboard, and optional local notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[r00tid](https://clawhub.ai/user/r00tid)

### License/Terms of Use:

MIT

## Use Case:

Developers and Clawdbot users use Token Alert to check active session token consumption before or during long agent conversations, receive threshold-based status guidance, and optionally view usage in a local dashboard or macOS notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard and proxy grant broader local gateway access than token checking requires.

Mitigation: Prefer the CLI checker for normal use; avoid the dashboard/proxy until gateway tokens are removed and proxy access is narrowly scoped and authenticated.

Risk: Notification setup persists a macOS LaunchAgent and writes local state and log files.

Mitigation: Require explicit opt-in, review the LaunchAgent before loading it, and document reversible stop and uninstall steps.

Risk: Provider setup may store API keys in local configuration.

Mitigation: Use environment variables or a secrets store for provider keys and restrict permissions on any local configuration file.

Risk: Dashboard automation can export session data or write memory automatically near high usage thresholds.

Mitigation: Require explicit confirmation before export, summary, or memory-writing actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/r00tid/skills/token-alert)
- [Clawdbot Docs](https://docs.clawd.bot)
- [README](README.md)
- [Quick Start Guide](QUICKSTART.md)
- [Testing Notes](TESTING_NOTES.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style terminal text, shell commands, local configuration guidance, and optional HTML dashboard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI checks return threshold-based exit codes; optional dashboard and notification setup add local runtime components.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
