## Description: <br>
Weather Plus Cn queries China city weather information from China Weather Network and returns temperature, conditions, clothing advice, and lifestyle indices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchaoqun](https://clawhub.ai/user/chenchaoqun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to answer Chinese city weather questions, prepare for travel, and generate clothing advice from current forecast data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on network access to weather.com.cn or wttr.in, so requests can fail or return stale data. <br>
Mitigation: Check connectivity, retry later, and treat results as current weather guidance rather than authoritative emergency or safety advice. <br>
Risk: City-code lookup or HTML parsing can fail when the requested city code is wrong or the source page structure changes. <br>
Mitigation: Verify city codes against the bundled city-code reference and review page content manually when parsing fails. <br>
Risk: The bundled security evidence is clean, but the skill can propose network fetches and shell commands. <br>
Mitigation: Review commands before execution and run only the weather-query actions needed for the requested city. <br>


## Reference(s): <br>
- [China Weather Network](http://www.weather.com.cn) <br>
- [China Weather Network City List](http://www.weather.com.cn/citylist/) <br>
- [China Weather Network City Codes](references/city_codes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/chenchaoqun/weather-plus-cn) <br>
- [Publisher Profile](https://clawhub.ai/user/chenchaoqun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style weather summary with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes city, current conditions, temperature, wind, clothing advice, and lifestyle indices when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
