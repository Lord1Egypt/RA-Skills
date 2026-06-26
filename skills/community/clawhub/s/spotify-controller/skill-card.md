## Description: <br>
Control Spotify playback and devices from an AI agent using spotify.py and the official Spotify Web API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[egemenyerdelen](https://clawhub.ai/user/egemenyerdelen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and control Spotify playback, search tracks, manage Spotify Connect devices, and play Spotify track URIs in local, container, VPS, or headless environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control playback on the user's Spotify account through Spotify OAuth credentials. <br>
Mitigation: Install only when that control is intended, review requested Spotify scopes, and revoke or rotate credentials if access is no longer needed or secrets are exposed. <br>
Risk: Spotify client secrets and refresh tokens are sensitive credentials. <br>
Mitigation: Keep credentials out of committed files, pass them through the runtime environment, and rotate app credentials if leaked. <br>
Risk: Spotify API and device restrictions can cause playback, device handoff, or volume commands to fail. <br>
Mitigation: Treat non-zero exits as failures, keep at least one Spotify device session active, and retry only appropriate transient network errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/egemenyerdelen/spotify-controller) <br>
- [Spotify Developer Documentation](https://developer.spotify.com) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and Markdown instructions with shell, Dockerfile, YAML, and environment variable snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, requests, Spotify Premium, Spotify OAuth credentials, and an active Spotify device session for playback controls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
