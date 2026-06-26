## Description: <br>
使用积智数据 VIN 车型解析 API，通过 17 位 VIN 车架号查询车辆的车型信息：如品牌、车型、车系、年款、销售类型、发动机、变速箱等信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polaris2013](https://clawhub.ai/user/polaris2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up vehicle model details from a 17-character VIN and summarize fields such as brand, model, year, engine, transmission, and drivetrain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VINs are sent to a third-party lookup service and may be sensitive vehicle identifiers. <br>
Mitigation: Use only when the user is comfortable sharing the VIN with the configured service, and avoid sending unnecessary or unrelated personal data. <br>
Risk: The skill requires an API key for the external service. <br>
Mitigation: Store JZ_API_KEY in the environment or a secret manager, and do not paste it into prompts, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/polaris2013/vincartype) <br>
- [Publisher profile](https://clawhub.ai/user/polaris2013) <br>
- [VIN car type API endpoint](https://erp.qipeidao.com/jzOpenClaw/getVinCarType) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON response from a Python CLI, with agent-facing text summaries expected after use] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JZ_API_KEY environment variable; sends VIN values to the configured third-party lookup service.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
