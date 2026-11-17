## Description:

Use when working with qBittorrent Web API - adding torrents, managing downloads, checking status, or any qBittorrent automation task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hxbreak](https://clawhub.ai/user/hxbreak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill as a qBittorrent Web API reference for torrent management, status checks, file operations, categories, tags, RSS, search, and automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples include unsafe credential handling and weak defaults for qBittorrent access.

Mitigation: Use a safer secret mechanism, replace weak defaults, and restrict API access to HTTPS or localhost-only connections.

Risk: Deletion, shutdown, plugin install or uninstall, and bulk actions can have high operational impact.

Mitigation: Require explicit user confirmation before these actions, especially before deleteFiles=true or actions that target all torrents.

Risk: Shared or persistent cookie files can expose authenticated qBittorrent sessions.

Mitigation: Use a private temporary cookie jar and remove it after the API workflow completes.

## Reference(s):

- [qBittorrent OpenAPI Demo](https://www.qbittorrent.org/openapi-demo/)
- [qBittorrent WebUI API Wiki](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1))
- [qBittorrent Web API Changelog](https://github.com/qbittorrent/qBittorrent/blob/master/WebAPI_Changelog.md)
- [ClawHub Skill Page](https://clawhub.ai/hxbreak/skills/qbittorrent-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with endpoint tables and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes curl examples, API endpoint summaries, parameter notes, workflow guidance, and troubleshooting notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
