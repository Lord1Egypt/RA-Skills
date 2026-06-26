## Description: <br>
Control Spotify playback on macOS. Play/pause, skip tracks, control volume, play artists/albums/playlists. Use when a user asks to play music, control Spotify, change songs, or adjust Spotify volume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2mawi2](https://clawhub.ai/user/2mawi2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent control the local Spotify desktop app on macOS for playback, track navigation, volume, status, and playback by Spotify URI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad request such as "play music" may activate Spotify control when the user intended another app. <br>
Mitigation: Ask the user to confirm Spotify as the target app for generic music-control requests. <br>
Risk: The skill relies on the Homebrew shpotify package, the spotify CLI, AppleScript, and the local Spotify desktop app on macOS. <br>
Mitigation: Confirm the command-line dependency and Spotify desktop app are installed and available before issuing playback commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/2mawi2/spotify) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only guidance that assumes the Spotify desktop app and spotify CLI are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
