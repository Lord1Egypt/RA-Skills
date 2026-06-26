## Description: <br>
Search and manage Spotify playlists, tracks, albums, artists, and playback state via the Spotify Web API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Spotify content, inspect playlists and library state, and make confirmed changes such as playlist edits, saved-library updates, follows, uploads, or playback controls through a connected Spotify account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting a Spotify account through ClawLink and grants access according to the OAuth scopes approved during setup. <br>
Mitigation: Review the Spotify OAuth scopes during connection and install only if the account connection through ClawLink is acceptable. <br>
Risk: Playlist, library, follow, upload, and playback tools can change the connected Spotify account state. <br>
Mitigation: Preview and confirm write operations only when they match the user's explicit request. <br>
Risk: Playback controls may fail when the account lacks Spotify Premium or no active Spotify device is available. <br>
Mitigation: Confirm Premium status and an active Spotify session before attempting playback control. <br>


## Reference(s): <br>
- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api) <br>
- [Spotify Developer Console](https://developer.spotify.com/console/) <br>
- [Spotify OAuth Guide](https://developer.spotify.com/documentation/general/guides/authorization/) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/spotify-audio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live Spotify tool catalog and ClawLink connection state; write operations should be previewed and confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
