## Description:

Control Sonos speakers for discovery, status, playback, volume, grouping, favorites, queue operations, and optional Spotify search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maddydci45-svg](https://clawhub.ai/user/maddydci45-svg)

### License/Terms of Use:


## Use Case:

Developers and users with Sonos speakers use this skill to have an agent suggest or run Sonos CLI commands for local speaker discovery, playback control, volume control, grouping, favorites, queue management, and optional Spotify search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on an upstream third-party Go CLI package at the latest version, creating supply-chain and version drift risk.

Mitigation: Install only after reviewing the upstream package, prefer a version pinned to a reviewed commit, and rerun security review when the dependency changes.

Risk: Optional Spotify Web API search may require credential environment variables.

Mitigation: Expose only the required Spotify credentials for the command being run and avoid sharing unrelated environment variables with the CLI process.

Risk: Sonos control commands affect speakers on the local network and may target the wrong device if names or IP addresses are ambiguous.

Mitigation: Confirm the speaker name or IP address with discovery/status commands before issuing playback, grouping, queue, or volume changes.

## Reference(s):

- [Sonos CLI homepage](https://sonoscli.sh)
- [ClawHub skill page](https://clawhub.ai/maddydci45-svg/skills/sonos)
- [Go install module: github.com/steipete/sonoscli/cmd/sonos](https://pkg.go.dev/github.com/steipete/sonoscli/cmd/sonos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local-network speaker names or IP addresses and optional Spotify credential environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact origin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
