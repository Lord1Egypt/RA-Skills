## Description:

SmartPi device binding, QR-code setup, device management, and troubleshooting for connection failures, 9002 timeouts, and unresponsive SmartPi devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengseven777](https://clawhub.ai/user/fengseven777)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to bind and manage SmartPi devices, check plugin and Gateway status, and diagnose connection, routing, and AI response timeout issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or repairing the OpenClaw SmartPi plugin can change the local environment.

Mitigation: Confirm the plugin source, publisher, and version before approving installation or repair.

Risk: Device removal, configuration changes, and Gateway restart can alter local state or interrupt service.

Mitigation: Proceed only after explicit user confirmation and only when the action matches the requested SmartPi task.

Risk: Incorrect channel configuration can break message routing for SmartPi or other channels.

Mitigation: Read the full configuration first, preserve existing channel entries, and verify that channels.openclaw-smartpi matches the plugin channel id.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengseven777/skills/smartpi)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, status summaries, and next-step recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first troubleshooting; state-changing actions require user confirmation.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
