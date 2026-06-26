## Description: <br>
Manages SP501LW serial gateways over MQTT for serial passthrough and Modbus RTU data collection with custom topics and brokers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likong-iot](https://clawhub.ai/user/likong-iot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to register SP501LW gateways, send and listen for serial data, switch gateway modes, and configure Modbus RTU polling over MQTT. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send commands to real SP501LW gateways and change gateway configuration, including operations that may restart the device. <br>
Mitigation: Install and use it only for gateways you control, review commands before execution, and wait for devices to finish restarting after configuration changes. <br>
Risk: Default or public MQTT credentials and unencrypted broker connections can expose device-control traffic. <br>
Mitigation: Use a private MQTT broker with unique credentials and TLS where supported, and avoid public or default credentials in production. <br>
Risk: Saved gateway records may include broker topics, usernames, and passwords. <br>
Mitigation: Protect the local devices.json file, exclude it from sharing and source control, and treat CLI-entered passwords as exposed unless shell history and logs are controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/likong-iot/serial-server-mqtt) <br>
- [GitHub homepage](https://github.com/likong-iot/sp501lw-mqtt-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may publish MQTT messages and write local devices.json gateway records.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
