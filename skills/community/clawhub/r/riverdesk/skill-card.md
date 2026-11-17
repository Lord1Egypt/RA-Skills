## Description:

Connect OpenClaw to the RiverDesk task app: install the openclaw-riverdesk channel plugin, pair with a one-time code from web.riverdesk.ai, and verify the agent is online.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riverdesk-ai](https://clawhub.ai/user/riverdesk-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an OpenClaw gateway agent to RiverDesk, pair it with a one-time code, verify the channel is online, and troubleshoot common connectivity or pairing issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs installation of an unpinned RiverDesk gateway plugin that can handle agent messages and reconnect automatically.

Mitigation: Review the plugin source, publisher, version, and integrity before installing, and use it only when RiverDesk should connect to the OpenClaw agent.

Risk: Pairing codes, persistent plugin tokens, keypairs, and state files are sensitive credentials.

Mitigation: Do not print, log, or transmit these secrets; back up gateway configuration before changes and remove used pairing codes from config when appropriate.

Risk: Gateway config edits and restarts can disrupt existing agents or sessions.

Mitigation: Merge only the RiverDesk channel block, preserve existing channels, and warn users before restarting the gateway during critical sessions.

## Reference(s):

- [RiverDesk](https://riverdesk.ai)
- [RiverDesk web app](https://web.riverdesk.ai)
- [RiverDesk API health endpoint](https://api.riverdesk.ai/health)
- [ClawHub skill page](https://clawhub.ai/riverdesk-ai/skills/riverdesk)
- [Publisher profile](https://clawhub.ai/user/riverdesk-ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, pairing, verification, troubleshooting, and secret-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
