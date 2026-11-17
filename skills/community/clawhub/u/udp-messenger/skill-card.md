## Description:

LocalUDPMessenger helps agents discover peers and exchange text messages over a local UDP network with configurable trust, rate limits, logging, and optional relay monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turfptax](https://clawhub.ai/user/turfptax)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and operators use this skill to coordinate OpenClaw agents on the same LAN, manage peer trust, and review or relay local agent-to-agent messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network messages can trigger agent activity without the confirmation users are told to expect.

Mitigation: Use only on trusted networks, review before installing, and do not rely on always-confirm until enforcement is fixed.

Risk: Relay and wake-up settings can increase exposure of message contents or trigger automatic agent turns.

Mitigation: Leave relayServer and hookToken disabled unless explicitly needed and avoid sharing secrets or project data through messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turfptax/skills/udp-messenger)
- [Project homepage](https://github.com/turfptax/openclaw-udp-messenger)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and agent tool outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local UDP peer discovery, messaging, trust management, inbox, status, and log interactions through OpenClaw tools.]

## Skill Version(s):

1.6.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
