## Description:

Solo Impl is an autonomous executor for Solo CLI that runs setup, calibration, teleoperation, dataset recording, policy training, and inference commands in a user's terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samarthshukla6](https://clawhub.ai/user/samarthshukla6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics operators use Solo Impl to have an agent execute Solo CLI workflows for supported robot arms, from environment setup and calibration through dataset recording, training, and inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run Solo CLI commands that affect connected robot arms and local robot configuration.

Mitigation: Review displayed commands before execution, keep the robot workspace clear, and require physical confirmation for robot movement.

Risk: The skill can install mutable third-party code, including a remote installer and source checkout.

Mitigation: Use only when comfortable with those installs, prefer pinned or package-manager installs where possible, and review installer commands before running them.

Risk: Dataset/model pushes and training logs can use HuggingFace or Weights & Biases credentials.

Mitigation: Enable Hub or W&B operations only intentionally, confirm the destination, and avoid exposing credentials in terminal output or logs.

## Reference(s):

- [Solo Impl on ClawHub](https://clawhub.ai/samarthshukla6/skills/solo-impl)
- [Solo CLI documentation](https://docs.getsolo.tech)
- [Solo Claw homepage](https://github.com/GetSoloTech/Solo-claw)
- [Solo CLI source repository](https://github.com/GetSoloTech/solo-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands and terminal status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open terminal windows, run long-running commands, and report validation status for robot workflows.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact/skill.json reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
