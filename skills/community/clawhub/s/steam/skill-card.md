## Description:

Browse, filter, and discover games in a Steam library by playtime, reviews, Steam Deck compatibility, genres, and tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjrussell](https://clawhub.ai/user/mjrussell)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query a configured Steam library, filter games by playtime, reviews, Steam Deck compatibility, tags, and genres, and produce game recommendations or library summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and invoking the steam-games-cli package.

Mitigation: Confirm trust in the npm package and publisher before installation, avoid elevated privileges, and consider pinning a reviewed package version or using an isolated local install.

Risk: The configured Steam API key and Steam ID can be used to query Steam account and library metadata.

Mitigation: Configure credentials only in trusted environments, avoid exposing them in logs or shared transcripts, and rotate the API key if it may have been disclosed.

## Reference(s):

- [Steam Games CLI ClawHub Skill](https://clawhub.ai/mjrussell/skills/steam)
- [Steam Web API Key Setup](https://steamcommunity.com/dev/apikey)
- [Project Homepage](https://github.com/mjrussell/steam-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples; CLI output may be colored tables, plain text, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the steam CLI binary and STEAM_API_KEY configuration.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
