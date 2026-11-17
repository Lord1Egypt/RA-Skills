## Description:

中文天气查询工具 - 使用中国天气网获取实时天气（无需API密钥，不依赖大模型）

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenera](https://clawhub.ai/user/kenera)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer Chinese city weather questions by running a local Bash script that looks up city codes, fetches weather.com.cn pages, and returns current weather and lifestyle indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell script evaluates weather data fetched from the internet as shell code, creating command-execution risk.

Mitigation: Remove eval and parse fetched HTML as untrusted text before routine use; review the script before installing.

Risk: The skill depends on live access to weather.com.cn, so unavailable or delayed source data can affect results.

Mitigation: Confirm important weather decisions against an authoritative forecast source when network access fails or stale data is suspected.

## Reference(s):

- [China Weather Network](https://www.weather.com.cn/)
- [ClawHub skill listing](https://clawhub.ai/kenera/skills/weather-cn)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with formatted Chinese weather fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and grep; queries weather.com.cn; uses a local city-code map.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
