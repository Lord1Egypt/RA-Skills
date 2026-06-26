## Description: <br>
Terminal Spotify playback/search via spogo (preferred) or spotify_player. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to control Spotify playback, search tracks, select devices, and manage basic player actions from a terminal through spogo or spotify_player. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication import, local config access, or terminal output can expose Spotify tokens, cookies, client IDs, device IDs, or playback data. <br>
Mitigation: Require explicit user approval before authentication or config-file access, never display credentials, and avoid piping Spotify CLI output to network-transmitting commands. <br>
Risk: Spotify account state can be changed by destructive actions such as deleting playlists, removing saved tracks, or unfollowing artists. <br>
Mitigation: Confirm destructive Spotify actions with the user before execution and summarize the account change being approved. <br>
Risk: The preferred spogo install path uses a third-party Homebrew tap. <br>
Mitigation: Verify the third-party Homebrew tap before installing spogo and use spotify_player as a fallback when appropriate. <br>
Risk: Repeated automated playback or polling commands can exceed the user's intended level of Spotify automation. <br>
Mitigation: Avoid loops, background polling, and rapid repeated spogo or spotify_player commands unless the user explicitly requests bounded automation. <br>


## Reference(s): <br>
- [Spotify](https://www.spotify.com) <br>
- [Faberlens Safety Evaluation](https://faberlens.ai) <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/spotify-player-hardened) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Spotify Premium account and either spogo or spotify_player installed locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
