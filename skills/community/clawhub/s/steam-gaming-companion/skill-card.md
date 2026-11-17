## Description:

Steam & PC Gaming Companion provides Steam Web API workflows for library management, play recommendations, wishlist sale monitoring, achievement tracking, and game information lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduardmirko390-crypto](https://clawhub.ai/user/eduardmirko390-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External Steam users use this skill to help an agent inspect their Steam library, surface backlog and achievement status, monitor public wishlist sales, and recommend games based on mood and available play time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Steam API credentials and a Steam ID, giving the agent access to public Steam library, wishlist, and achievement data.

Mitigation: Install only when that account data exposure is acceptable, keep credentials in environment variables or a secret manager, and rotate keys if they are exposed.

Risk: The documented Twitch OAuth token command can expose a Twitch client secret if pasted or logged directly.

Mitigation: Use a safer prompt or secret manager for the client secret, and rotate the secret afterward if it may have been exposed.

Risk: Optional IGDB lookups may send searched or library-derived game titles to Twitch or IGDB APIs.

Mitigation: Enable IGDB only when external game-title lookup disclosure is acceptable for the user.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/eduardmirko390-crypto/skills/steam-gaming-companion)
- [ClawHub publisher profile](https://clawhub.ai/user/eduardmirko390-crypto)
- [Steam Web API key registration](https://steamcommunity.com/dev/apikey)
- [Steam owned games API endpoint](https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/)
- [Steam achievement API endpoint](https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/)
- [Steam store app details API endpoint](https://store.steampowered.com/api/appdetails?appids={appid})
- [Steam wishlist data endpoint](https://store.steampowered.com/wishlist/profiles/{STEAM_ID}/wishlistdata/)
- [Twitch developer console for IGDB credentials](https://dev.twitch.tv/console/apps)
- [Twitch OAuth token endpoint](https://id.twitch.tv/oauth2/token)
- [IGDB games API endpoint](https://api.igdb.com/v4/games)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown responses with inline shell commands, API request details, tables, and concise guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Steam API credentials and optional IGDB credentials supplied by the user; responses may include personalized library, wishlist, achievement, and game metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
