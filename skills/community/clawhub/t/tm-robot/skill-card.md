## Description: <br>
Control and monitor OMRON TM collaborative robots with motion commands, status feedback, safety controls, camera support, and IO handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qujingyang28](https://clawhub.ai/user/qujingyang28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to connect agent workflows to configured OMRON TM collaborative robots for status monitoring, motion commands, IO checks, camera pose retrieval, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live motion scripts and examples can move physical robot hardware or actuate IO outputs. <br>
Mitigation: Use only with trained robot operators, an isolated control network, a clear robot work area, emergency stop available, and verified speed and tooling limits. <br>
Risk: Included reset_alarm and camera trigger helpers are convenience functions, not validated safety interlocks. <br>
Mitigation: Rely on the robot safety controller and site safety procedures, and review or remove these helpers before operational deployment. <br>
Risk: Incorrect robot IP, TMflow, Ethernet Slave, or Listen Node configuration can produce failed connections or unintended command targets. <br>
Mitigation: Verify the target robot, network ports, TMflow version, Ethernet Slave variables, and Listen Node project in a dry-run or controlled test setup before sending motion commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qujingyang28/tm-robot) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact test report](artifact/TEST_REPORT.md) <br>
- [TMflow official documentation](https://www.tm-robot.com/) <br>
- [techmanpy GitHub](https://github.com/TechmanRobotInc/techmanpy) <br>
- [TM Export tool](https://github.com/TechmanRobotInc/TM_Export) <br>
- [RobotQu support site](https://robotqu.com) <br>
- [RobotQu forum](https://robotqu.mbbs.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include robot IP configuration, TMflow setup steps, Python API calls, diagnostic commands, and safety review guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact documentation references 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
