## Description: <br>
基于 QuecPython 平台的 Modbus IoT framework for building cellular sensor devices that collect Modbus RTU data, report JSON payloads over 4G, integrate with cloud endpoints, and support OTA updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbs2016](https://clawhub.ai/user/lbs2016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and IoT engineers use this skill to scaffold and customize QuecPython Modbus RTU device projects for gas, temperature, water quality, power, and other industrial sensor monitoring scenarios. It helps configure reporting endpoints, Modbus parameters, sensor parsing, deployment files, and troubleshooting steps for compatible QuecPython hardware. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default reporting and OTA endpoints may send operational data or fetch updates from unintended services. <br>
Mitigation: Replace all default URL_REPORT and URL_OTA values with approved endpoints before testing or deployment. <br>
Risk: OTA behavior can remotely update firmware and reboot deployed devices. <br>
Mitigation: Disable or tightly control OTA unless signed firmware, rollback procedures, and operational approval are in place. <br>
Risk: Generated device payloads can include IMEI, IMSI, ICCID, and other cellular identifiers. <br>
Mitigation: Send identifiers only when required, redact them from logs, and verify data-handling requirements for the deployment. <br>
Risk: Autostart or reboot behavior can disrupt production hardware if configuration is wrong. <br>
Mitigation: Test on non-production QuecPython hardware and review generated code before enabling autostart or field deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lbs2016/tianjin-anxinhuarui-gas-monitoring-iot) <br>
- [artifact/README.md](artifact/README.md) <br>
- [artifact/技能使用说明.md](artifact/技能使用说明.md) <br>
- [artifact/template/docs/部署指南.md](artifact/template/docs/部署指南.md) <br>
- [artifact/template/docs/配置说明.md](artifact/template/docs/配置说明.md) <br>
- [artifact/template/docs/调试指南.md](artifact/template/docs/调试指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets, shell commands, configuration examples, and deployment checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces QuecPython project templates and instructions intended for review and customization before deployment to hardware.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
