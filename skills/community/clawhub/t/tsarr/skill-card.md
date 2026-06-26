## Description: <br>
Manage home media services through TsArr from OpenClaw. Use for Radarr, Sonarr, Lidarr, Readarr, Prowlarr, Bazarr, qBittorrent, and Seerr tasks such as checking health, inspecting queues and history, browsing libraries, searching, adding, editing, deleting items, viewing profiles, tags, and root folders, managing torrents, managing media requests, and checking TsArr configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbeverhelst](https://clawhub.ai/user/robbeverhelst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to manage Servarr-based home media services through the TsArr CLI, including health checks, queue and history inspection, library browsing, search, add, edit, delete, torrent, request, and configuration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access media-service configuration files and credentials. <br>
Mitigation: Install only when the TsArr npm package and local service configuration are trusted, and avoid exposing API keys or passwords in logs, shell history, screenshots, or shared config. <br>
Risk: The skill can run delete actions, including commands that remove files. <br>
Mitigation: Review commands before execution, inspect the target item first, and reserve destructive flags such as --delete-files or non-interactive confirmation for explicit user requests. <br>


## Reference(s): <br>
- [TsArr homepage](https://github.com/robbeverhelst/tsarr) <br>
- [ClawHub skill page](https://clawhub.ai/robbeverhelst/tsarr) <br>
- [Setup](references/setup.md) <br>
- [Common Workflows](references/common-workflows.md) <br>
- [Service Cheatsheet](references/service-cheatsheet.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request confirmation before destructive actions and may prefer JSON CLI output when selecting IDs or comparing service results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
