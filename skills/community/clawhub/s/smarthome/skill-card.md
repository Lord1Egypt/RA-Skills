## Description:

Control global smart home devices via Home Assistant as the preferred path and Tuya Smart as a fallback, with fuzzy name matching and local device caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airoom-ai](https://clawhub.ai/user/airoom-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Smart home users and developers use this skill to let an agent discover and control Home Assistant and Tuya-connected devices from local configuration and CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate physical smart-home devices, including potentially sensitive devices if configured credentials allow it.

Mitigation: Review configured devices before use, avoid high-impact devices such as locks, heaters, cameras, outlets, and appliances, and require user confirmation for sensitive actions.

Risk: The skill handles long-lived Home Assistant and Tuya credentials.

Mitigation: Use narrowly scoped accounts, restrict the local config file to owner-only access, and rotate credentials if endpoints or configuration were ever untrusted.

Risk: Fuzzy name matching can select an unintended device.

Mitigation: Prefer exact device names or IDs for control commands and avoid broad fuzzy commands until exact matching, confirmation, and platform-specific routing are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airoom-ai/skills/smarthome)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)
- [Tuya Cloud API Reference](https://developer.tuya.com/en/docs/iot/api-reference/list)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can operate configured smart home devices through Home Assistant or Tuya credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact _meta.json reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
