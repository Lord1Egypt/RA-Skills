## Description:

Spotify Openclaw lets an OpenClaw agent control Spotify Premium playback on macOS, inspect listening and library data, discover related music, and create or update playlists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mixx85](https://clawhub.ai/user/mixx85)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users on macOS use this skill to operate Spotify Premium from chat, review listening history and library information, find related music, and build playlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Spotify listening data, private playlists, library state, and playback controls through broad OAuth scopes.

Mitigation: Review requested scopes before use, remove unused scopes where possible, and delete the old OAuth cache after any scope reduction.

Risk: The skill can create playlists, add tracks, queue playback, change volume, skip tracks, shuffle, pause, and start playback.

Mitigation: Require explicit confirmation before playlist changes or playback changes that affect the user's Spotify account or active device.

Risk: The skill instructs the agent to run local Spotify commands rather than only answering in text.

Mitigation: Prefer explicit Spotify-prefixed requests and review command intent before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mixx85/skills/spotify-openclaw)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style command guidance and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output may include Spotify track, artist, playlist, device, playback, and library details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
