## Description: <br>
按城市与日期查询历史天气（温湿度、风、气压、AQI 等），用于回答类似“去年今天北京多少度”或“2023 年 7 月上海历史天气”这类问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up historical weather by city or city ID and date, then summarize temperature, humidity, wind, pressure, AQI, and related fields for natural-language answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JisuAPI app key and sends city/date weather queries to JisuAPI. <br>
Mitigation: Use a dedicated key with quota limits and avoid including unnecessary sensitive context in queries. <br>
Risk: The Python script depends on the local requests package. <br>
Mitigation: Install dependencies from a trusted package source and run the skill in a controlled environment. <br>


## Reference(s): <br>
- [Historical Weather API](https://www.jisuapi.com/api/weather2/) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/weather2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends city/date weather queries to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
