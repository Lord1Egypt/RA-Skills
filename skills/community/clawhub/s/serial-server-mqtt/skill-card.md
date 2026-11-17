## Description:

Manages SP501LW serial gateways over MQTT for serial pass-through and Modbus RTU data collection, with custom topics and broker settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likong-iot](https://clawhub.ai/user/likong-iot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to register and manage SP501LW gateways, switch MQTT and Modbus modes, send or listen to serial data, and configure Modbus RTU polling tasks through MQTT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control real gateways and attached serial or Modbus equipment over MQTT.

Mitigation: Use only authorized gateways, confirm device IDs and topics before commands, and review planned commands before execution.

Risk: MQTT credentials and device records may expose passwords, and TLS is not implemented.

Mitigation: Avoid default public broker credentials, use trusted networks, protect devices.json and command output, and prefer secured broker and network controls where available.

Risk: Configuration changes can reboot devices for 5-30 seconds.

Mitigation: Schedule configuration operations, wait for reboot completion before follow-up commands, and avoid consecutive commands during restart windows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/likong-iot/skills/serial-server-mqtt)
- [Project homepage](https://github.com/likong-iot/sp501lw-mqtt-skill)
- [README](artifact/README.md)
- [Architecture notes](artifact/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MQTT topics, broker settings, device IDs, and Modbus polling parameters supplied by the user.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
