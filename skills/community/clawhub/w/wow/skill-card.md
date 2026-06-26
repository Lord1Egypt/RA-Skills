## Description: <br>
Look up World of Warcraft characters, including Mythic+ scores, best runs, raid progression, gear, and more, using Raider.io with optional Blizzard API and Warcraft Logs integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tag-assistant](https://clawhub.ai/user/tag-assistant) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up World of Warcraft character profiles, Mythic+ scores, current affixes, top runs, raid summaries, gear information, and optional armory or parse data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install metadata symlinks a separate wow CLI that was not included in the reviewed artifact. <br>
Mitigation: Install only if the local wow executable is trusted, and review the executable and destination path before creating the symlink. <br>
Risk: Optional Blizzard and Warcraft Logs credentials may be provided through environment variables or a local config file. <br>
Mitigation: Prefer environment variables or a protected config file with restrictive permissions, and avoid exposing credentials in shared logs or outputs. <br>
Risk: Character names, realms, regions, and optional API credentials may be sent to third-party game-data services. <br>
Mitigation: Use the skill only when sharing that lookup data with Raider.io, Blizzard, or Warcraft Logs is acceptable for the user and environment. <br>


## Reference(s): <br>
- [Blizzard API Client Management](https://develop.battle.net/access/clients) <br>
- [Warcraft Logs API Clients](https://www.warcraftlogs.com/api/clients) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq, relies on third-party game-data services, and may use optional Blizzard or Warcraft Logs credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
