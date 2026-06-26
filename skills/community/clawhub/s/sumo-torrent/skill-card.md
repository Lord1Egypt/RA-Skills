## Description: <br>
Searches BT4G for torrents, enriches magnet links with public trackers, and can add selected downloads to qBittorrent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sumo0221](https://clawhub.ai/user/sumo0221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search BT4G for torrent candidates, inspect seed activity, generate tracker-enriched magnet links, and optionally send approved downloads to a local qBittorrent WebUI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start qBittorrent downloads from selected magnet links. <br>
Mitigation: Require explicit user confirmation before adding any torrent, and verify the selected result, seed activity, and magnet link before submission. <br>
Risk: The skill may ask an agent to reuse a personal browser session to pass Cloudflare checks. <br>
Mitigation: Use a dedicated browser profile with no unrelated logins, and avoid forwarding torrent requests to another agent unless the user explicitly approves it. <br>
Risk: The qBittorrent WebUI examples use default credentials and local WebUI access. <br>
Mitigation: Change the default qBittorrent password, keep the WebUI bound to localhost, and do not expose the WebUI to the network. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sumo0221/sumo-torrent) <br>
- [BT4G search endpoint](https://bt4gprx.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated magnet-link text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce tracker-enriched magnet links and qBittorrent WebUI actions after user review.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
