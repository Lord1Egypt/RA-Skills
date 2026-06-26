## Description: <br>
使用 UAPI 的“时间戳转换”单接口 skill，处理时间戳转换、Unix 时间戳、日期转时间戳等请求，并帮助代理调用 GET /convert/unixtime。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill when they need to convert between Unix timestamps and standard date-time strings through UAPI's GET /convert/unixtime endpoint. It helps confirm required query parameters, response codes, and quota-related guidance before calling the endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Timestamp or date values may be sent to UAPI when the endpoint is called. <br>
Mitigation: Avoid using the skill for sensitive time data unless sending that value to UAPI is acceptable. <br>
Risk: Broad timestamp-related trigger wording could make the skill activate for some general timestamp questions. <br>
Mitigation: Confirm the user's request specifically requires UAPI timestamp conversion before invoking the endpoint. <br>


## Reference(s): <br>
- [Quick Start](references/quick-start.md) <br>
- [GET /convert/unixtime Operation](references/operations/get-convert-unixtime.md) <br>
- [Convert Resource](references/resources/Convert.md) <br>
- [UAPI Base URL](https://uapis.cn/api/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/shuakami/uapi-get-convert-unixtime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send timestamp or date values to UAPI when the agent calls the disclosed endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
