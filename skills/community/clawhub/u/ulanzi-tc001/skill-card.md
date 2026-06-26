## Description: <br>
Control the Ulanzi TC001 (Pixel Clock) over local HTTP to list commands, read status, enable or disable gadgets, and change settings such as brightness, night mode, timezone, switch speed, or scroll speed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felipeouropreto](https://clawhub.ai/user/felipeouropreto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and device operators use this skill to inspect and configure a Ulanzi TC001 Pixel Clock from an agent workflow, including gadget toggles and device settings over local HTTP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The weather command sends city names to Open-Meteo and posts notifications to the configured AWTRIX host. <br>
Mitigation: Use the weather command only when that data sharing is acceptable, and verify the AWTRIX host and port in config.json before execution. <br>
Risk: The skill can write configuration values to a local Ulanzi TC001 device over HTTP. <br>
Mitigation: Confirm the configured TC001 host points to the intended device before running commands that change settings. <br>
Risk: A YouTube API key entered through the skill may be stored on the device and sent over local HTTP. <br>
Mitigation: Use a restricted key where possible and treat any configured key as exposed to the local device and network path. <br>


## Reference(s): <br>
- [Ulanzi TC001 local HTTP endpoints](references/tc001-api.md) <br>
- [ClawHub skill page](https://clawhub.ai/felipeouropreto/ulanzi-tc001) <br>
- [Publisher profile](https://clawhub.ai/user/felipeouropreto) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send local HTTP requests to the configured TC001 and AWTRIX hosts, and the weather command contacts Open-Meteo before posting a notification.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
