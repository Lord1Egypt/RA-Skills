## Description: <br>
Use when working with qBittorrent Web API - adding torrents, managing downloads, checking status, or any qBittorrent automation task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HxBreak](https://clawhub.ai/user/HxBreak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to operate the qBittorrent Web API, including authentication, adding and managing torrents, checking status, and configuring categories, tags, trackers, RSS, and search behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential examples and .env usage could expose qBittorrent credentials if copied into version control or shared logs. <br>
Mitigation: Replace all sample credentials, keep .env out of version control, and avoid allowing the agent to inspect unrelated secrets. <br>
Risk: Mutating qBittorrent API operations can delete torrents or files, change global preferences, shut down qBittorrent, or install and remove search plugins. <br>
Mitigation: Require explicit user confirmation before destructive or broad operations, especially deleting files, using hashes=all, shutting down qBittorrent, changing global preferences, or modifying search plugins. <br>


## Reference(s): <br>
- [qBittorrent OpenAPI documentation](https://www.qbittorrent.org/openapi-demo/) <br>
- [qBittorrent WebUI API Wiki](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)) <br>
- [qBittorrent Web API changelog](https://github.com/qbittorrent/qBittorrent/blob/master/WebAPI_Changelog.md) <br>
- [ClawHub skill page](https://clawhub.ai/HxBreak/qbittorrent-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with curl examples, endpoint tables, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include qBittorrent API calls that mutate torrents, files, preferences, RSS feeds, or search plugins.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
