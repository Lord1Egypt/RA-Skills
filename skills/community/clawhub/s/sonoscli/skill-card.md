## Description: <br>
Control Sonos speakers (discover/status/play/volume/group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare and run Sonos CLI commands for discovering speakers, checking status, controlling playback, changing volume, managing groups, using favorites, editing queues, and optionally searching Spotify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sonos commands can change playback, volume, groups, and queues in shared spaces. <br>
Mitigation: Review commands before execution and use explicit speaker names or IP addresses for mutating actions. <br>
Risk: Unpinned Go module installation may reduce reproducibility. <br>
Mitigation: Pin or review the upstream Go module when reproducible installs matter. <br>
Risk: Spotify search requires optional client credentials. <br>
Mitigation: Configure Spotify client credentials only when Spotify search is needed. <br>


## Reference(s): <br>
- [Sonos CLI homepage](https://sonoscli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/steipete/sonoscli) <br>
- [Go install module](https://pkg.go.dev/github.com/steipete/sonoscli/cmd/sonos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Sonos speaker names, IP addresses, command options, and optional Spotify credential configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
