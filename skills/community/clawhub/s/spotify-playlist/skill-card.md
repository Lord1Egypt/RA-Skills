## Description: <br>
Build and manage Spotify playlists from natural language requests using the Spotify Web API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeaholicman](https://clawhub.ai/user/codeaholicman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to authenticate with Spotify, search music, create and update playlists, and personalize selections with listening history when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Spotify credentials can read listening history and profile data. <br>
Mitigation: Use only the needed Spotify scopes, avoid the profile command unless necessary, and delete or revoke the saved token when the skill is no longer in use. <br>
Risk: The skill can modify Spotify playlists after authorization. <br>
Mitigation: Prefer private playlists and review create, add, and remove operations before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeaholicman/spotify-playlist) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>
- [Spotify Web API base URL](https://api.spotify.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; helper scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Spotify OAuth credentials and a Spotify Premium account; helper scripts can create, update, and inspect Spotify playlists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
