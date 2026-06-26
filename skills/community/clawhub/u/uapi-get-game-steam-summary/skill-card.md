## Description: <br>
使用 UAPI 的 GET /game/steam/summary 接口查询 Steam 用户公开资料摘要，并帮助确认参数、鉴权要求和返回码。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to look up a Steam user's public profile summary through UAPI and choose the correct query identifier before making the request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording could cause the skill to be selected for Steam tasks that are not user profile summary lookups. <br>
Mitigation: Invoke it only when the user request is specifically about a Steam user or profile summary. <br>
Risk: A Steam Web API key may be exposed if it is passed through an unsafe client-side flow. <br>
Mitigation: Use a backend-managed key when possible, and only pass a user-provided key when it is necessary for the request. <br>
Risk: Private profiles, invalid identifiers, or upstream Steam issues can produce missing data or error responses. <br>
Mitigation: Check the documented response codes and report lookup failures without inferring hidden profile details. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shuakami/uapi-get-game-steam-summary) <br>
- [查询 Steam 用户](references/operations/get-game-steam-summary.md) <br>
- [快速上手](references/quick-start.md) <br>
- [Game 分类接口](references/resources/Game.md) <br>
- [UAPI Base URL](https://uapis.cn/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, text] <br>
**Output Format:** [Markdown or plain text guidance with request parameters and response handling notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Steam profile lookup; may require a Steam Web API key or UAPI key when authentication or quota limits require it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
