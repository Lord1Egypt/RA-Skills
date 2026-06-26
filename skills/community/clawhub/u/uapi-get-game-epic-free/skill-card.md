## Description: <br>
使用 UAPI 的 Epic 免费游戏单接口 skill，帮助 agents 判断、准备并调用 GET /game/epic-free 来查询 Epic Games 当前免费游戏信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route Epic free-game requests to the UAPI GET /game/epic-free endpoint, confirm that no explicit parameters are required, and explain response codes or quota handling before presenting results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad trigger can activate the skill for general game-information questions. <br>
Mitigation: Use explicit Epic free-game wording when invoking this skill, and narrow trigger terms in a future release. <br>
Risk: Anonymous or visitor quota can be exhausted before the endpoint returns results. <br>
Mitigation: When quota errors occur, ask the user to register with UAPI, create a free UAPI Key, and retry with that key. <br>
Risk: The external Epic free-games service can be temporarily unavailable. <br>
Mitigation: Check response codes and clearly report temporary service failures before retrying later. <br>


## Reference(s): <br>
- [Quick Start](references/quick-start.md) <br>
- [Epic 免费游戏 Operation](references/operations/get-game-epic-free.md) <br>
- [Game Resource](references/resources/Game.md) <br>
- [UAPI API Base URL](https://uapis.cn/api/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/shuakami/uapi-get-game-epic-free) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown guidance with endpoint, parameter, authentication, response-code, and quota-handling details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare a GET request to /game/epic-free and summarize returned free-game information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
