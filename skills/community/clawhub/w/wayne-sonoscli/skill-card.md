## Description:

Control Sonos speakers (discover/status/play/volume/group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wechatgpt798](https://clawhub.ai/user/wechatgpt798)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Sonos speakers through an agent-guided CLI workflow, including discovery, playback control, volume, grouping, favorites, queue management, and optional Spotify search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party Go CLI at install time.

Mitigation: Install only after reviewing or pinning the module version and trusting the upstream package.

Risk: The CLI can discover and control Sonos devices on the local network.

Mitigation: Use it only on trusted networks and target intended speakers by name or IP address.

Risk: Optional Spotify search uses Spotify Web API credentials.

Mitigation: Provide Spotify credentials only when using Spotify search and manage them through environment variables.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wechatgpt798/skills/wayne-sonoscli)
- [Publisher Profile](https://clawhub.ai/user/wechatgpt798)
- [Wayne Sonoscli Homepage](https://wayne-sonoscli.sh)
- [Go Install Module](https://pkg.go.dev/github.com/steipete/wayne-sonoscli/cmd/sonos)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local-network Sonos speaker names, speaker IP addresses, and optional Spotify environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
