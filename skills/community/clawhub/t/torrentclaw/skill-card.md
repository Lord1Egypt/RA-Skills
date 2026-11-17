## Description:

TorrentClaw helps agents search movies and TV shows across torrent sources, present metadata-enriched torrent results, and add selected magnet links to local torrent clients or provide magnet and .torrent download options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buryni](https://clawhub.ai/user/buryni)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use TorrentClaw to search for media torrents, compare quality and seeder metadata, and route a chosen torrent to Transmission, aria2, a magnet link, or a .torrent file workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate local torrent downloads through Transmission or aria2.

Mitigation: Require explicit user approval before adding any magnet link, downloading any .torrent file, or starting a torrent client.

Risk: Torrent searches and selected torrent actions may be sent to TorrentClaw.

Mitigation: Tell users what activity will be sent to TorrentClaw and avoid using the skill for sensitive torrent activity unless the user accepts that disclosure.

Risk: The documented MCP path uses an unpinned npx package command.

Mitigation: Pin and review the MCP package version before running it.

## Reference(s):

- [TorrentClaw website](https://torrentclaw.com)
- [TorrentClaw repository](https://github.com/torrentclaw/torrentclaw-skill)
- [TorrentClaw API Reference](references/api-reference.md)
- [OpenAPI specification](https://torrentclaw.com/api/openapi.json)
- [API documentation](https://torrentclaw.com/api/docs)
- [MCP server documentation](https://torrentclaw.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON API responses and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include magnet links, .torrent download commands, torrent-client installation guidance, and local client-detection JSON.]

## Skill Version(s):

0.1.17 (source: skill metadata, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
