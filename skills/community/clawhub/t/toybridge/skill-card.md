## Description:

Control any BLE toy that has been reverse-engineered and connected via the ToyBridge server. Calls a local HTTP API to send vibrate/stop commands. Requires the ToyBridge server running on the same machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amandaclarke61](https://clawhub.ai/user/amandaclarke61)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to control reverse-engineered BLE toys through a trusted local ToyBridge server, including vibrate, stop, status, and preset pattern commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send live control commands to an intimate physical BLE device, including high intensity vibration.

Mitigation: Require explicit confirmation for each session, verify the correct device and environment, start at low intensity, and keep the stop command available.

Risk: Commands depend on a trusted local ToyBridge server and device-specific reverse-engineered configuration.

Mitigation: Install only with a trusted local ToyBridge setup and verify the configured device before issuing vibrate or pattern commands.

## Reference(s):

- [ToyBridge setup guide](https://github.com/AmandaClarke61/toybridge)
- [ToyBridge ClawHub skill page](https://clawhub.ai/amandaclarke61/skills/toybridge)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands call a local HTTP ToyBridge API and use intensity values from 0 to 100.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
