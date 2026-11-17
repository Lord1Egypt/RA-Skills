## Description:

Control Spotify playback and devices from an AI agent using spotify.py and the official Spotify Web API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[egemenyerdelen](https://clawhub.ai/user/egemenyerdelen)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to check Spotify playback state, control playback, manage Spotify Connect devices, search tracks, and play tracks by search result or Spotify URI from local, Docker, VPS, or headless environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spotify client secrets and refresh tokens can grant account playback access if exposed.

Mitigation: Store credentials outside source control, restrict access to the .env file, use least-access Spotify scopes, and revoke or rotate the refresh token if exposure is suspected.

Risk: Loose dependency installation and writable script permissions can increase deployment risk.

Mitigation: Use an isolated virtual environment or locked container dependency set, pin requests, avoid system-wide package installs where possible, and keep the script read-only for non-deployment users.

## Reference(s):

- [Spotify Developer Documentation](https://developer.spotify.com)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- [ClawHub Skill Page](https://clawhub.ai/egemenyerdelen/skills/spotify-controller)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, requests, Spotify Premium, Spotify Developer credentials, and SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_REFRESH_TOKEN environment variables.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
