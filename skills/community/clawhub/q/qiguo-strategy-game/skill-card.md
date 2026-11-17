## Description:

Launches a bundled browser strategy game with campaign and skirmish modes, AI opponents, same-device two-player play, and optional online matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmily741963](https://clawhub.ai/user/hmily741963)

### License/Terms of Use:

MIT-0

## Use Case:

Players use this skill to open a Chinese-language, turn-based strategy game in a browser, choosing a campaign or quick battle against AI or another player.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted participants in cross-device matches may tamper with gameplay or inject browser-rendered content.

Mitigation: Use cross-device multiplayer only with trusted participants; otherwise play locally or use same-device modes.

Risk: A network-accessible multiplayer relay may be exhausted by unauthenticated peers.

Mitigation: Do not expose the optional relay to an untrusted network; restrict access to trusted participants.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hmily741963/skills/qiguo-strategy-game)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [Playable HTML game files and brief launch instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Game progress is stored locally in the browser; cross-device play requires an optional relay.]

## Skill Version(s):

1.5.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
