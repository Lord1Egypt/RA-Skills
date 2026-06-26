## Description: <br>
Manage torrents with qBittorrent WebUI API, including listing, adding, pausing, resuming, deleting, and monitoring torrent activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricanwarfare](https://clawhub.ai/user/ricanwarfare) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to manage qBittorrent WebUI sessions from an agent, including torrent lifecycle actions, transfer monitoring, categories, tags, and speed limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can delete torrents and downloaded files through destructive qBittorrent actions. <br>
Mitigation: Require explicit user confirmation before delete operations, especially when the --files option is present. <br>
Risk: The agent can change persistent qBittorrent application preferences. <br>
Mitigation: Review or remove set-preferences access unless preference changes are required for the deployment. <br>
Risk: The skill uses qBittorrent WebUI credentials and session cookies. <br>
Mitigation: Store credentials and session files in owner-only locations and scope the WebUI account to the minimum permissions practical. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ricanwarfare/qbittorrent-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/ricanwarfare) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses qBittorrent WebUI credentials and can change torrent state, application preferences, and downloaded files when invoked with destructive options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
