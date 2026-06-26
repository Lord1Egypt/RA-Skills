## Description: <br>
国内天气查询技能 - 基于uapis.cn免费API。支持全国3000+城市，无需注册和API密钥。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouwenbin2000](https://clawhub.ai/user/zhouwenbin2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query real-time weather for cities and districts in China through the uapis.cn weather API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City or district names are sent to uapis.cn for weather lookup. <br>
Mitigation: Avoid querying locations considered sensitive, and disclose this external API use to users when relevant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouwenbin2000/weather-support) <br>
- [uapis.cn weather API example](https://uapis.cn/api/v1/misc/weather?city=北京) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls] <br>
**Output Format:** [Plain text or Markdown with weather fields returned from JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; sends the requested city or district name to uapis.cn; no API key is required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
