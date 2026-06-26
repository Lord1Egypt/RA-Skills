## Description: <br>
Fetch recent game updates from Steam News for tracked Steam games, including patch notes, updates, and news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PatFitzner](https://clawhub.ai/user/PatFitzner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to fetch, list, and maintain recent public Steam news for a configurable set of tracked games. It helps an agent resolve Steam apps, manage the tracked-game list, and summarize newly discovered game updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public Steam endpoints and stores local tracking history for configured games and discovered updates. <br>
Mitigation: Run it with awareness of the Steam network calls, and remove the local config and data files when retained update history is no longer wanted. <br>


## Reference(s): <br>
- [Steam News API endpoint](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/) <br>
- [Steam Community app search endpoint](https://steamcommunity.com/actions/SearchApps/) <br>
- [Steam Store app details endpoint](https://store.steampowered.com/api/appdetails) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON files for tracked games, last-run state, and accumulated update records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
