## Description:

Control Sonos speakers with CLI commands for discovery, status, playback, volume, grouping, favorites, queues, and optional Spotify search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadshouly](https://clawhub.ai/user/ahmadshouly)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for Sonos CLI guidance and commands that control Sonos speakers on a local network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install metadata downloads a third-party Sonos CLI at install time from a mutable Go dependency version.

Mitigation: Prefer a pinned sonoscli release where available, and review the dependency before installing in controlled environments.

Risk: Spotify-related commands may require Spotify client credentials.

Mitigation: Provide Spotify credentials only for Spotify workflows and manage them through the local secret handling expected by the agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahmadshouly/skills/sonoscli-bak)
- [Publisher profile](https://clawhub.ai/user/ahmadshouly)
- [Sonos CLI homepage](https://sonoscli.sh)
- [sonoscli Go install module](https://pkg.go.dev/github.com/steipete/sonoscli/cmd/sonos)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the sonos binary; Spotify-related commands may require Spotify client credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
