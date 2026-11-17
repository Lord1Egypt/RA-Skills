## Description:

Manage home media services through TsArr from OpenClaw. Use for Radarr, Sonarr, Lidarr, Readarr, Prowlarr, Bazarr, qBittorrent, Seerr, and Jellyfin tasks such as checking health, inspecting queues and history, browsing libraries, searching, adding, editing, deleting items, viewing profiles, tags, and root folders, managing torrents, managing media requests, triggering library scans, reading watched state, checking active playback sessions, fixing missing or poor cover images, and checking TsArr configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbeverhelst](https://clawhub.ai/user/robbeverhelst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate home media services through the tsarr CLI, including health checks, library inspection, queue and history review, searches, adds, edits, deletes, torrent management, request handling, Jellyfin playback and library tasks, and configuration checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs and relies on an unpinned tsarr npm executable.

Mitigation: Install only when the current and future tsarr package publisher is trusted, and consider pinning or independently reviewing the CLI package before use in sensitive environments.

Risk: The skill can guide destructive media-service actions such as deleting media, deleting torrents with files, changing watched state, approving or declining requests, controlling playback sessions, and starting or stopping Jellyfin tasks.

Mitigation: Require the agent to list or fetch the exact target first, summarize the destructive effect, and obtain explicit confirmation before executing mutating commands or using --yes.

Risk: The skill requires credentials or configuration for home media services.

Mitigation: Use the documented local or user config files and service environment variables carefully, avoid exposing secrets in chat output, and inspect effective configuration with tsarr config commands when troubleshooting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/robbeverhelst/skills/tsarr)
- [TsArr Repository](https://github.com/robbeverhelst/tsarr)
- [Setup](references/setup.md)
- [Common Workflows](references/common-workflows.md)
- [Service Cheatsheet](references/service-cheatsheet.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks and concise operational summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command flags, service names, item IDs, instance selectors, and warnings before destructive operations.]

## Skill Version(s):

1.0.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
