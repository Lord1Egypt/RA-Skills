## Description:

Guides an agent to use UAPI's GET /game/minecraft/serverstatus endpoint to retrieve Minecraft Java server status after confirming the required server parameter and response handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when an agent needs to answer Minecraft server-status requests by checking a server address with UAPI and explaining success, failure, and quota-related responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the endpoint sends the queried Minecraft server address to uapis.cn.

Mitigation: Confirm the user intends to query that server address and avoid sending private or sensitive hostnames unless the user explicitly provides them for this lookup.

Risk: The trigger wording is broader than a server-status-only skill needs.

Mitigation: Invoke the skill only for Minecraft server-status requests and confirm the required server query parameter before preparing a call.

Risk: Anonymous or visitor quota may be exhausted.

Mitigation: If the API returns 429 or a quota-related error, explain the quota condition and suggest retrying with a free UAPI key from the provider.

## Reference(s):

- [Quick Start](references/quick-start.md)
- [查询 MC 服务器](references/operations/get-game-minecraft-serverstatus.md)
- [Game 分类接口](references/resources/Game.md)
- [UAPI service](https://uapis.cn)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown or plain text guidance with endpoint, parameter, response-code, and quota handling details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the GET /game/minecraft/serverstatus endpoint, the required server query parameter, response summaries, and UAPI key retry guidance when quota errors occur.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
