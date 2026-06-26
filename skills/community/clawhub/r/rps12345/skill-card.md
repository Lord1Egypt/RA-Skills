## Description: <br>
Play a text-based game of rock-paper-scissors against the user and keep score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YoavRez](https://clawhub.ai/user/YoavRez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to play a short conversational rock-paper-scissors game with scorekeeping inside the current chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to be chat-only and should not access files, tools, the network, credentials, or persistent memory. <br>
Mitigation: Install and run it only in contexts where the agent follows the supplied chat-only behavior and does not grant tool or filesystem access for this game. <br>
Risk: The game host may choose moves in a way that feels patterned rather than fair. <br>
Mitigation: Have the agent vary rock, paper, and scissors choices across rounds and avoid fixed repeating patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YoavRez/rps12345) <br>
- [Publisher profile](https://clawhub.ai/user/YoavRez) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown conversation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scoreboard text and short prompts remain in the current conversation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
