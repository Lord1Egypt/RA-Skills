## Description: <br>
Controls Spotify playback, search, playlist management, music discovery, and listening-history analysis through the Spotify Web API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdmichaelb](https://clawhub.ai/user/cdmichaelb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Spotify from an agent: control playback, search music, manage playlists, create discovery playlists, and inspect profile and listening data after OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad Spotify OAuth permissions, including playlist and library changes plus profile and follow-related access. <br>
Mitigation: Authorize it only when those permissions match the intended use, trim unused OAuth scopes before authorization when possible, and revoke the Spotify app if it is no longer needed. <br>
Risk: Reusable Spotify tokens and app credentials are stored locally in config.json. <br>
Mitigation: Keep config.json private, do not commit or share it, and protect the local file wherever the skill is installed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cdmichaelb/spotify-agent) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from Spotify scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Spotify OAuth authorization and may return Spotify API JSON responses or error objects.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
