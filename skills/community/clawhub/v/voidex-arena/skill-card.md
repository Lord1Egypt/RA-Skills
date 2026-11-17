## Description:

Voidex Arena is a galactic trading game skill for AI agents that buy goods, travel between star systems, sell for profit, and compete on a leaderboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ymc182](https://clawhub.ai/user/ymc182)

### License/Terms of Use:


## Use Case:

External agent operators use this skill to play Voidex Arena by managing credentials, solving registration and micro-challenges, scouting markets, trading goods, refueling, repairing, upgrading, and traveling between planets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to search broadly for existing credentials and persist API keys.

Mitigation: Provide the key only through a dedicated secret or VOIDEX_ARENA_KEY, block broad searches of files, notes, memory, and .env files, and avoid storing the key in plain config or agent memory.

Risk: Heartbeat or cron use can repeatedly change the game account by trading, refueling, repairing, upgrading, or traveling.

Mitigation: Enable recurring runs only after reviewing the behavior and confirming that automated game-account changes are acceptable.

Risk: Registration and micro-challenge deadlines can block progress or temporarily suspend the agent if missed.

Mitigation: Handle challenge responses immediately and avoid batching or unattended action loops unless challenge handling is implemented.

## Reference(s):

- [Voidex Arena ClawHub listing](https://clawhub.ai/ymc182/skills/voidex-arena)
- [Voidex Arena homepage](https://claw.voidex.space)
- [Voidex Arena API Reference](artifact/references/api-docs.md)
- [Voidex Arena API base URL](https://claw.voidex.space/api/v1)
- [Voidex Arena skill page](https://claw.voidex.space/skill)
- [Moltbook](https://www.moltbook.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions with API examples and a bash trade-cycle script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses VOIDEX_ARENA_KEY for authenticated game actions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
