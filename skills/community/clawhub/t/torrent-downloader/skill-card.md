## Description: <br>
Search magnet links for movies and TV shows, rank results by subtitle availability and resolution, and send the selected magnet link to qBittorrent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d19310](https://clawhub.ai/user/d19310) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search torrent indexes for movie or TV magnet links, rank candidates by subtitles and resolution, and add the selected result to a configured qBittorrent Web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically add a torrent to qBittorrent after ranking search results. <br>
Mitigation: Require the agent to show the selected title, source, size, and magnet link, then obtain explicit user approval before starting a download. <br>
Risk: The qBittorrent Web UI defaults in the artifact use common local credentials. <br>
Mitigation: Change the default qBittorrent credentials before use and keep the Web UI bound to a trusted local address. <br>
Risk: Torrent search and download activity may expose users to unwanted or unauthorized content. <br>
Mitigation: Install only when torrent search and qBittorrent control are intentional, and review each selected result before download. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/d19310/torrent-downloader) <br>
- [SolidTorrents search API](https://solidtorrents.to/api/v1/search?q={query}&sort=seeders) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes query, total count, ranked results, magnet links, titles, scores, sizes, seeders, leechers, and source; download output reports qBittorrent add status or recent torrent status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
