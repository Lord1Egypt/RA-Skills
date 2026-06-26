## Description: <br>
Terminal Spotify playback and search via spogo, with spotify_player as a fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nabssku](https://clawhub.ai/user/nabssku) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and terminal users can use this skill to control Spotify playback, search tracks, manage devices, and configure terminal Spotify clients from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default spogo setup imports Chrome browser cookies for authentication, which can expose session credentials if the tool or local environment is not trusted. <br>
Mitigation: Install only trusted Spotify CLI tools, review how imported credentials are stored and revoked, and prefer a supported OAuth or device-login flow when available. <br>


## Reference(s): <br>
- [Spotify](https://www.spotify.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires either spogo or spotify_player and a Spotify Premium account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
