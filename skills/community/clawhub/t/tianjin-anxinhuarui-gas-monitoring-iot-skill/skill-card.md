## Description: <br>
Generates, customizes, and deploys QuecPython code for reading Anxin Huarui AX100 gas-controller data over Modbus RTU and reporting it to a customer HTTP platform at a configurable interval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbs2016](https://clawhub.ai/user/lbs2016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and field engineers use this skill to adapt a QuecPython template for AX100 gas alarm controllers, including customer upload URLs, reporting frequency, JSON payload shape, Modbus register addresses, and device deployment steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The template includes enabled-by-default remote OTA behavior that can download files and reboot deployed devices. <br>
Mitigation: Disable URL_OTA unless the operator controls and trusts the update service, require authenticated and integrity-checked OTA packages before enabling updates, and test on non-production devices first. <br>
Risk: OTA checks and platform reporting can include device identifiers and gas telemetry such as IMEI, IMSI, ICCID, signal strength, and detector readings. <br>
Mitigation: Confirm the receiving platform is authorized for these data types and remove unnecessary telemetry from OTA checks or customer payloads. <br>


## Reference(s): <br>
- [AX100 code structure guide](references/code_guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/lbs2016/tianjin-anxinhuarui-gas-monitoring-iot-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with customized QuecPython code snippets or complete Python files and deployment guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typically emits a modified config.py, may modify main.py payload logic, and may reference unchanged template files for deployment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
