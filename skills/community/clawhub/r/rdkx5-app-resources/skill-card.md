## Description:

Access to RDK X5 /app folder resources including GPIO, multimedia, AI samples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zh1fen](https://clawhub.ai/user/zh1fen)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to locate and run RDK X5 board demos for GPIO, I2C/SPI, UART, video capture, multimedia processing, AI inference, and ISP tuning under the /app folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GPIO, PWM, camera, ISP tuning, and root-level examples may perform real hardware-control actions.

Mitigation: Confirm the board model, pin numbering, wiring, voltage and current limits, and attached hardware safety before executing examples.

Risk: Running RDK X5 Python samples in a conda environment may fail because required D-Robotics libraries are installed for system Python.

Mitigation: Use /usr/bin/python3.10 for the documented Python demos unless the target board environment has been explicitly configured otherwise.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and resource paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is specific to RDK X5 /app sample resources and system Python usage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
