## Description:

Control Spotify on Linux via MPRIS DBus for launching Spotify, controlling playback, searching songs, and switching playback to a specific track.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxp731](https://clawhub.ai/user/lxp731)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control the real Spotify desktop client in a local Linux desktop session through MPRIS DBus commands and the bundled launcher.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Playback commands affect the user's real Spotify client immediately.

Mitigation: Confirm the requested track, album, playlist, or control action before issuing commands that start playback or change state.

Risk: The user-level Spotify process may continue after the agent task finishes.

Mitigation: Use the documented --stop command when playback is no longer wanted.

Risk: --check output can include proxy URLs that may contain credentials.

Mitigation: Avoid sharing raw diagnostic logs, or redact proxy URLs before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxp731/skills/spotify-cachyos-linux)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may start or stop a user-level Spotify process and can change live playback immediately.]

## Skill Version(s):

1.0.5 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
