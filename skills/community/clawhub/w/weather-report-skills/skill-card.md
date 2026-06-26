## Description: <br>
天气播报格式化技能。当用户询问天气、查看天气预报、或需要生成天气报告时触发。技能包含完整的天气信息格式化模板，支持今天/明天/后天三种类型，以及时间段的斜体规则。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhjx94264](https://clawhub.ai/user/zhjx94264) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch Tianjin weather data and format Chinese weather reports for today, tomorrow, or the day after tomorrow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes a live request to wttr.in and may disclose the queried location to that public weather service. <br>
Mitigation: Confirm that live lookup and the location are appropriate before use, and adjust the hardcoded Tianjin location when needed. <br>


## Reference(s): <br>
- [Weather Report Template](references/weather_template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhjx94264/weather-report-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Chinese Markdown weather report with tables, emoji, separators, and bullet summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses wttr.in weather data for Tianjin by default and applies time-sensitive formatting for past time blocks when reporting today's weather.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
