## Description:

Control Tuya/Smart Life smart home devices including pet feeders, lights, plugs, curtains via cloud API or local network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachelchoo1212](https://clawhub.ai/user/rachelchoo1212)

### License/Terms of Use:


## Use Case:

Developers and smart-home operators use this skill to scan, query, and control Tuya or Smart Life devices through Tuya cloud APIs or local-network control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Tuya access secrets, local keys, and commands that can affect physical devices.

Mitigation: Use it only with devices and networks you own or administer, avoid placing real secrets directly in shell commands, and review commands before execution.

Risk: Cloud device information may include local_key values and other sensitive device details.

Mitigation: Do not share cloud info output publicly, and store any copied credentials in a protected secrets manager or local environment.

Risk: Dependencies and local-network device control can introduce supply-chain and operational risk.

Mitigation: Install dependencies in a pinned virtual environment and test commands on non-critical devices before routine use.

## Reference(s):

- [Tuya Smart Home API Reference](references/tuya_api.md)
- [Tuya IoT Platform](https://iot.tuya.com)
- [Tuya Smart Home ClawHub Skill Page](https://clawhub.ai/rachelchoo1212/skills/tuya-smart-home)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include device status JSON or command output from Tuya cloud and local-device operations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
