## Description:

Generates and customizes QuecPython code templates that read Anxin Huarui AX100 gas detector controller data through RS485/Modbus RTU and report JSON payloads to customer HTTP platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbs2016](https://clawhub.ai/user/lbs2016)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and field engineers use this skill to adapt AX100 gas monitoring device code for customer platform URLs, reporting intervals, JSON formats, Modbus register maps, and QuecPython deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The template includes automatic OTA behavior with a hardcoded default update endpoint.

Mitigation: Disable or replace the default OTA endpoint, and require signed update manifests plus hash verification before applying updates or rebooting devices.

Risk: The template may share device identifiers such as IMEI, ICCID, or IMSI more broadly than a deployment requires.

Mitigation: Minimize transmitted identifiers and confirm the customer explicitly requires each identifier before including it in telemetry or OTA requests.

Risk: Incorrect customer-specific URL, reporting interval, GPIO, or Modbus register settings can produce missing or misleading gas monitoring reports.

Mitigation: Confirm deployment parameters against the target platform protocol, module hardware documentation, and controller register table before installation.

## Reference(s):

- [Code guide](references/code_guide.md)
- [ClawHub skill page](https://clawhub.ai/lbs2016/skills/tianjin-anxinhuarui-gas-monitoring-iot-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/lbs2016)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown containing generated or modified QuecPython files, configuration values, deployment steps, and occasional command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May output only a modified config.py for simple deployments or full Python template files when payload or device behavior changes are requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
