## Description:

Uses UAPI's Epic free-games endpoint to help an agent handle requests for current Epic Games free-game information through GET /game/epic-free.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare or execute requests for current Epic Games free-game information via UAPI. It helps agents confirm the single endpoint, no-parameter request shape, expected response codes, and quota or API-key handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on uapis.cn for Epic free-game data, so the external service or the documented 500 response can prevent a result.

Mitigation: Confirm the endpoint response and clearly report service-unavailable failures instead of presenting stale or guessed game data.

Risk: Anonymous UAPI quota may be exhausted and the workflow may require a UAPI key.

Mitigation: Request a user-provided UAPI key only after an explicit quota error or 429 response, and avoid exposing the key in user-facing output.

Risk: A broad game-information request could be routed to this narrow Epic free-games endpoint by mistake.

Mitigation: Confirm the user is specifically asking for Epic free games before applying this skill.

## Reference(s):

- [Epic 免费游戏](references/operations/get-game-epic-free.md)
- [快速上手](references/quick-start.md)
- [Game 分类接口](references/resources/Game.md)
- [UAPI](https://uapis.cn)

## Skill Output:

**Output Type(s):** [guidance, text, API calls]

**Output Format:** [Markdown or plain text with endpoint details and response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UAPI quota guidance and documented response-code handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
