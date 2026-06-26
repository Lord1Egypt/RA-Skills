## Description: <br>
Interact with the TikiCow farming game to plant, water, harvest crops, manage cows, trade items, check market, weather, energy, and view leaderboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhue-ai](https://clawhub.ai/user/mhue-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and developers use this skill to let an agent operate a linked TikiCow account, plan farming and market actions, and interact with game APIs under the documented cooldown and rate-limit rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent receives a live TikiCow bearer token that can change account state. <br>
Mitigation: Generate linking codes only inside the official game, treat the returned token like a password, and avoid logging or sharing it. <br>
Risk: Autonomous actions can trade items, use energy, register bots, or otherwise alter game state. <br>
Mitigation: Require explicit approval before marketplace trades, bot registration, or other state-changing actions unless autonomous play is intended. <br>
Risk: Ignoring movement, cooldown, or rate-limit rules can cause failed actions or ineffective automation. <br>
Mitigation: Move within 30 seconds before write actions, respect the 2-second write cooldown, check energy before expensive operations, and stay within documented request limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mhue-ai/tikicow) <br>
- [Play TikiCow](https://play.tikicow.com) <br>
- [TikiCow developers](https://www.tikicow.com/developers) <br>
- [TikiCow API reference](https://api.tikicow.com/v1/agent/api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown with HTTP endpoint examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a player-generated linking code and bearer token for authenticated game actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
