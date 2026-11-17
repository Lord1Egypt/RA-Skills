## Description:

SignalRadar monitors Polymarket prediction markets for probability changes and sends alerts when configured thresholds are crossed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahnxu](https://clawhub.ai/user/vahnxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use SignalRadar to add, inspect, and monitor Polymarket markets, receive threshold-crossing alerts, and manage background checks or digests through the CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabling scheduling creates a recurring background job that can persist after the agent session.

Mitigation: Require user consent before enabling scheduling, and use `schedule disable` or `schedule clear-route` to remove monitoring or cached reply-route state.

Risk: Webhook delivery sends monitored market questions, probabilities, and a bearer-style webhook URL to a user-selected provider.

Mitigation: Use a trusted endpoint, keep webhook URLs masked, and retain the default HTTPS and public-address destination guards.

Risk: File delivery can append alert data to local disk.

Mitigation: Keep the default data-directory scope unless the user deliberately enables `SIGNALRADAR_ALLOW_ANY_FILE_TARGET=1`.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vahnxu/skills/signalradar)
- [SignalRadar Configuration Reference](references/config.md)
- [SignalRadar Runtime Protocol Reference](references/protocol.md)
- [SignalRadar Operations Reference](references/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Natural-language guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce alerts, digest summaries, configuration guidance, and structured CLI status output.]

## Skill Version(s):

1.5.8 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
