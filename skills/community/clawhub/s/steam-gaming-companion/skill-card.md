## Description: <br>
Steam & PC Gaming Companion provides Steam Web API workflows for library management, play recommendations, wishlist sale monitoring, achievement tracking, and game information lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eduardmirko390-crypto](https://clawhub.ai/user/eduardmirko390-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to let an agent inspect their Steam library, achievements, wishlist, and game metadata, then return backlog summaries, recommendations, sale checks, progress reports, rankings, and setup diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Steam API key and Steam ID, and it queries Steam profile, library, wishlist, and achievement data. <br>
Mitigation: Install only when that access is acceptable, keep credentials scoped to this use, and revoke or rotate API tokens when the skill is no longer needed. <br>
Risk: Optional IGDB credentials send game lookup queries to IGDB/Twitch. <br>
Mitigation: Leave IGDB_CLIENT_ID and IGDB_ACCESS_TOKEN unset if those third-party lookups are not desired. <br>
Risk: Wishlist and achievement features can be limited by private Steam profile or game-detail settings. <br>
Mitigation: Keep Steam privacy settings aligned with the intended feature use and rely on the skill's setup diagnostics before querying data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eduardmirko390-crypto/steam-gaming-companion) <br>
- [Steam Web API key registration](https://steamcommunity.com/dev/apikey) <br>
- [SteamID lookup](https://steamid.io) <br>
- [Twitch developer console for IGDB credentials](https://dev.twitch.tv/console/apps) <br>
- [Steam owned games API](https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/) <br>
- [IGDB games API](https://api.igdb.com/v4/games) <br>
- [Steam Store app details API](https://store.steampowered.com/api/appdetails?appids={appid}) <br>
- [Steam wishlist data endpoint](https://store.steampowered.com/wishlist/profiles/{STEAM_ID}/wishlistdata/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with setup commands, API request examples, tables, progress summaries, recommendations, and error diagnostics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Steam API key and 64-bit Steam ID; optional IGDB credentials enrich game metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
