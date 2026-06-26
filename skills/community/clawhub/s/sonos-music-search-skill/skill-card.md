## Description: <br>
Search for music via Brave Search and play it on Sonos speakers, with support for playback, current-track lookup, and speaker discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Spotify track results through Brave Search and control playback on Sonos speakers on their local network. It can also report the current track and list discovered speakers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can discover Sonos speakers on the local network and control playback. <br>
Mitigation: Install it only in environments where local speaker discovery and playback control are acceptable, and confirm the target speaker before playback commands. <br>
Risk: Speaker discovery output may include local device IP addresses. <br>
Mitigation: Avoid sharing logs or command output when they include local network device details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/sonos-music-search-skill) <br>
- [ClawDIS homepage](https://clawhub.com/skills/sonos-music-search-skill) <br>
- [Brave Search API](https://brave.com/search/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Configuration] <br>
**Output Format:** [Plain text CLI status messages and JavaScript object results, with Markdown usage examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRAVE_API_KEY and at least one Sonos speaker on the same local network.] <br>

## Skill Version(s): <br>
1.1.1 (source: evidence.json release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
