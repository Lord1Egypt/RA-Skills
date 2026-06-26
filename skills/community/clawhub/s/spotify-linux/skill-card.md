## Description: <br>
Spotify CLI for headless Linux servers, enabling terminal playback control with cookie authentication when OAuth localhost callbacks are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shaharsha](https://clawhub.ai/user/Shaharsha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and control Spotify playback from headless Linux servers. It provides installation, cookie-auth setup, device selection, playback commands, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spotify session cookies can grant account access if exposed. <br>
Mitigation: Keep sp_dc and sp_t private, use restrictive permissions on ~/.config/spogo and cookie files, avoid logging cookie values, and remove the cookies when the skill is no longer needed. <br>
Risk: Installing spogo with an unpinned latest version can change behavior over time. <br>
Mitigation: Review or pin the upstream spogo version before installing in controlled environments. <br>
Risk: Browser fallback can start Spotify playback through an agent-controlled browser session. <br>
Mitigation: Use the fallback only when no active Spotify device exists and keep it limited to opening Spotify and clicking Play in the isolated browser profile. <br>


## Reference(s): <br>
- [Spotify Player on ClawHub](https://clawhub.ai/Shaharsha/spotify-linux) <br>
- [spogo GitHub repository](https://github.com/steipete/spogo) <br>
- [Go downloads](https://go.dev/dl/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash, TOML, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include local cookie-file setup and optional browser fallback steps.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
