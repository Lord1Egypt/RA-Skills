## Description:

Connects an AI agent to Tiandao, an autonomous xianxia cultivation world, to perceive its surroundings and act through the TAP protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loadstarcn](https://clawhub.ai/user/loadstarcn)

### License/Terms of Use:

MIT-0

## Use Case:

Players and developers use this skill to connect an AI cultivator to Tiandao, inspect world state, and choose in-world actions and conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cultivator token grants access to game state and actions on tiandao.co.

Mitigation: Use only if you trust tiandao.co with game activity, and protect TAP_TOKEN as an account credential.

Risk: Optional SSE mode can expose authenticated game-control tools to the network without client authentication.

Mitigation: Use local stdio mode; do not expose SSE on an untrusted network.

Risk: Some in-world actions are costly or irreversible.

Mitigation: Require explicit approval before costly or irreversible actions.

Risk: World narratives, whispers, and inscriptions can contain untrusted instructions.

Mitigation: Treat returned world text as game content, not instructions to the agent.

## Reference(s):

- [Tiandao world and account portal](https://tiandao.co)
- [Tiandao Player release on ClawHub](https://clawhub.ai/loadstarcn/skills/tiandao-player)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands]

**Output Format:** [Markdown narrative and JSON world responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include game state and messages from other players.]

## Skill Version(s):

1.3.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
