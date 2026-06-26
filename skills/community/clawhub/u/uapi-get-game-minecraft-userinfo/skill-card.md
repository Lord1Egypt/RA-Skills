## Description: <br>
使用 UAPI 的“查询 MC 玩家”单接口 skill，处理 查询 MC 玩家、Minecraft玩家查询 等请求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare or perform a UAPI Minecraft player lookup by username and understand required parameters, response codes, quota handling, and returned profile fields such as UUID and skin URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has overbroad routing keywords, including Minecraft server status and name history, while the documented endpoint only performs player userinfo lookup. <br>
Mitigation: Use this skill only for Minecraft player profile/userinfo lookup by username; use a separate tool for server status or name history. <br>
Risk: Requests may involve user-provided player identifiers or quota-related credentials. <br>
Mitigation: Avoid sharing unrelated personal data or any UAPI key unless the service specifically requires it for quota limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuakami/uapi-get-game-minecraft-userinfo) <br>
- [Quick start](references/quick-start.md) <br>
- [GET /game/minecraft/userinfo operation](references/operations/get-game-minecraft-userinfo.md) <br>
- [Game resource overview](references/resources/Game.md) <br>
- [UAPI service](https://uapis.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown guidance with endpoint, parameter, response, and error-handling details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a prepared GET request for https://uapis.cn/api/v1/game/minecraft/userinfo using the required username query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
