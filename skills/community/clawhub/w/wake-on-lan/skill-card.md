## Description:

Send Wake on LAN (WOL) magic packets to wake computers and network devices on a local network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonakic](https://clawhub.ai/user/tonakic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT administrators, and users with authorized local-network devices use this skill to wake configured computers or network devices by MAC address or saved device name, optionally waiting for a ping response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send Wake-on-LAN packets and ping configured device IPs on the local network.

Mitigation: Use it only on networks and devices the user is authorized to manage, and review broadcast addresses before execution.

Risk: Device mappings may include MAC addresses, optional IP addresses, broadcast addresses, and notes in references/devices.json.

Mitigation: Review references/devices.json before use and avoid storing devices the user would not want an agent to wake.

## Reference(s):

- [Device configuration example](references/devices.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands and brief status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local device names, MAC addresses, broadcast addresses, UDP ports, and ping status when the user asks to wake or manage devices.]

## Skill Version(s):

1.0.1 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
