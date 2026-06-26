## Description: <br>
Controls currently bound Volcengine RTC audio/video devices by converting user requests into JSON commands for movement, volume, brightness, shutdown, emoji display, and vibration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huang-zhibin](https://clawhub.ai/user/huang-zhibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and device operators use this skill in agents that need to translate natural-language requests into Volcengine RTC device-control JSON for a currently bound hardware device. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Natural-language requests may be translated into real hardware actions such as immediate shutdown, vibration, movement, or multi-command execution without built-in confirmation. <br>
Mitigation: Require explicit operator or runtime confirmation before power-off, vibration, movement, or multi-command actions. <br>
Risk: Unsupported custom commands could be interpreted as new hardware behavior. <br>
Mitigation: Reject unsupported commands and ask the user to choose a supported command or change topic. <br>


## Reference(s): <br>
- [Protocol Specification](references/protocol.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/huang-zhibin/volcengine-rtc-device-control) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [JSON command objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return multiple send_command objects for combined device actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
