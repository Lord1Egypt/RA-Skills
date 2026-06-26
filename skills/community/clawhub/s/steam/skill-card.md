## Description: <br>
Browse, filter, and discover games in a Steam library by playtime, reviews, Steam Deck compatibility, genres, and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjrussell](https://clawhub.ai/user/mjrussell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect a Steam library, filter games, and produce game recommendations such as what to play next or what works on Steam Deck. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Steam API key and Steam ID to read Steam profile and library data. <br>
Mitigation: Use a revocable Steam API key, avoid exposing it in chats or logs, and revoke or remove it when the skill is no longer needed. <br>
Risk: The skill depends on the external steam-games-cli package and steam binary being installed. <br>
Mitigation: Install only from a trusted package source and verify the CLI before using it with account-related credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mjrussell/steam) <br>
- [Steam Web API Key](https://steamcommunity.com/dev/apikey) <br>
- [Skill Homepage](https://github.com/mjrussell/steam-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI results may be colored tables, plain text, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the steam CLI binary plus STEAM_API_KEY and a Steam ID; JSON output is available for scripting.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
