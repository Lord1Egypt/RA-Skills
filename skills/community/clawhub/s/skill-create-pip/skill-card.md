## Description: <br>
Control Ecovacs/DEEBOT robot vacuums via the Ecovacs IoT API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1209823208](https://clawhub.ai/user/1209823208) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to control Ecovacs/DEEBOT robot vacuums, inspect device state, manage cleaning behavior, and issue supported Ecovacs IoT API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable Ecovacs account material may be stored locally in the session file. <br>
Mitigation: Use the skill only on a trusted machine, restrict ~/.ecovacs_session.json to user-only permissions, remove stored credentials after use, and consider editing the script to avoid storing the password hash. <br>
Risk: Broad robot-vacuum control commands can start cleaning, alter settings, or change schedules. <br>
Mitigation: Review each device command and payload before execution, especially commands that start cleaning, change suction or water levels, dock the robot, or modify schedules. <br>


## Reference(s): <br>
- [Ecovacs Robot Control API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python examples, and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Ecovacs IoT API command names, device identifiers, and local session-file handling guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
