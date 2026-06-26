## Description: <br>
WittIoT气象站数据查询，支持WittStation系列气象站，提供实时温湿度、气压、光照、风速风向、降雨量等传感器数据查询，以及24小时/7天/30天历史趋势查询。也支持通过设备短码（shortcode）免登录查询公开气象站数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wittiot](https://clawhub.ai/user/wittiot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query WittIoT weather stations for current sensor readings, historical trends, device lists, and public station data by shortcode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs a WittIoT API key for private account data and may expose weather-station information to the agent runtime. <br>
Mitigation: Set WITTIOT_API_KEY as an environment variable or managed secret, avoid pasting it into chat or plaintext config, and revoke the key from WittIoT if exposed. <br>
Risk: Public shortcode queries can return data for public weather stations without authentication. <br>
Mitigation: Use shortcodes only for stations intended to be public and avoid sharing private station identifiers in prompts or logs. <br>


## Reference(s): <br>
- [WittIoT API Specification](references/api-spec.md) <br>
- [WittIoT](https://wittiot.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script output for the agent to summarize] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python helper emits JSON for devices, realtime readings, history records, shortcode results, errors, and device-selection prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
