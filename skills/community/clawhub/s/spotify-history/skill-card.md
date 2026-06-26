## Description: <br>
Access Spotify listening history, top artists/tracks, and get personalized recommendations via the Spotify Web API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[braydoncoyer](https://clawhub.ai/user/braydoncoyer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve Spotify listening history, top artists and tracks, current playback state, and personalized music recommendations after one-time OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private Spotify listening and preference data through OAuth scopes. <br>
Mitigation: Review the requested Spotify scopes before authorizing and revoke the Spotify app authorization when the skill is no longer needed. <br>
Risk: Spotify client secrets and OAuth tokens are stored locally. <br>
Mitigation: Keep credential and token files private, preserve user-only file permissions, and avoid sharing workspaces that contain those files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/braydoncoyer/spotify-history) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>
- [Spotify Accounts authorization endpoint](https://accounts.spotify.com/authorize) <br>
- [Spotify Accounts token endpoint](https://accounts.spotify.com/api/token) <br>
- [Spotify Web API base endpoint](https://api.spotify.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Spotify API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local Spotify OAuth tokens and user listening data after authorization.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
