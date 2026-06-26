## Description: <br>
Control Sonos speakers (discover/status/play/volume/group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wechatgpt798](https://clawhub.ai/user/wechatgpt798) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to install and operate the `sonos` CLI for discovering local Sonos speakers, checking status, controlling playback and volume, managing groups, favorites, and queues, and optionally searching Spotify tracks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and depends on an external Go-based Sonos CLI. <br>
Mitigation: Install only if the upstream module is trusted, and review the external module when stronger supply-chain assurance is required. <br>
Risk: Playback, volume, grouping, and queue commands can affect local Sonos speakers. <br>
Mitigation: Confirm speaker names or IP addresses before issuing playback, volume, grouping, or queue-clearing commands. <br>
Risk: Optional Spotify integration may involve client credentials. <br>
Mitigation: Keep Spotify client secrets in environment variables and out of prompts, transcripts, and logs. <br>


## Reference(s): <br>
- [Wayne Sonoscli Homepage](https://wayne-sonoscli.sh) <br>
- [Wayne Sonoscli Go Module](https://pkg.go.dev/github.com/steipete/wayne-sonoscli/cmd/sonos) <br>
- [ClawHub Release Page](https://clawhub.ai/wechatgpt798/wayne-sonoscli) <br>
- [Publisher Profile](https://clawhub.ai/user/wechatgpt798) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `sonos` binary; optional Spotify Web API search uses SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
