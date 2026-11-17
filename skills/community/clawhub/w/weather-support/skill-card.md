## Description:

国内天气查询技能 - 基于uapis.cn免费API。支持全国3000+城市，无需注册和API密钥。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouwenbin2000](https://clawhub.ai/user/zhouwenbin2000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer weather questions for Chinese cities and districts. It queries uapis.cn and returns current weather details such as city, conditions, temperature, wind, humidity, and report time.

### Deployment Geography for Use:

Global, with practical coverage for cities and districts in China

## Known Risks and Mitigations:

Risk: City names entered for weather lookup are sent to the external uapis.cn API.

Mitigation: Avoid private or sensitive location queries when that disclosure is not acceptable.

## Reference(s):

- [uapis.cn weather API example](https://uapis.cn/api/v1/misc/weather?city=北京)
- [ClawHub skill page](https://clawhub.ai/zhouwenbin2000/skills/weather-support)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with weather fields; may include curl commands when showing API usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and sends city names to the public uapis.cn weather API; no API key is required.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
