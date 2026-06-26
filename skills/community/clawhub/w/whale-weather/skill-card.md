## Description: <br>
全球城市天气查询与对比工具。支持中英文城市名，具备多语言输出、动态数据源切换（Open-Meteo）及精准大城市定位功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redapp](https://clawhub.ai/user/redapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query current weather for one city or compare multiple cities in Chinese or English, including temperature, humidity, wind, precipitation probability, and travel advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups send the supplied city name or lookup term to Open-Meteo over the network. <br>
Mitigation: Use the skill only when sharing the queried location with Open-Meteo is acceptable. <br>
Risk: The skill runs local shell scripts and invokes python3 to fetch live weather data. <br>
Mitigation: Review the included scripts before installation and run them from the skill directory as documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redapp/whale-weather) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [Open-Meteo geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text weather summaries from shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can be localized to Chinese or English; scripts require python3 and network access to Open-Meteo.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
