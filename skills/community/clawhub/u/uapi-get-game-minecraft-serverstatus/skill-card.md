## Description: <br>
使用 UAPI 的“查询 MC 服务器”单接口 skill，处理查询 MC 服务器、MC服务器状态等请求，并帮助 agents prepare calls to GET /game/minecraft/serverstatus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to identify and prepare a UAPI Minecraft Java server status lookup, including required server parameters, response codes, and quota handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Minecraft server addresses provided by users may be sent to the external UAPI service. <br>
Mitigation: Tell users before lookup when the server address is sensitive, and avoid sending private or internal server addresses without confirmation. <br>
Risk: Broad routing keywords may attract Minecraft player lookup or name-history requests that this skill does not support. <br>
Mitigation: Use the skill only for Minecraft server status lookups and redirect unsupported player or name-history requests to an appropriate capability. <br>
Risk: Anonymous UAPI quota can be exhausted and cause request failures. <br>
Mitigation: When 429 or quota errors occur, suggest registering for a UAPI key and retrying with the key. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/shuakami/uapi-get-game-minecraft-serverstatus) <br>
- [快速上手](references/quick-start.md) <br>
- [查询 MC 服务器](references/operations/get-game-minecraft-serverstatus.md) <br>
- [Game 分类接口](references/resources/Game.md) <br>
- [UAPI](https://uapis.cn) <br>
- [UAPI API base URL](https://uapis.cn/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with endpoint, parameter, authentication, and response-code details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the server query parameter and UAPI quota or key guidance when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
