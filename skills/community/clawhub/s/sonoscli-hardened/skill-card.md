## Description: <br>
Control Sonos speakers (discover/status/play/volume/group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Sonos CLI commands that control local-network speakers while preserving guardrails for destructive actions, credentials, volume, and speaker data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Go installer pulls the current upstream sonoscli module. <br>
Mitigation: Review the upstream module before installation and consider pinning a known version in controlled environments. <br>
Risk: Queue clearing, grouping changes, and high-volume changes can disrupt speakers or remove queued playback. <br>
Mitigation: Require explicit user confirmation in the current conversation before destructive or high-volume commands. <br>
Risk: Spotify credential values could be exposed during troubleshooting. <br>
Mitigation: Do not echo, print, hash, substring, or otherwise display SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET. <br>
Risk: Sonos command output can reveal speaker names, IP addresses, playback state, queue contents, and local network topology. <br>
Mitigation: Keep raw Sonos output local and do not pipe, redirect, or transmit it to external URLs, webhooks, or remote endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/sonoscli-hardened) <br>
- [Sonos CLI homepage](https://sonoscli.sh) <br>
- [sonoscli Go install module](https://pkg.go.dev/github.com/steipete/sonoscli/cmd/sonos) <br>
- [Faberlens](https://faberlens.ai) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the sonos binary; Spotify search can use SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
