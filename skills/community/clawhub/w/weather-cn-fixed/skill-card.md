## Description: <br>
中文天气查询工具 - 使用中国天气网获取实时天气（无需API密钥，不依赖大模型） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziqi-jin](https://clawhub.ai/user/ziqi-jin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to query real-time Chinese weather for supported city names from China Weather without an API key or model-based parsing. <br>

### Deployment Geography for Use: <br>
Global; weather lookup coverage is focused on cities in China. <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports command-execution risk because weather-cn.sh evaluates parsed website data as shell code. <br>
Mitigation: Patch the script to avoid eval, parse only expected fields explicitly, and treat website responses as untrusted before installing or running the skill. <br>
Risk: Weather results depend on live access to China Weather and may be delayed or unavailable when the site or local network is unavailable. <br>
Mitigation: Check network access to www.weather.com.cn, keep weather_codes.txt current, and treat weather and lifestyle indexes as informational guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziqi-jin/weather-cn-fixed) <br>
- [China Weather](https://www.weather.com.cn/) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=39.9042&longitude=116.4074&current_weather=true&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia%2FShanghai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text terminal weather output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and grep; uses a city-code mapping file for supported Chinese cities.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
