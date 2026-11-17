## Description:

Look up World of Warcraft characters, Mythic+ scores, best runs, raid progression, gear, current affixes, and top runs using Raider.io, with optional Blizzard API and Warcraft Logs integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tag-assistant](https://clawhub.ai/user/tag-assistant)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve World of Warcraft character summaries, Mythic+ information, raid progression, gear details, affixes, and top run information from documented game-data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install step creates a global CLI symlink, and the reviewed artifact did not include the referenced wow executable.

Mitigation: Before installing, verify the local target that /usr/local/bin/wow will point to.

Risk: Optional Blizzard API and Warcraft Logs credentials may be stored in a plaintext config file.

Mitigation: Prefer environment variables when practical; if using ~/.config/wow/config.env, keep it out of backups and dotfile sync and restrict permissions such as chmod 600.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tag-assistant/skills/wow)
- [Blizzard API client registration](https://develop.battle.net/access/clients)
- [Warcraft Logs API client registration](https://www.warcraftlogs.com/api/clients)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and optional raw JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include live game-profile data from Raider.io and optional Blizzard API or Warcraft Logs calls when credentials are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
