## Description:

Uses UAPI's GET /game/minecraft/userinfo endpoint to look up a Minecraft player's UUID and skin URL from a provided Minecraft username.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they need an agent to prepare or explain a UAPI Minecraft player lookup. It helps confirm the required username query parameter, expected response fields, and common error responses before calling the endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be selected too broadly because its routing keywords include general Minecraft terms such as userinfo, server status, and name history.

Mitigation: Use it only for Minecraft player username lookups, and confirm ambiguous requests before sending a username to UAPI.

Risk: Requests without a confirmed Minecraft username can produce failed calls or unintended lookup targets.

Mitigation: Confirm the required username query parameter before calling the endpoint.

Risk: The endpoint can return quota or upstream-service errors.

Mitigation: Handle documented 429-style quota guidance and 502 upstream failures by explaining the retry or account-key path rather than treating the result as a player lookup failure.

## Reference(s):

- [Skill release page](https://clawhub.ai/shuakami/skills/uapi-get-game-minecraft-userinfo)
- [UAPI service](https://uapis.cn)
- [UAPI base URL](https://uapis.cn/api/v1)
- [Quick start](references/quick-start.md)
- [查询 MC 玩家](references/operations/get-game-minecraft-userinfo.md)
- [Game 分类接口](references/resources/Game.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions]

**Output Format:** [Markdown with endpoint details, parameter guidance, and response handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or describe a GET request to /game/minecraft/userinfo with a required username query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
