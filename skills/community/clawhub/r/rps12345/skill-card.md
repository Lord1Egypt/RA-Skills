## Description:

Play a text-based game of rock-paper-scissors against the user and keep score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoavrez](https://clawhub.ai/user/yoavrez)

### License/Terms of Use:


## Use Case:

External users use this skill to play a short conversational rock-paper-scissors game, choose match length, submit moves, and track the score in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be available as an always-present skill.

Mitigation: Only start the game when the user explicitly asks to play or directly invokes the skill; ask a clarifying question for ambiguous mentions.

Risk: The game could drift beyond its intended conversational scope.

Mitigation: Keep play inside the current chat and do not use tools, files, accounts, networking, or long-term memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoavrez/skills/rps12345)
- [Publisher profile](https://clawhub.ai/user/yoavrez)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Chat messages with round results and compact score summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No files, tool calls, network access, or persistence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
