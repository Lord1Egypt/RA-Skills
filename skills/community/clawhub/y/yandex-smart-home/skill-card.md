## Description: <br>
This skill lets an agent inspect and control Yandex Smart Home devices, groups, and scenarios through the official Yandex IoT API using a user-provided OAuth token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dima-online](https://clawhub.ai/user/dima-online) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to list Yandex Smart Home devices, read device state, change supported device capabilities such as power, brightness, color temperature, RGB color, thermostat temperature, and modes, and launch configured scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Yandex OAuth token that can view and control smart-home devices. <br>
Mitigation: Install only when the user is comfortable giving the agent this level of access, and store the token in the documented YANDEX_IOT_TOKEN environment variable rather than sharing it in chat. <br>
Risk: State-changing commands can affect real household devices, groups, thermostats, or scenarios. <br>
Mitigation: Require manual confirmation before any device action, group action, thermostat change, scenario launch, or request that affects many devices. <br>
Risk: The /user/info response can reveal household layout, device names, room structure, ownership, and scenario details. <br>
Mitigation: Avoid sharing raw /user/info output; summarize only the device or room details needed for the user's request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dima-online/yandex-smart-home) <br>
- [Publisher profile](https://clawhub.ai/user/dima-online) <br>
- [Yandex Smart Home IoT API](https://api.iot.yandex.net) <br>
- [Yandex OAuth application registration](https://oauth.yandex.ru/client/new) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a Yandex OAuth token supplied through YANDEX_IOT_TOKEN with iot:view and iot:control scopes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
