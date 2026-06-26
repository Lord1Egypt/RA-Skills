## Description: <br>
RealWorldClaw lets an agent control ESP32 modules, read physical sensor data, actuate relays, servos, LEDs, and buzzers, and manage automation rules for RWC-compatible devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianzhibo-design](https://clawhub.ai/user/brianzhibo-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to RWC-compatible ESP32 hardware, inspect device status, read sensor telemetry, send actuator commands, and define simple automation rules for physical workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent immediate physical actuation capability for connected ESP32 devices. <br>
Mitigation: Use harmless test loads first, do not connect relays or servos to hazardous equipment, and require human approval before running act or monitor commands. <br>
Risk: Local MQTT communication weakens TLS verification when device access codes are configured. <br>
Mitigation: Isolate the device network, protect config.json and access codes, and use trusted local devices only. <br>
Risk: Platform API registration and login commands can submit account credentials to the cloud API. <br>
Mitigation: Avoid submitting credentials unless the service is trusted and keep config.json and rules.json protected. <br>


## Reference(s): <br>
- [RWC Protocol v0.1 Draft](references/protocol.md) <br>
- [RealWorldClaw ClawHub Release](https://clawhub.ai/brianzhibo-design/realworldclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate local MQTT commands or HTTP API calls when the user runs the generated commands against configured devices.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
