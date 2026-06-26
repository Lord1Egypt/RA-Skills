## Description: <br>
Gets current weather and forecasts through Moji Weather or MSN Weather for weather, temperature, and forecast questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer weather, temperature, and forecast questions for locations by checking Moji Weather first and MSN Weather as a fallback or cross-check. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather requests and location names may be visible to Moji Weather or MSN Weather. <br>
Mitigation: Use this skill only when those providers are acceptable for the requested location, and avoid sending sensitive location details. <br>
Risk: The skill overrides the built-in weather flow and is not intended for historical weather, severe weather alerts, or detailed meteorological analysis. <br>
Mitigation: Use a dedicated weather-alert, historical-weather, or meteorological source when those outputs are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/weather-cn-zh) <br>
- [Moji Weather](https://tianqi.moji.com/) <br>
- [MSN Weather](https://www.msn.cn/zh-cn/weather/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with sourced weather summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source attribution and cross-check notes when weather providers differ.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
