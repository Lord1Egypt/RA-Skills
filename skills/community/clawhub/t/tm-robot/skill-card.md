## Description:

Control and monitor OMRON TM collaborative robots with motion commands, status feedback, safety controls, camera support, and IO handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qujingyang28](https://clawhub.ai/user/qujingyang28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to connect agents or Python automation to OMRON TM collaborative robots for status monitoring, motion commands, safety controls, camera pose retrieval, and IO handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples and tests can issue live motion commands to connected robot hardware.

Mitigation: Require explicit operator confirmation, independent safety interlocks, and bounded motion validation before running any motion command.

Risk: Module-level scripts may move hardware when executed in an environment that can reach a robot.

Mitigation: Remove or gate live-motion scripts in deployment workflows and separate hardware tests from parser or documentation-only checks.

Risk: Dependency and robot-control behavior may vary across local environments and robot configurations.

Mitigation: Pin reviewed dependency versions, verify TMflow configuration, and test on the target robot model before production use.

## Reference(s):

- [TM Robot Control on ClawHub](https://clawhub.ai/qujingyang28/skills/tm-robot)
- [TMflow Official Documentation](https://www.tm-robot.com/)
- [techmanpy](https://github.com/TechmanRobotInc/techmanpy)
- [TM Export Tool](https://github.com/TechmanRobotInc/TM_Export)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live robot-control commands that require operator review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
