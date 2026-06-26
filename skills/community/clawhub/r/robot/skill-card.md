## Description: <br>
Build robots from hobby to industrial with hardware wiring, ROS2, motion planning, and safety constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, robotics hobbyists, and automation engineers use this skill for robotics hardware selection, wiring, sensor and motor integration, ROS configuration, industrial robot programming, and systematic troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create and reuse local notes under ~/robot that could contain project, site, or operationally sensitive details. <br>
Mitigation: Review those files periodically and do not store credentials, sensitive site details, or other secrets in the robot notes. <br>
Risk: Robotics wiring, firmware, or control code guidance can damage equipment or create unsafe motion if applied to real machines without verification. <br>
Mitigation: Treat generated robotics code as draft guidance; verify exact hardware, test with power limited, restrain mechanisms or lift wheels, and keep an emergency stop available. <br>
Risk: Industrial robot examples can be unsafe when simulation status, safety systems, coordinate frames, speed limits, or tool calibration are unknown. <br>
Mitigation: Clarify simulation versus real hardware, confirm safety systems and calibrated tooling, use low speeds, and review all motion paths before execution. <br>


## Reference(s): <br>
- [Robot Skill](https://clawhub.ai/ivangdavila/robot) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>
- [Memory Setup](artifact/memory-template.md) <br>
- [Hardware](artifact/hardware.md) <br>
- [Sensors](artifact/sensors.md) <br>
- [Motors](artifact/motors.md) <br>
- [ROS](artifact/ros.md) <br>
- [Industrial Robotics](artifact/industrial.md) <br>
- [Debugging](artifact/debugging.md) <br>
- [Project Templates](artifact/projects.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local note files under ~/robot and draft robotics code that requires human review before use on hardware.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
