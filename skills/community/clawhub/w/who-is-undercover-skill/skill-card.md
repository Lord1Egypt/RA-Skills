## Description: <br>
Who Is Undercover Skill lets OpenClaw users play the social deduction game with 4-10 players, AI opponents, role assignment, description rounds, voting, and win detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq5776569](https://clawhub.ai/user/qq5776569) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to run an interactive AI-assisted version of the party game Who Is Undercover, including game setup, player turns, status updates, descriptions, voting, and result handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Under-disclosed remote game-service code is present despite documentation saying the skill runs locally without network requests. <br>
Mitigation: Review before installing; document the external service and data sent, and make remote play an explicit opt-in. <br>
Risk: The artifact includes a hardcoded InStreet API key. <br>
Mitigation: Ask the publisher to remove and rotate the embedded key and require user-provided credentials through a documented configuration path. <br>
Risk: Running the remote game controller can create and operate an external InStreet room. <br>
Mitigation: Do not run instreet_game_controller.js unless remote room creation and operation are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qq5776569/who-is-undercover-skill) <br>
- [Project homepage](https://github.com/long5/who-is-undercover) <br>
- [Publisher profile](https://clawhub.ai/user/qq5776569) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text and Markdown game messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive turn-based game state, role, status, description, vote, and result responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
