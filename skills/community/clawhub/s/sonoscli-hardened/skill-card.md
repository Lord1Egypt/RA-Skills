## Description:

Control Sonos speakers (discover/status/play/volume/group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Sonos speakers on a local network through the sonos CLI, including discovery, playback controls, volume, grouping, favorites, queue, and Spotify search. The skill adds guardrails for destructive actions, credential secrecy, and local handling of speaker and network data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a mutable third-party Go CLI using an @latest module reference.

Mitigation: Prefer a pinned, reviewed sonoscli version before installation or deployment.

Risk: The CLI can affect live Sonos speakers through queue, grouping, playback, and volume commands.

Mitigation: Require explicit user confirmation before destructive queue actions, grouping changes, or high-volume changes.

Risk: Spotify integration may rely on SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET values.

Mitigation: Keep credential values private and do not print, echo, hash, or expose credential fragments during troubleshooting.

Risk: Sonos status and discovery output can reveal speaker names, IP addresses, playback state, queue contents, and local network topology.

Mitigation: Keep command output local unless the user manually reviews and redacts what is safe to share.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/sonoscli-hardened)
- [Sonos CLI homepage](https://sonoscli.sh)
- [Faberlens sonoscli safety evaluation](https://faberlens.ai/explore/sonoscli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend local sonos CLI commands; destructive queue, grouping, or high-volume changes require explicit confirmation, Spotify credentials must not be displayed, and Sonos output should remain local.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
