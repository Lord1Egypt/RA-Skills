## Description: <br>
Control a robotic arm through the OpenClaw SOARM API for reading joint state, moving by joint angles, moving by XYZ coordinates, and handling SOARM robot-control requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyoujiang](https://clawhub.ai/user/yuyoujiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robot operators use this skill to read SOARM joint and end-effector state, issue joint-angle or XYZ movement commands, start the local SOARM API, and trigger a pick task for a connected robotic arm. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent direct physical movement and pick authority over a connected SOARM robotic arm. <br>
Mitigation: Keep the API bound to localhost or a protected network, clear the workspace, supervise all runs, and require explicit human confirmation before any move or pick command. <br>
Risk: Robot motion may be unsafe if calibration, workspace setup, or motion targets are wrong. <br>
Mitigation: Verify calibration before motion, inspect and pin the external URDF/model files, and test movement commands cautiously before normal operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyoujiang/soarm-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, JSON API payload examples, and Python or shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce curl commands and local script invocations that control a connected SOARM robotic arm.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
