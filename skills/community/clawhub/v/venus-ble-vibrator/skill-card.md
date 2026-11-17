## Description:

Control a Venus (Cachito) BLE vibrator from natural language by calling a local HTTP server that broadcasts BLE commands to the toy through macOS CoreBluetooth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amandaclarke61](https://clawhub.ai/user/amandaclarke61)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to control a Venus or Cachito-protocol BLE vibrator through OpenClaw after configuring a local macOS bridge. It is intended for informed, consent-based device control with immediate stop and status commands available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw may directly activate an intimate physical device.

Mitigation: Use only with informed consent from the person using the device, keep the stop command available, and prefer timed sessions that stop at intensity 0.

Risk: The skill depends on an unauthenticated local bridge.

Mitigation: Run the bridge locally, restrict network exposure, and avoid exposing port 8888 beyond the trusted host environment.

Risk: External setup code may change after release.

Mitigation: Review and pin a known bridge version before running setup or device-control commands.

## Reference(s):

- [ToyBridge setup guide](https://github.com/AmandaClarke61/toybridge)
- [Buttplug.io compatibility index](https://iostindex.com)
- [ClawHub skill page](https://clawhub.ai/amandaclarke61/skills/venus-ble-vibrator)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only OpenClaw guidance for a local HTTP bridge on port 8888.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
