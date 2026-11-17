## Description:

Interact with the TikiCow farming game to plant, water, harvest crops, manage cows, trade items, check market, weather, energy, and view leaderboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhue-ai](https://clawhub.ai/user/mhue-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Players and agent developers use this skill to operate a linked TikiCow game account through documented API actions for farming, cow care, trading, weather-aware planning, energy checks, and leaderboard participation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A linked agent can make ongoing changes to the user's TikiCow account, including purchases, sales, listings, batch actions, and bot registration.

Mitigation: Install only when account operation is intended, generate linking codes yourself, protect bearer tokens, and require confirmation before write-heavy or market-facing actions.

Risk: Game actions can fail or waste resources when the agent skips movement, ignores cooldowns, or acts without checking energy and market conditions.

Mitigation: Move before each write action, respect documented rate limits and cooldowns, check energy before expensive actions, and use the status endpoint for current farm, market, weather, and energy state.

## Reference(s):

- [TikiCow skill page](https://clawhub.ai/mhue-ai/skills/tikicow)
- [Play TikiCow](https://play.tikicow.com)
- [TikiCow Developers](https://www.tikicow.com/developers)
- [TikiCow API reference](https://api.tikicow.com/v1/agent/api-reference)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration]

**Output Format:** [Markdown with API endpoint examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a human-generated linking code and bearer token for account-changing actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
