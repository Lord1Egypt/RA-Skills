## Description: <br>
Search for music via Brave Search and play it on your Sonos speakers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search for Spotify tracks through Brave Search and start playback on a named Sonos speaker from a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Brave Search API key and sends music search queries to Brave. <br>
Mitigation: Install only when that credential use and external search request flow are acceptable for the deployment environment. <br>
Risk: The skill can start playback on a named Sonos speaker and plays the first matched Spotify result without a separate confirmation step. <br>
Mitigation: Use it in spaces where automatic playback is acceptable, and review the matched track behavior before using it in shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/sonos-music-search) <br>
- [ClawHub metadata homepage](https://clawhub.com/skills/sonos-music-search) <br>
- [Brave Search API](https://brave.com/search/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output with setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, network access, a Brave Search API key, a local Sonos speaker, and Spotify linked to the Sonos system.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
