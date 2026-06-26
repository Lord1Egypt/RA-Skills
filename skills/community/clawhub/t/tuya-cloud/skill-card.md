## Description: <br>
Read sensor data and control Tuya IoT devices via Tuya Cloud API or local LAN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minshi-veyt](https://clawhub.ai/user/minshi-veyt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and home automation users use this skill to list Tuya devices, read sensor values, calculate soil-moisture averages, scan local devices, and send switch or valve commands through Tuya Cloud or local LAN control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose TUYA_ACCESS_SECRET and Tuya local_key values. <br>
Mitigation: Keep credentials and local keys out of source control, shared logs, and transcripts; store them only in local environment files or secret managers. <br>
Risk: The skill can change physical device state, including switches and water valves. <br>
Mitigation: Review every control command, device ID, DP code, and countdown value before execution, especially for valve or switch actions. <br>
Risk: The --enrich local scan mode can combine LAN discovery with cloud credentials and local control keys. <br>
Mitigation: Use --enrich only when cloud-backed device names or local keys are needed, and avoid sharing enriched scan output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/minshi-veyt/tuya-cloud) <br>
- [Publisher Profile](https://clawhub.ai/user/minshi-veyt) <br>
- [Tuya Cloud Controller Installation Guide](https://medium.com/@min.shi.happy/building-a-tuya-smart-home-controller-skill-for-openclaw-beadb796c05c) <br>
- [Tuya Developer Platform](https://platform.tuya.com) <br>
- [Tuya Europe OpenAPI Endpoint](https://openapi.tuyaeu.com) <br>
- [Tuya US OpenAPI Endpoint](https://openapi.tuyaus.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python command examples, JSON command payloads, and JSON or text command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus Tuya credentials in TUYA_ACCESS_ID and TUYA_ACCESS_SECRET for cloud operations; local read and control require device IP and local_key values.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
