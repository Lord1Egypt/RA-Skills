## Description:

使用 UAPI 的“程序员历史事件”单接口 skill，处理 程序员历史事件 等请求。 Use when the user wants get history programmer, history programmer, programmer, or when you need to call GET /history/programmer directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to identify and call UAPI's programmer-history endpoint. It helps confirm required month and day query parameters, authentication or quota handling, and expected response codes before requesting programmer-related historical events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact uapis.cn to retrieve programmer-history events.

Mitigation: Review outbound API use before deployment and ensure users understand requests go to UAPI.

Risk: Anonymous quota may be exhausted and the skill may ask for a UAPI key.

Mitigation: Use a scoped UAPI key only when needed, and avoid exposing the key in prompts, logs, or shared outputs.

Risk: Broad trigger terms such as programmer may invoke the skill when a user did not intend to call this endpoint.

Mitigation: Prefer exact programmer-history intent or narrow invocation triggers during deployment.

## Reference(s):

- [Programmer History Endpoint](references/operations/get-history-programmer.md)
- [Quick Start](references/quick-start.md)
- [Misc Category](references/resources/Misc.md)
- [UAPI Base API](https://uapis.cn/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/shuakami/skills/uapi-get-history-programmer)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GET /history/programmer query parameters, response-code guidance, and UAPI key or quota handling notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
