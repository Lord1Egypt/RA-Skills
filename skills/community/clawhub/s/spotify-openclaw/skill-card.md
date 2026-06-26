## Description: <br>
Spotify Openclaw lets an OpenClaw agent control Spotify Premium playback, inspect listening history, analyze top tracks, artists, and genres, discover related music, and create playlists on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mixx85](https://clawhub.ai/user/mixx85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to run local Spotify Premium playback, library analysis, music discovery, and playlist-management commands from chat. It is intended for macOS environments with Spotify developer credentials and the Spotipy Python package installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad Spotify account access, including access to listening history and playback or playlist controls. <br>
Mitigation: Review the Spotify OAuth consent screen before authorizing, install only when that access is acceptable, and remove unused scopes such as user-read-email or user-library-modify when they are not needed. <br>
Risk: Commands can make persistent Spotify account changes, including queue, playback, and playlist updates. <br>
Mitigation: Confirm playlist and library modification commands before execution and review command arguments for the target playlist, track, or artist. <br>
Risk: The cached Spotify token can allow continued account access if exposed. <br>
Mitigation: Keep the token cache private, avoid sharing the local OpenClaw configuration directory, and revoke the Spotify app authorization if the token may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mixx85/spotify-openclaw) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python commands that may read Spotify account data and modify playback, queue, and playlists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
