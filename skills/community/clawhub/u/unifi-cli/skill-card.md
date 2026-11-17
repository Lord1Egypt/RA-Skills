## Description:

Use when asked about UniFi network gear or the local network - access points, gateway, switches, WiFi, or connected clients - by querying the local UniFi gateway via the unifi CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baileywickham](https://clawhub.ai/user/baileywickham)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect UniFi gateway, access point, switch, WiFi, site, and connected-client status through the local unifi CLI. It also guides agents to request explicit user approval before network-disruptive restart or power-cycle actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to install and link an unpinned third-party CLI before using local network credentials.

Mitigation: Review the CLI source before installation, prefer a pinned commit or signed release, and install with minimal exposed secrets.

Risk: The skill uses a UniFi API key that can expose sensitive local network data or permissions.

Mitigation: Use a UniFi API key with only the permissions needed for the task and avoid sharing the key in conversation or logs.

Risk: Restart and power-cycle commands intentionally disrupt network devices.

Mitigation: Run disruptive commands only after explicit user approval for the specific device and action.

## Reference(s):

- [unifi-cli source repository](https://github.com/baileywickham/unifi-cli)
- [Bun](https://bun.sh)
- [ClawHub skill page](https://clawhub.ai/baileywickham/skills/unifi-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON CLI output when parsing UniFi device or client data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
