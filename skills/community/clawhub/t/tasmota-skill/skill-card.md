## Description:

Discover, monitor, and control Tasmota smart home devices on local networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wmantly](https://clawhub.ai/user/wmantly)

### License/Terms of Use:


## Use Case:

Developers, operators, and smart-home administrators use this skill to discover Tasmota devices on local networks, inspect device status, and control power, brightness, and color settings for devices they administer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan a local network and read device and network details.

Mitigation: Use it only on networks and Tasmota devices the user administers, and run discovery during an approved maintenance window when network scanning is acceptable.

Risk: The skill can change smart-home device states, including power, brightness, and color.

Mitigation: Confirm the target device IP and intended command before execution, and avoid raw commands unless the operator understands their effect.

Risk: One script can execute a controller from outside the reviewed package.

Mitigation: Fix or verify the external controller path before running bulk status checks so reviewed code is used.

## Reference(s):

- [ClawHub Tasmota skill page](https://clawhub.ai/wmantly/skills/tasmota-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local-network discovery and device-control commands when used by an agent with shell access.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
