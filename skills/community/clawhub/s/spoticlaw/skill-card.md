## Description: <br>
Spotify Web API client for Nyx agents to search Spotify, control playback, manage playlists and library items, and retrieve tracks, artists, albums, shows, and podcasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ledzgio](https://clawhub.ai/user/ledzgio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use SpotiClaw to give an agent controlled access to Spotify account workflows, including search, playback control, playlist management, library updates, and listening-history queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth credentials and the .spotify_cache token can provide read and write access to the connected Spotify account. <br>
Mitigation: Protect .env and .spotify_cache like credentials, use a Spotify app you control, and revoke the app or delete the cache when access is no longer needed. <br>
Risk: Agent actions can change playback state, playlists, and saved library items. <br>
Mitigation: Require explicit approval before playlist, library, queue, volume, or playback changes. <br>
Risk: The requested OAuth scopes include private playlist, playback, library, history, top-item, and followed-artist access. <br>
Mitigation: Review the Spotify OAuth scopes before authorization and only install the skill when those account permissions are acceptable. <br>


## Reference(s): <br>
- [SpotiClaw on ClawHub](https://clawhub.ai/ledzgio/spoticlaw) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>
- [Spotify Authorization Code Flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow) <br>
- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; runtime calls return Spotify API response objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Spotify OAuth credentials and a local .spotify_cache token file.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
