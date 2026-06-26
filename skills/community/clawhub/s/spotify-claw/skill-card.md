## Description: <br>
Spotify enables an agent to control Spotify Premium playback, analyze listening history and taste, discover similar music, and create or update playlists through Spotify commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mixx85](https://clawhub.ai/user/mixx85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents with Spotify Premium use this skill to run Spotify playback commands, inspect top tracks and artists, search liked songs, discover related music, and build playlists from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spotify account authorization can permit playback control, library analysis, and playlist changes. <br>
Mitigation: Review Spotify OAuth scopes before authorizing and use explicit Spotify phrasing for account-changing commands. <br>
Risk: Playback or playlist commands can have visible side effects in the user's Spotify account. <br>
Mitigation: Confirm the intended device, playlist, and action before running commands that play, queue, create, or update content. <br>
Risk: Spotify client credentials are required for setup. <br>
Mitigation: Store credentials in macOS Keychain as documented and avoid placing secrets in prompts, logs, or plain-text files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mixx85/spotify-claw) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown instructions with bash command examples and short text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may control playback, read library data, and create or modify playlists through authorized Spotify account access.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
