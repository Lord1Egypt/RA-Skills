## Description:

Query an Unraid server via GraphQL for system, array, and Docker status in read-only mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoshiofthewire](https://clawhub.ai/user/yoshiofthewire)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and homelab operators use this skill to check Unraid system health, array/parity state, Docker status, and API connectivity from an OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Unraid API key and may load optional session credentials.

Mitigation: Keep credentials in environment variables or a private .env file, avoid optional session cookies unless required, and do not print or commit secrets.

Risk: Recurring monitoring can modify cron configuration and write logs or snapshots.

Mitigation: Review cron entries before installing them, use a safe temporary file workflow, and keep .state contents private.

Risk: Self-signed TLS certificates can weaken trust decisions if accepted without verification.

Mitigation: Use HTTPS, verify self-signed certificate fingerprints out of band, and do not install unverified certificates system-wide.

Risk: Unraid API schema differences can produce partial monitoring results.

Mitigation: Treat partial output warnings as operational signals and confirm critical status directly on the Unraid server when fields are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoshiofthewire/skills/unraid-claw)
- [OpenClaw skills docs](https://docs.openclaw.ai/tools/creating-skills)
- [Unraid API docs](https://docs.unraid.net/API/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown or plain text summaries with optional JSON reports and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include read-only health status, timestamps, system metrics, array/parity details, Docker counts, alerts, and setup guidance.]

## Skill Version(s):

1.0.4 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
