## Description:

Searches magnet links for movies and TV shows, ranks results by subtitle availability and resolution, and downloads the selected result through qBittorrent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d19310](https://clawhub.ai/user/d19310)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search torrent indexes for movie or TV magnet links, rank candidates by subtitle and resolution preferences, and send a selected magnet link to qBittorrent for download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically start downloads through qBittorrent after ranking torrent search results.

Mitigation: Require explicit approval before adding any magnet link and review the selected title, size, seeders, and source.

Risk: Default qBittorrent credentials and credentialed Web UI access can expose downloader control if left unchanged or reachable on an untrusted network.

Mitigation: Use dedicated non-default qBittorrent credentials and keep QBT_URL on loopback or HTTPS.

Risk: Torrent search results may point to unsafe, misleading, or unauthorized content.

Mitigation: Use the skill only where torrent downloading is permitted and inspect selected results before download.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/d19310/skills/torrent-downloader)
- [SolidTorrents search API endpoint](https://solidtorrents.to/api/v1/search?q={query}&sort=seeders)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON search results plus plain-text download status and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses qBittorrent connection settings from environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
