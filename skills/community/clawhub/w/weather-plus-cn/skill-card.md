## Description:

Weather Plus Cn helps agents query Chinese city weather from China Weather Network and provide temperature, weather-condition, clothing-advice, and lifestyle-index guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchaoqun](https://clawhub.ai/user/chenchaoqun)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers can use this skill to answer China city weather, temperature, forecast, travel-preparation, and clothing-advice requests.

### Deployment Geography for Use:

Global; primarily supports China city weather queries.

## Known Risks and Mitigations:

Risk: Weather data is fetched over unencrypted HTTP from weather.com.cn.

Mitigation: Avoid using this skill for safety-critical severe-weather decisions unless the data source is moved to HTTPS and fetched content is treated as untrusted.

Risk: Weather pages may change format or become unavailable, causing failed or incomplete parsing.

Mitigation: Check the returned source data before relying on the summary and fall back to direct page review or another weather source when parsing fails.

Risk: The skill is scoped mainly to Chinese cities and may not handle overseas weather requests well.

Mitigation: Use the documented fallback source for overseas cities or route those requests to a broader weather skill.

## Reference(s):

- [China Weather Network](http://www.weather.com.cn)
- [China Weather Network City List](http://www.weather.com.cn/citylist/)
- [City Codes Reference](references/city_codes.md)
- [ClawHub Skill Page](https://clawhub.ai/chenchaoqun/skills/weather-plus-cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown or plain text with weather summaries, clothing advice, lifestyle indices, and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language weather output; network access is required for live weather data.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
