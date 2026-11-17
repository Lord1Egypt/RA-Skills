## Description:

使用 UAPI 的“查询 Steam 用户”单接口 skill，帮助代理确认参数、鉴权、返回码，并准备调用 GET /game/steam/summary 查询公开 Steam 用户资料摘要。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user asks to look up a Steam profile or account summary through UAPI. It supports choosing the correct GET /game/steam/summary endpoint, checking Steam identifier parameters, and handling authentication or common response codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Steam Web API key can be supplied as a URL query parameter to a third-party UAPI service.

Mitigation: Prefer backend-held credentials or safer header or secret handling, and avoid exposing personal keys in client URLs or logs.

Risk: Implicit invocation is enabled for broad Steam profile lookup requests.

Mitigation: Confirm the request is specifically for a Steam profile lookup and ensure a supported Steam identifier is available before invocation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shuakami/skills/uapi-get-game-steam-summary)
- [Quick Start](references/quick-start.md)
- [查询 Steam 用户](references/operations/get-game-steam-summary.md)
- [Game 分类接口](references/resources/Game.md)
- [UAPI](https://uapis.cn)
- [UAPI Base URL](https://uapis.cn/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with API endpoint details, parameter notes, and response-code handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include using a third-party UAPI endpoint and handling a Steam Web API key safely.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
