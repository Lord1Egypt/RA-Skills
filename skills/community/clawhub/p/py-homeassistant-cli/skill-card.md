## Description: <br>
Tiny and short Python CLI tool to control Home Assistant devices and automations via the REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwings](https://clawhub.ai/user/xwings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Home Assistant users can use this skill to let an agent inspect devices, read smart-home state, and call Home Assistant services through a Python CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Home Assistant token allows the skill to read and control smart-home devices and automations. <br>
Mitigation: Install only for agents that should access the Home Assistant instance, protect HA_TOKEN carefully, and prefer the least-privilege credentials available. <br>
Risk: Commands can affect security-sensitive devices and automations such as locks, alarms, garage doors, gates, and generic service calls. <br>
Mitigation: Require explicit user approval before security device actions, automation changes, generic service calls, notifications, TTS, or vehicle-location commands. <br>
Risk: Presence, calendar, history, logbook, and location commands can expose sensitive household or personal information. <br>
Mitigation: Limit use to appropriate contexts and confirm before querying or sharing sensitive Home Assistant data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xwings/py-homeassistant-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, API Calls, Guidance] <br>
**Output Format:** [CLI stdout and stderr, often formatted JSON from the Home Assistant REST API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.6+, network access to a Home Assistant instance, HA_URL, and HA_TOKEN.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
