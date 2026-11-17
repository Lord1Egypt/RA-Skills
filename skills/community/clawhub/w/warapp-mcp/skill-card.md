## Description:

Advises players on war.app multiplayer strategy games by summarizing game state, maps, opponents, and possible picks and turns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

War.app players use this skill to check their games, understand maps and opponents, and plan picks and turns. It can also help with game chat and diplomacy actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can accept a surrender without asking when accepting would win the game, ending that game.

Mitigation: Review and decide whether this automatic win condition is acceptable before installation; require an explicit user decision for other pending surrender acceptances.

## Reference(s):

- [warapp-mcp on ClawHub](https://clawhub.ai/chrischall/skills/warapp-mcp)
- [war.app API token instructions](https://war.app/API/GetAPIToken)

## Skill Output:

**Output Type(s):** [Text, Guidance, Analysis]

**Output Format:** [Natural-language game summaries, strategy guidance, and proposed picks or turn orders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans are presented for review before turn submission.]

## Skill Version(s):

0.5.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
