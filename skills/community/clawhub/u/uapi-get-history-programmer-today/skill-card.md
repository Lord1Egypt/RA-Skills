## Description: <br>
使用 UAPI 的“程序员历史上的今天”单接口 skill，处理 程序员历史上的今天 等请求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to decide when and how to call UAPI's GET /history/programmer/today endpoint for programmer-history-today requests. It helps confirm the endpoint, authentication posture, response codes, and whether the request matches this single-interface skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad keyword "today" may route unrelated conversations to this skill and cause unnecessary external API calls. <br>
Mitigation: Use the skill only when the user is asking for programmer-history-today information or explicitly wants the UAPI GET /history/programmer/today endpoint. <br>
Risk: Anonymous UAPI usage may be rate limited or require authentication for continued access. <br>
Mitigation: Start with public access when appropriate, then add a dedicated UAPI key only if the service returns quota, rate-limit, or authentication errors. <br>


## Reference(s): <br>
- [Quick Start](references/quick-start.md) <br>
- [程序员历史上的今天](references/operations/get-history-programmer-today.md) <br>
- [Misc 分类接口](references/resources/Misc.md) <br>
- [UAPI](https://uapis.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/shuakami/uapi-get-history-programmer-today) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown guidance with endpoint, parameter, authentication, and response-code details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The wrapped endpoint has no explicit parameters and is usually callable directly; a UAPI key may be needed if anonymous quota is exhausted or authentication is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
