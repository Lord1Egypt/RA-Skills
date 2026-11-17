## Description:

Controls Roku TVs and streaming devices on the local network using Roku ECP for discovery, navigation, playback, app launch, volume, search text, and power commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaloney](https://clawhub.ai/user/imaloney)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent discover and control approved Roku devices on the same local network, including menu navigation, playback, app launch, volume, power, and search text workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send unauthenticated commands to Roku devices reachable on the same LAN.

Mitigation: Use it only on trusted networks and target approved Roku IP addresses.

Risk: Discovery results on shared or guest networks may include devices the user should not control.

Mitigation: Prefer explicit, trusted Roku IP addresses over untrusted discovery results.

Risk: Power, app launch, volume, and text input commands can disrupt the current viewer experience.

Mitigation: Review disruptive actions before execution.

## Reference(s):

- [Common Roku Apps & Channels](references/common-apps.md)
- [Roku Remote Keys Reference](references/remote-keys.md)
- [Roku Device Mapping](references/roku.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Roku devices reachable on the same LAN and may return JSON-formatted device, app, or active-app data.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
