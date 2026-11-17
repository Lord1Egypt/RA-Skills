## Description:

按城市与日期查询历史天气（温湿度、风、气压、AQI 等）。当用户说：去年今天北京多少度？查一下 2023 年 7 月上海历史天气，或类似历史气温问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query JisuAPI historical weather by city name or city ID and date, then summarize weather, temperature, humidity, pressure, wind, sunrise/sunset, and AQI fields for end users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City/date queries and the JISU_API_KEY are sent to JisuAPI over HTTPS.

Mitigation: Install only if that data sharing is acceptable, keep the API key scoped to JisuAPI, and rotate it if exposed.

Risk: The skill depends on a user-provided JisuAPI credential for successful operation.

Mitigation: Configure JISU_API_KEY as an environment variable and avoid embedding the key in prompts, source files, or shared command history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/weather2)
- [JisuAPI historical weather API](https://www.jisuapi.com/api/weather2/)
- [JisuAPI provider site](https://www.jisuapi.com/)
- [JisuAPI weather2 endpoint](https://api.jisuapi.com/weather2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command examples; runtime script output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
