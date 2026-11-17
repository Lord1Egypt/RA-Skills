## Description:

Provides a QuecPython Modbus IoT framework for multi-sensor data collection, 4G reporting, cloud integration, and OTA updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbs2016](https://clawhub.ai/user/lbs2016)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create and customize QuecPython IoT device projects that read Modbus RTU sensors and report data over 4G to a cloud platform. It is aimed at gas monitoring, temperature and humidity monitoring, water quality monitoring, power monitoring, and other industrial sensor collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deploying the template unchanged can send identifiable device telemetry to preset services.

Mitigation: Replace default reporting and OTA endpoints with approved services before deployment and avoid sending raw IMSI, ICCID, or IMEI unless required.

Risk: Remote OTA behavior may accept updates without visible safeguards in the artifact.

Mitigation: Disable OTA until explicitly provisioned, then require signed and allowlisted update files.

Risk: Copying template files directly into a device /usr directory can overwrite an existing deployment.

Mitigation: Back up device files and review configuration changes before copying files to the device.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lbs2016/skills/tianjin-anxinhuarui-gas-monitoring-iot)
- [Artifact README](artifact/README.md)
- [Skill usage guide](artifact/技能使用说明.md)
- [Deployment guide](artifact/template/docs/部署指南.md)
- [Configuration guide](artifact/template/docs/配置说明.md)
- [Debugging guide](artifact/template/docs/调试指南.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code snippets, shell commands, and project configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a QuecPython project template and customization guidance for Modbus sensor, HTTP reporting, OTA, and deployment settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
