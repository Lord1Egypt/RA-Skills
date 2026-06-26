## Description: <br>
Controls Sensibo smart AC devices through Sensibo's REST API for power, temperature, mode, sensor, automation, and schedule tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omere2](https://clawhub.ai/user/omere2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and smart-home users use this skill to let an agent operate Sensibo-connected AC devices, inspect temperature and humidity, and manage schedules or climate automations from natural language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensibo API keys grant access to smart-home AC controls. <br>
Mitigation: Protect the API key, avoid committing or sharing TOOLS.md, and store only the minimum device mapping needed for use. <br>
Risk: Agent actions can change AC power, temperatures, schedules, timers, or Climate React settings. <br>
Mitigation: Require confirmation for bulk operations, schedule deletion, and ambiguous room or device commands before execution. <br>


## Reference(s): <br>
- [Sensibo API key page](https://home.sensibo.com/me/api) <br>
- [Published ClawHub skill page](https://clawhub.ai/omere2/sensibo) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Sensibo API key and device IDs; generated commands can change device state, schedules, and automation settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
