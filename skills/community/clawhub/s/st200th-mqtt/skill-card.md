## Description: <br>
立控 ST200TH 温湿度变送器全功能管理技能——查询温湿度/气压/海拔、查看设备信息(IP/型号/固件)、修改配置、补偿校准、重启设备、OTA升级。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shodan1q](https://clawhub.ai/user/shodan1q) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to let an agent query and administer LIKONG ST200TH temperature and humidity transmitters over MQTT, including sensor readings, device configuration, calibration, restart, reset, and OTA update workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change device configuration, restart devices, restore factory settings, and start OTA updates. <br>
Mitigation: Confirm the exact target MAC address before writes and require an explicit user confirmation for reset, OTA, and other maintenance-window operations. <br>
Risk: MQTT passwords, network details, and device identifiers may be exposed during configuration or troubleshooting. <br>
Mitigation: Avoid sharing credentials or network details in chat or logs, and use the skill only on trusted networks where device administration is intended. <br>
Risk: OTA and HTTP configuration paths rely on HTTP-only URIs. <br>
Mitigation: Use OTA and HTTP configuration only on an isolated trusted network and verify the firmware URI before sending the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shodan1q/st200th-mqtt) <br>
- [LIKONG ST200TH MQTT protocol documentation](https://docv2.likong-iot.com/products/transmitters/ST200TH/mqtt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus optional plain text or JSON command output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can query device state, persist a local device list, and send MQTT-based configuration or maintenance actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
