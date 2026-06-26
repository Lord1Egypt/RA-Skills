## Description: <br>
Control Spotify playback on a Linux device through command-line search, play, pause, resume, skip, status, and device-listing commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShawnPana](https://clawhub.ai/user/ShawnPana) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to control Spotify playback from a Linux device, typically after confirming a search result with the user before starting playback. It is useful for remote or embedded Linux environments where Spotify is already active on another device. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation instructions copy an unprovided executable into /usr/local/bin with sudo. <br>
Mitigation: Inspect and trust the actual spotify script before installation, and prefer a user-local bin directory where possible. <br>
Risk: The dependency installation example uses --break-system-packages. <br>
Mitigation: Install dependencies in a virtual environment or with pipx instead of modifying the system Python environment. <br>
Risk: Spotify client credentials are stored in a local config file. <br>
Mitigation: Restrict the config file permissions, such as with chmod 600, and avoid sharing the file contents. <br>
Risk: Spotify search may select the wrong track when a query is ambiguous. <br>
Mitigation: Search first, review the top results with the user, and play the confirmed title and artist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ShawnPana/spotify-cli) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>
- [Spotify Web Player](https://open.spotify.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Spotify Premium, Spotipy credentials, and an active Spotify session on another device.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
