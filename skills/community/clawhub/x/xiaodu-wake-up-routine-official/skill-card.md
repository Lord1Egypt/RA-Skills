## Description: <br>
Orchestrates a child's Xiaodu wake-up routine by reusing the installed xiaodu-control-official scripts to trigger morning scenes, adjust supported Xiaodu IoT devices, and use Xiaodu smart-screen speech or media capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dueros-mcp](https://clawhub.ai/user/dueros-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and home-automation agents use this skill to turn broad Chinese wake-up requests into a conservative, scene-first Xiaodu morning routine for a child's room. It helps choose supported scene, light, curtain, comfort, smart-screen speech, and optional media actions while avoiding unsupported device assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real smart-home actions through its xiaodu-control-official dependency and could target the wrong room, device, or smart screen if the environment is ambiguous. <br>
Mitigation: Use only with a trusted xiaodu-control-official installation and trusted Xiaodu/mcporter account, refresh device lists before execution, and require a minimal confirmation when room or device targeting is unclear. <br>
Risk: The skill can store household wake-up preferences, which may reveal routines or affect future automation behavior. <br>
Mitigation: Set clear preferences for weather, time, reminders, music, and memory use before first deployment, and review memory updates after preference changes. <br>
Risk: The security evidence notes inconsistent defaults for media, weather, reminders, and music. <br>
Mitigation: Configure allowed default content explicitly and supervise early runs so optional weather, reminder, and media actions occur only when intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dueros-mcp/xiaodu-wake-up-routine-official) <br>
- [Publisher profile](https://clawhub.ai/user/dueros-mcp) <br>
- [Usage notes](references/usage-notes.md) <br>
- [Test cases](references/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Natural-language guidance with ordered shell-command calls and concise user-facing status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update household wake-up preferences when the agent has explicit evidence that a memory file was written.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
