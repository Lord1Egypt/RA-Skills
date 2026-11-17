## Description:

The Segway skill helps agents interact with Segway personal electric vehicles for connection, diagnostics, configuration, data access, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aninebot](https://clawhub.ai/user/aninebot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to connect to Segway devices, read status, battery, mileage, firmware, and ride data, adjust supported vehicle settings, run diagnostics, troubleshoot common issues, and export riding statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Device-control commands such as reset, speed-limit changes, lighting changes, firmware work, or other configuration actions can affect a real vehicle.

Mitigation: Confirm the target device, keep the vehicle stopped for parameter changes, back up settings before firmware work, and avoid factory reset unless the erased settings are understood.

Risk: Configuration or firmware work may be less reliable when the device battery is low.

Mitigation: Check that the device battery is above 20% before running operations that change settings or firmware.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration instructions]

**Output Format:** [Markdown with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include device-control command suggestions, diagnostic explanations, troubleshooting steps, and export guidance.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
