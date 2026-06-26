## Description: <br>
使用 UAPI 的“程序员历史事件”单接口 skill，处理程序员历史事件查询，并指导代理调用 GET /history/programmer。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to decide when and how to call UAPI's programmer-history endpoint for a specific month and day. It helps confirm required query parameters, authentication expectations, and documented response codes before making the lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad "programmer" trigger could activate in conversations that are not asking for programmer-history events. <br>
Mitigation: Confirm the user request is specifically about historical programmer events before allowing an API call. <br>
Risk: Authentication or quota errors may require a UAPI key. <br>
Mitigation: Provide a UAPI key only for this service when quota or authentication requires it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shuakami/uapi-get-history-programmer) <br>
- [UAPI base URL](https://uapis.cn/api/v1) <br>
- [UAPI account and key portal](https://uapis.cn) <br>
- [Quick start](references/quick-start.md) <br>
- [GET /history/programmer operation](references/operations/get-history-programmer.md) <br>
- [Misc category reference](references/resources/Misc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown guidance with endpoint, query parameter, authentication, and response-code details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead an agent to call a read-only UAPI endpoint with month and day query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
