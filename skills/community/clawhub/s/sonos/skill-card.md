## Description: <br>
Control Sonos speakers with commands for discovery, status, playback, volume, grouping, favorites, queues, and optional Spotify search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maddydci45-svg](https://clawhub.ai/user/maddydci45-svg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate Sonos speakers on a local network, including playback, volume, grouping, favorites, queue actions, and optional Spotify search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control Sonos speakers on the local network, including playback, volume, grouping, and queue clearing. <br>
Mitigation: Review agent prompts before allowing speaker-control actions, especially volume changes, grouping changes, and queue-clearing commands. <br>
Risk: Optional Spotify Web API search may require Spotify credentials in the environment. <br>
Mitigation: Provide Spotify credentials only when needed, keep them out of prompts and logs, and prefer scoped or disposable credentials where possible. <br>
Risk: The Go install target uses a latest-version module reference, which may change over time. <br>
Mitigation: Pin the Go module version when reproducible installs are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maddydci45-svg/sonos) <br>
- [Publisher profile](https://clawhub.ai/user/maddydci45-svg) <br>
- [Sonos CLI homepage](https://sonoscli.sh) <br>
- [sonoscli Go module](https://pkg.go.dev/github.com/steipete/sonoscli/cmd/sonos) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the sonos binary and local network access to Sonos speakers; optional Spotify Web API search uses SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
