## Description: <br>
Queries historical events, births, deaths, and related date-based history records for a supplied month and day using JisuAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to answer user questions about what happened on a specific calendar date by retrieving same-day historical records and summarizing selected results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the configured API key and requested date to the disclosed third-party JisuAPI service. <br>
Mitigation: Use a dedicated JisuAPI key where possible and follow the provider's and organization's data-sharing requirements. <br>
Risk: Responses can depend on third-party API availability, quota, and returned historical data quality. <br>
Mitigation: Handle API errors and quota failures gracefully, and verify important historical claims before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/todayhistory) <br>
- [JisuAPI Today History API](https://www.jisuapi.com/api/todayhistory/) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from the helper script, typically summarized by the agent as Markdown or plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, and a configured JISU_API_KEY.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
