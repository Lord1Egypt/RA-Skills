## Description: <br>
Add HTTP OTA (Over-The-Air) firmware update capability to Unihiker K10 Arduino projects, including AP/STA projects and ESP-NOW projects that need a safe OTA maintenance mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockets-cn](https://clawhub.ai/user/rockets-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add scriptable HTTP firmware updates to Unihiker K10 Arduino projects without relying on USB or ArduinoOTA. It is especially relevant for AP/STA deployments and ESP-NOW projects that need an explicit OTA maintenance mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copyable examples expose firmware reflashing over plain HTTP with weak default Wi-Fi credentials and no access control. <br>
Mitigation: Use a unique per-device password or token, require an explicit short-lived maintenance mode such as a button press, and avoid exposing the OTA endpoint on untrusted networks. <br>
Risk: Firmware uploads may be accepted without integrity validation. <br>
Mitigation: Validate firmware signatures or hashes before applying OTA updates. <br>
Risk: ESP-NOW or time-critical control behavior can conflict with Wi-Fi networking and flash writes during OTA. <br>
Mitigation: Enter a dedicated OTA maintenance mode, align Wi-Fi and ESP-NOW channels when needed, and pause ESP-NOW sends and control loops while upload is active. <br>
Risk: An incorrect partition table can overwrite K10 AI model regions or fail because no OTA partition is available. <br>
Mitigation: Use OTA app partitions that end before the documented model, voice_data, and fr regions, and perform the first partition-table change by USB. <br>


## Reference(s): <br>
- [K10 HTTP OTA Implementation Guide](references/ota-implementation.md) <br>
- [ClawHub skill page](https://clawhub.ai/rockets-cn/skills/unihiker-k10-ota) <br>
- [Publisher profile](https://clawhub.ai/user/rockets-cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline C++, CSV, bash, PowerShell, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces firmware integration guidance, partition table configuration, OTA endpoint code, and upload commands for Unihiker K10 Arduino projects.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
