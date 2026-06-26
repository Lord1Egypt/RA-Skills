## Description: <br>
Terminal Spotify playback/search via spogo (preferred) or spotify_player. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and terminal users use this skill to control Spotify playback, search for tracks, manage devices, and configure terminal-based Spotify clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can import Spotify authentication from a Chrome browser profile, which may expose account tokens or cookies if the CLI or local storage is not trusted. <br>
Mitigation: Install only trusted Spotify CLI tools, prefer official OAuth or device-code login when available, verify token storage behavior, and know how to revoke Spotify access. <br>
Risk: Playback and device commands act on the user's Spotify account and active Spotify Connect devices. <br>
Mitigation: Review commands before execution and confirm the target device before changing playback state. <br>


## Reference(s): <br>
- [Spotify](https://www.spotify.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/steipete/spotify-player) <br>
- [Publisher Profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires either spogo or spotify_player and a Spotify Premium account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
