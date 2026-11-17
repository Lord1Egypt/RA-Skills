## Description:

Push high-risk ClawVault security events and daily security reports through OpenClaw agent messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martin2877](https://clawhub.ai/user/martin2877)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security operators use this skill to configure OpenClaw delivery for high-risk ClawVault events, run one-time alert checks, manage background monitoring, and send daily security summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run as a background daemon and send notifications repeatedly.

Mitigation: Review configuration before enabling the daemon, use the built-in deduplication and rate limits, and monitor daemon status and logs.

Risk: OpenClaw delivery can forward security-event summaries to external channels.

Mitigation: Use a dedicated low-privilege OpenClaw notification agent and restrict deliver routes to trusted channels.

Risk: Security-event text from ClawVault is passed into an OpenClaw agent.

Mitigation: Keep notifications terse and redacted, review events before acting on them, and leave input previews and file paths disabled unless required for trusted workflows.

Risk: A non-loopback dashboard URL could retrieve event data from an untrusted source.

Mitigation: Keep the dashboard URL on http://127.0.0.1:8766 unless the remote endpoint and its event data are explicitly trusted.

## Reference(s):

- [ClawVault repository](https://github.com/tophant-ai/ClawVault)
- [ClawVault issues](https://github.com/tophant-ai/ClawVault/issues)
- [ClawHub skill page](https://clawhub.ai/martin2877/skills/tophant-clawvault-openclaw-alerts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown or JSON command output with OpenClaw notification messages and configuration/status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are redacted by default, capped in length, deduplicated, and rate limited.]

## Skill Version(s):

0.1.0 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
