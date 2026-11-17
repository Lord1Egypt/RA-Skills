## Description:

Manages LIKONG ST200TH temperature and humidity transmitters over MQTT, including telemetry queries, configuration changes, calibration, restart, factory reset, and HTTP OTA updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shodan1q](https://clawhub.ai/user/shodan1q)

### License/Terms of Use:

MIT-0

## Use Case:

IoT operators, facilities engineers, and developers use this skill to monitor and administer ST200TH transmitters they own or manage. It supports reading sensor and device state, maintaining local device selections, changing protocol configuration, calibrating readings, and triggering live maintenance actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send live device-changing MQTT commands, including reset, restart, calibration, protocol configuration, and OTA update actions.

Mitigation: Operate only on devices you own or administer, confirm the exact MAC address before each live action, and require explicit user confirmation for reset and OTA workflows.

Risk: MQTT communication and HTTP OTA workflows are weakly protected, and firmware updates can alter device behavior.

Mitigation: Use the skill only on isolated, trusted networks and avoid OTA firmware unless the firmware source and integrity have been independently verified.

Risk: Incorrect calibration or protocol configuration can degrade telemetry quality or disconnect devices until corrected.

Mitigation: Review requested compensation values and network settings before sending them, then verify device readings and connectivity after changes.

## Reference(s):

- [LIKONG ST200TH MQTT protocol documentation](https://docv2.likong-iot.com/products/transmitters/ST200TH/mqtt)
- [ClawHub skill page](https://clawhub.ai/shodan1q/skills/st200th-mqtt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands; the CLI can emit plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store local device MAC/name mappings and send live MQTT commands to selected devices.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
