## Description:

Read light intensity from USB sensors with real-time monitoring, filtering, and threshold detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj-hao](https://clawhub.ai/user/lj-hao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to read real-time lux values from a USB-connected light sensor, smooth readings with a moving average, and classify ambient light as dark or bright using thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires serial-device access to connected USB hardware.

Mitigation: Install it only where sensor access is intended, verify the expected device path, and limit dialout or serial permissions to users who need hardware access.

Risk: The bundled guide includes relay automation examples that can switch real connected equipment.

Mitigation: Review or remove relay-control workflows before use, inspect connected equipment behavior, and require human approval before allowing an agent to operate physical devices.

Risk: The setup guide includes privileged installation patterns and unpinned external components.

Mitigation: Avoid curl-to-sudo installation, pin CLI and Python dependency versions, and independently inspect external components before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lj-hao/skills/usb-light-sensor-reader)
- [pyserial Documentation](https://pyserial.readthedocs.io/)
- [ClawHub Documentation](https://clawhub.ai/docs)
- [NanoBot Documentation](https://nanobot.ai/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include serial-port setup, Python sensor usage, real-time lux readings, and threshold checks.]

## Skill Version(s):

1.0.2 (source: server release metadata, SKILL.md frontmatter, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
