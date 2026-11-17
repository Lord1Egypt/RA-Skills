## Description:

Safer Spotify playback for OpenClaw on setups where direct spogo play is unreliable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surdragon-design](https://clawhub.ai/user/surdragon-design)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control Spotify playback through spogo when direct playback commands are unreliable. It helps search Spotify content, select devices, and start tracks, albums, or playlists with safer command sequencing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented spotify-safe-play wrapper script is missing from the artifact.

Mitigation: Verify or install the wrapper before relying on the safe playback command.

Risk: Playback commands operate through the user's authenticated Spotify account and active playback device.

Mitigation: Use the skill only on trusted machines with a known Spotify Connect target and a trusted spogo installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/surdragon-design/skills/spotify-safe-play)
- [Skill homepage](https://github.com/surdragon-design/spotify-safe-player)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate through spogo and the user's authenticated Spotify account.]

## Skill Version(s):

v0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
