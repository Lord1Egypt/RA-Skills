## Description: <br>
Searches Spotify by song, artist, or keyword and plays the selected track in the local macOS Spotify app using AppleScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uxbryan](https://clawhub.ai/user/uxbryan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and users on macOS use this skill to turn a natural-language song request into Spotify playback through the installed Spotify app, then receive the requested track name, URI, and current playback status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch and control the local Spotify app and start audio playback on the user's Mac. <br>
Mitigation: Install and use it only on a Mac where agent-controlled Spotify playback is acceptable. <br>
Risk: Spotify API client credentials may be read from environment variables or ~/.shpotify.cfg. <br>
Mitigation: Use dedicated Spotify API credentials where possible and keep ~/.shpotify.cfg readable only by the local user. <br>


## Reference(s): <br>
- [Spotplay on ClawHub](https://clawhub.ai/uxbryan/spotplay) <br>
- [Spotify Web API Search endpoint](https://developer.spotify.com/documentation/web-api/reference/search) <br>
- [Spotify Web API Client Credentials flow](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls] <br>
**Output Format:** [Plain text status output with requested track, Spotify URI, and now-playing information] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Spotify.app, network access to Spotify APIs, and Spotify client credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
