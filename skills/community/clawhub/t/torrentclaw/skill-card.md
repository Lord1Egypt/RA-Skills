## Description: <br>
TorrentClaw helps agents search movie and TV torrents, present metadata-rich results, and add selected magnets to Transmission or aria2 or provide magnet and .torrent alternatives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buryni](https://clawhub.ai/user/buryni) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to find media torrents, compare quality and seed information, and hand a selected magnet or torrent file to a local torrent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Torrent search and download workflows can expose privacy, legal, and system-impact risks. <br>
Mitigation: Confirm the exact torrent, file size, legality, and download location before allowing add or download actions. <br>
Risk: The skill can add a selected magnet to local torrent software. <br>
Mitigation: Require user confirmation before running add-torrent actions and prefer explicit download directories. <br>
Risk: API keys may increase rate limits and should not be exposed in logs or URLs. <br>
Mitigation: Use the TORRENTCLAW_API_KEY environment variable only when needed and pass it through an Authorization header. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/buryni/torrentclaw) <br>
- [TorrentClaw Homepage](https://torrentclaw.com) <br>
- [Repository](https://github.com/torrentclaw/torrentclaw-skill) <br>
- [API Reference](references/api-reference.md) <br>
- [OpenAPI Spec](https://torrentclaw.com/api/openapi.json) <br>
- [API Docs](https://torrentclaw.com/api/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, JSON snippets, and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include magnet links, torrent-file URLs, torrent-client detection JSON, and installation guidance.] <br>

## Skill Version(s): <br>
0.1.17 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
