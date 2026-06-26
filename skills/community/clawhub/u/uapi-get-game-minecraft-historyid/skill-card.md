## Description: <br>
使用 UAPI 的查询 MC 曾用名接口，帮助 agents prepare calls to GET /game/minecraft/historyid and understand its parameters, response modes, and common errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to look up Minecraft username history through UAPI by username or UUID, with guidance on required query parameters and response handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may cause an agent to use this skill for Minecraft server status or general player-profile requests instead of name-history lookups. <br>
Mitigation: Use it only when the user asks for Minecraft name history, and verify that returned data is name-history data before relying on it. <br>
Risk: Anonymous or free UAPI quota can be exhausted, which may cause 429 responses or similar quota errors. <br>
Mitigation: If quota errors occur, ask the user to provide a UAPI key or retry after confirming account and quota status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuakami/uapi-get-game-minecraft-historyid) <br>
- [Quick Start](references/quick-start.md) <br>
- [查询 MC 曾用名](references/operations/get-game-minecraft-historyid.md) <br>
- [Game 分类接口](references/resources/Game.md) <br>
- [UAPI](https://uapis.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with endpoint details and query-parameter instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or prepare GET /game/minecraft/historyid requests using a Minecraft username or UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
