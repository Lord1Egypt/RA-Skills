## Description:

A skill to look up video game information, prices, compatibility, and duration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanheral](https://clawhub.ai/user/ivanheral)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to query game details, compare prices, check Steam Deck and Linux compatibility, view playtime estimates, and retrieve Steam-related game data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts public game-data services and stores cached API responses locally.

Mitigation: Review network access expectations before use and clear the local skill cache when cached game data should not persist.

Risk: Installing with an @latest command can resolve to a newer release than the reviewed version.

Mitigation: Prefer a pinned or trusted ClawHub installer command for environments that require reproducible skill versions.

Risk: Default language, currency, and region settings may not match the user's locale.

Mitigation: Set STEAM_LANGUAGE, STEAM_CURRENCY, and STEAM_CC or pass the documented command-line options before running lookups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivanheral/skills/videogames)
- [Steam](https://store.steampowered.com/)
- [CheapShark](https://www.cheapshark.com/)
- [ProtonDB](https://www.protondb.com/)
- [HowLongToBeat](https://howlongtobeat.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown-oriented guidance with command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live public game-data results and links; no external Python packages are required.]

## Skill Version(s):

1.0.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
