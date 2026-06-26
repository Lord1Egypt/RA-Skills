## Description: <br>
中文天气查询工具 - 使用中国天气网获取实时天气（无需API密钥，不依赖大模型） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenera](https://clawhub.ai/user/kenera) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query current weather for supported Chinese cities from China Weather using a local Python script and city-code table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts weather.com.cn when used for Chinese city weather queries. <br>
Mitigation: Install and use it only in environments where outbound access to weather.com.cn is allowed. <br>
Risk: The optional shell alias changes the user's command-line environment. <br>
Mitigation: Add the alias only after reviewing the path and deciding that a shortcut command is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenera/weather-zh) <br>
- [China Weather](https://www.weather.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and the requests package; no API key is required.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
