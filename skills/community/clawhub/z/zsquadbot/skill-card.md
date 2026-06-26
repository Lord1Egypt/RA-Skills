## Description: <br>
Comprehensive quadruped robot development skill covering motor control, sensor data processing, locomotion patterns, and debugging workflows for legged robots such as Unitree Go1, ANYmal, and custom four-legged designs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wsteve](https://clawhub.ai/user/Wsteve) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to generate, test, and troubleshoot quadruped robot motor commands, sensor handling, gait patterns, simulation workflows, and motion exports before moving to real hardware. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable and command real quadruped motors without strong safety gating. <br>
Mitigation: Use simulation workflows first; run hardware commands only with the robot physically secured, power and emergency stop ready, and conservative position, velocity, and force limits in place. <br>
Risk: The simple_test.py artifact uses a hardcoded dynamic code execution path. <br>
Mitigation: Avoid simple_test.py unless the hardcoded exec path is removed or replaced with a normal import from the installed skill files. <br>
Risk: Incorrect gait, calibration, or communication settings can cause unexpected motion or unstable operation. <br>
Mitigation: Verify baud rate, cable connections, sensor calibration, PID tuning, and telemetry before enabling motors or running generated gait profiles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Wsteve/zsquadbot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; bundled scripts may generate JSON or CSV motion files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes hardware-control guidance, simulation workflows, gait generation examples, and motion export instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
