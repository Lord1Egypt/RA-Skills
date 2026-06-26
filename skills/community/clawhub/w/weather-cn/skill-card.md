## Description: <br>
中文天气查询工具 - 使用中国天气网获取实时天气（无需API密钥，不依赖大模型）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenera](https://clawhub.ai/user/kenera) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to query current weather for supported Chinese cities from China Weather, using a local shell script instead of an API key or large-model call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell script evaluates parsed remote weather page text as shell code, creating an avoidable local command execution risk. <br>
Mitigation: Patch the parser to remove eval, assign only expected fields safely, and review the script before routine use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenera/weather-cn) <br>
- [China Weather](https://www.weather.com.cn/) <br>
- [Artifact README](artifact/README.md) <br>
- [City code mapping](artifact/weather_codes.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal weather report with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and grep; accepts a supported Chinese city name; no API key is required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
