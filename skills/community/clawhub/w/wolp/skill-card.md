## Description:

Wake or shut down LAN devices by sending WOL-plus packets from the agent host when the user provides target network details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeyeel](https://clawhub.ai/user/leeyeel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send wake and shutdown packets to known devices on a local network, inspect stored device inventory, and configure a compatible WOL-plus client when shutdown support is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide installation of a persistent third-party WOL-plus service and privileged packages.

Mitigation: Install the client only from trusted release sources, verify downloaded artifacts before installation, and confirm the service configuration after install.

Risk: The client documentation includes default web credentials for the LAN Web UI.

Mitigation: Change the default password before exposing or using the Web UI on the local network.

Risk: The device inventory may store MAC addresses, IP addresses, extra data values, and recent action timestamps.

Mitigation: Treat the inventory as local network configuration data and limit access to users who are authorized to control those devices.

Risk: Packet transmission confirms only that a UDP packet was sent locally, not that the remote device changed power state.

Mitigation: Use dry runs and follow-up verification, such as service status or Web UI checks, before reporting a completed wake or shutdown outcome.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leeyeel/skills/wolp)
- [WOL-plus project](https://github.com/leeyeel/WOL-plus)
- [WOL-plus releases](https://github.com/leeyeel/WOL-plus/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send UDP packets or update the local device inventory when the user requests a non-dry-run operation.]

## Skill Version(s):

0.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
