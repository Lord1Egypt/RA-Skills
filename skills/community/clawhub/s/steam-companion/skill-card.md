## Description:

Reusable Steam gaming companion for profiles, library insights, recommendations, wishlist tracking, achievement context, game lookups, reviews, setup verification, and preference memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franciscoagx](https://clawhub.ai/user/franciscoagx)

### License/Terms of Use:

MIT-0

## Use Case:

Steam users and gaming assistants use this skill to summarize profiles, libraries, wishlists, achievements, game metadata, and setup status. It helps generate grounded play recommendations, review context, and preference-aware guidance from Steam data and local profile memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Steam profile data and local preference memory may expose personal gaming activity or preferences.

Mitigation: Install only in environments where connecting Steam-related data to the assistant is acceptable, and avoid shared service configurations unless the host enforces per-user profile access.

Risk: Private, restricted, or unavailable Steam data can make summaries and recommendations incomplete.

Mitigation: Treat empty or missing payloads as a privacy or availability signal, disclose the limitation, and avoid filling gaps with guesses.

Risk: The skill depends on steam-mcp and STEAM_API_KEY configuration for live Steam data.

Mitigation: Use setup verification before relying on live results, and fall back to existing conversation context when the MCP server or credentials are unavailable.

## Reference(s):

- [Steam Companion on ClawHub](https://clawhub.ai/franciscoagx/skills/steam-companion)
- [steam-mcp MCP server](https://github.com/franciscoagx/steam-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or structured text for Steam profile, library, wishlist, achievement, lookup, setup, recommendation, and review contexts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on accessible Steam data, steam-mcp availability, Steam privacy settings, and locally saved preference memory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact constants.ts)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
