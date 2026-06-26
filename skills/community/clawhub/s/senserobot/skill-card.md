## Description: <br>
Enables an agent to control a SenseRobot Go-playing robot for stone pickup and placement, arm movement, expressions, Chinese text-to-speech, board cleanup, board detection, photo capture, recording, and image display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SenseRobotClawBot](https://clawhub.ai/user/SenseRobotClawBot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers who own or administer a SenseRobot device use this skill to guide an agent through supervised Go robot control, including movement, stone handling, board state checks, media capture, and speech or display actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger physical arm movement and board cleanup on a connected robot. <br>
Mitigation: Use it only with in-person supervision, keep the arm area clear, and require confirmation before movement or cleanup commands. <br>
Risk: The skill can control camera and microphone functions. <br>
Mitigation: Use photo and recording commands only with explicit consent from nearby people. <br>
Risk: The image display command can upload a local file to the robot. <br>
Mitigation: Avoid uploading sensitive local files and review the selected image path before execution. <br>


## Reference(s): <br>
- [SenseRobot API Reference](references/API_REFERENCE.md) <br>
- [SenseRobot Cheat Sheet](references/CHEATSHEET.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/SenseRobotClawBot/senserobot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls] <br>
**Output Format:** [Markdown guidance with curl examples and Python CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and network access to the SenseRobot device at 192.168.199.10:60010.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
