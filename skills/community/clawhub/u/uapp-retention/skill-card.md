## Description: <br>
友盟 U-App 留存率查询技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 1 个只读留存接口，覆盖新增/活跃用户的次日/3日/7日/14日/30日留存率查询、版本与渠道维度的留存对比分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product analysts use this skill to query Umeng U-App retention data for an appkey, including 1-day, 3-day, 7-day, 14-day, and 30-day retention by date, version, or channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local umeng-cli authentication and may send telemetry that includes the user's appkey before the requested retention query. <br>
Mitigation: Review before installing, authenticate only in an approved local environment, and do not allow automatic umeng-cli trace calls with an appkey unless the user explicitly consents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squall0925/uapp-retention) <br>
- [umeng-cli project homepage](https://github.com/umeng/umeng-cli) <br>
- [Umeng website](https://www.umeng.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses umeng-cli with a required appkey and date range; retention windows are extracted from the returned retentionRate array.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
