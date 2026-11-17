## Description:

Manage torrents with qBittorrent WebUI, including listing, adding, pausing, resuming, deleting, organizing, and monitoring transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricanwarfare](https://clawhub.ai/user/ricanwarfare)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage qBittorrent WebUI torrents from an agent, including adding downloads, changing torrent state, organizing categories and tags, setting speed limits, and checking transfer status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete torrents and optionally delete local files.

Mitigation: Require explicit user confirmation of the torrent hash and whether files should be removed before running delete commands.

Risk: The skill can change qBittorrent application preferences and transfer limits.

Mitigation: Limit preference changes to reviewed JSON payloads and confirm the exact setting changes before execution.

Risk: The skill handles qBittorrent WebUI credentials and session cookies.

Mitigation: Use a trusted endpoint, prefer HTTPS except for localhost, and store credential files with owner-only permissions.

## Reference(s):

- [ClawHub qBittorrent Skill](https://clawhub.ai/ricanwarfare/skills/qbittorrent-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a local shell helper that returns qBittorrent WebUI API responses or status JSON.]

## Skill Version(s):

1.0.0 (source: server evidence, SKILL.md frontmatter, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
