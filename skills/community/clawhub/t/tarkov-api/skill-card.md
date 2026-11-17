## Description:

Security-focused Tarkov.dev and optional EFT Wiki assistant for live Escape from Tarkov lookups, stash valuation, trader flip screening, map-risk scoring, and raid-kit recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cole-z](https://clawhub.ai/user/cole-z)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Tarkov.dev and, when needed, the EFT Wiki for game status, item economy, ammo, task, map, stash, and raid-planning decisions. It is intended for concise gameplay guidance with data evidence and uncertainty notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Tarkov.dev and EFT Wiki requests can return stale, unavailable, or community-edited data.

Mitigation: Use the API as the primary structured source, use wiki checks only when needed, and note uncertainty or in-game verification for patch-sensitive details.

Risk: Alternate endpoints may expose the agent to untrusted API responses.

Mitigation: Keep default allowlisted endpoints and use --allow-unsafe-endpoint only when the user intentionally trusts the alternate endpoint.

Risk: Raw GraphQL queries and large lookups can broaden data access or cause slow requests.

Mitigation: Prefer preset commands, validate raw query scope and variables, and keep limits bounded for routine lookups.

Risk: Trader flip and map-risk outputs are heuristic snapshots that may be invalidated by fees, limits, market movement, spawn randomness, or patches.

Mitigation: Present these results as decision support, not guarantees, and remind users to verify high-impact choices in game.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cole-z/skills/tarkov-api)
- [Tarkov.dev GraphQL API](https://api.tarkov.dev/graphql)
- [Escape from Tarkov Wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki)
- [Query Cookbook](references/query-cookbook.md)
- [Security Model](references/security-model.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make live outbound requests to Tarkov.dev and, conditionally, the EFT Wiki; can read user-provided JSON or CSV stash files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
