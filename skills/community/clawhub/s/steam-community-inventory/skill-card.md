## Description: <br>
Retrieves Steam inventory data for a user from steamcommunity.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluesyparty-src](https://clawhub.ai/user/bluesyparty-src) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Steam users use this skill to retrieve, page through, and inspect Steam Community inventory data with curl and jq. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to handle a live Steam browser session cookie. <br>
Mitigation: Treat STEAM_COOKIES like a password: do not share it, avoid shared terminals, logs, screenshots, and persistent shell history, and invalidate the Steam session if it may have been exposed. <br>
Risk: Repeated Steam Community inventory requests may trigger rate limits or temporary IP bans. <br>
Mitigation: Use cookies only for the user's own inventory and wait at least 4 seconds between inventory or pagination requests. <br>


## Reference(s): <br>
- [Steam Community Developer Documentation](https://steamcommunity.com/dev) <br>
- [SteamID Lookup](https://steamid.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/bluesyparty-src/steam-community-inventory) <br>
- [Publisher Profile](https://clawhub.ai/user/bluesyparty-src) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with bash commands, jq examples, and JSON response-field guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, STEAM_ID, and STEAM_COOKIES.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
