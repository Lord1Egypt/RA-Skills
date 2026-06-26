## Description: <br>
Control Sonos speakers (discover/status/play/volume/group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahmadshouly](https://clawhub.ai/user/ahmadshouly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Sonos users use this skill to generate command-line guidance for discovering, checking, and controlling Sonos speakers on a local network. It also covers grouping, favorites, queues, optional Spotify search, and manual IP fallback when discovery fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow fetches an upstream Go module at install time. <br>
Mitigation: Install only after reviewing and trusting the upstream module; use controlled dependency review or pinning where required. <br>
Risk: The generated commands can control playback, volume, speaker grouping, and queues on reachable Sonos speakers. <br>
Mitigation: Run commands only on trusted local networks and confirm target speaker names or IP addresses before execution. <br>
Risk: Spotify search requires optional Spotify API credentials. <br>
Mitigation: Provide Spotify credentials only when Spotify search is needed and manage them through the agent environment's normal secret handling. <br>


## Reference(s): <br>
- [Sonos CLI homepage](https://sonoscli.sh) <br>
- [Sonos CLI Go install module](https://pkg.go.dev/github.com/steipete/sonoscli/cmd/sonos) <br>
- [ClawHub release page](https://clawhub.ai/ahmadshouly/sonoscli-bak) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate against Sonos speakers reachable on the local network; Spotify search requires optional Spotify credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
