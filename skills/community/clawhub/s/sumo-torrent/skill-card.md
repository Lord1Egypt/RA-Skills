## Description:

Searches BT4G for torrents, generates tracker-enriched magnet links, and can add selected magnet links or torrent files to a local qBittorrent Web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumo0221](https://clawhub.ai/user/sumo0221)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting users with authorized torrent workflows use this skill to search BT4G, identify active results, enrich magnet links with public trackers, and optionally submit a chosen download to qBittorrent after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can reuse a personal browser profile or session to bypass site challenges.

Mitigation: Use an isolated browser profile dedicated to this site and do not reuse a personal daily profile.

Risk: The helper can directly add magnet links or torrent files to qBittorrent.

Mitigation: Require explicit user confirmation before adding any magnet link or torrent file to the client.

Risk: The qBittorrent helper includes weak default credentials and accepts credentials through command-line flags.

Mitigation: Change the qBittorrent password, keep the Web UI bound to localhost, and avoid passing passwords on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sumo0221/skills/sumo-torrent)
- [Publisher profile](https://clawhub.ai/user/sumo0221)
- [qBittorrent Web UI](http://localhost:8080)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated magnet-link text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add public trackers to magnet links and interact with a local qBittorrent Web UI when configured.]

## Skill Version(s):

1.0.4 (source: server release evidence, released 2026-04-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
