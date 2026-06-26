## Description: <br>
支持站站、车次、余票查询，返回时刻、票价与余票等。当用户说：北京到上海今天还有高铁票吗？帮我查一下 G1 次列车经停站，或类似火车票、余票问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Chinese train routes, train stops, schedules, fares, and remaining ticket availability through JisuAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JisuAPI account key, which can affect quota or billing if misused or exposed. <br>
Mitigation: Use a dedicated API key where possible, monitor quota or billing, and rotate or revoke the key if it is exposed. <br>
Risk: Train query details are sent to JisuAPI when the skill performs lookups. <br>
Mitigation: Submit only the station, date, and train-number fields needed for the lookup, and avoid entering unrelated personal or sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/train) <br>
- [JisuAPI train API documentation](https://www.jisuapi.com/api/train/) <br>
- [JisuAPI homepage](https://www.jisuapi.com/) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jisuapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [JSON returned by shell-invoked Python commands, with Markdown usage and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends route, train number, and date query fields to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
