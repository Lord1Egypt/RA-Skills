## Description:

Download music from YouTube/YouTube Music and stream to Chromecast via Home Assistant. Complete CLI toolset with web server integration, configuration wizard, and playback controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidanthebandit](https://clawhub.ai/user/aidanthebandit)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to download YouTube or YouTube Music audio, host it locally, and cast playback to Chromecast devices through Home Assistant. It supports setup, server control, playback management, radio mode, and optional MP4 video output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a long-lived Home Assistant access token stored in local configuration.

Mitigation: Use HTTPS for Home Assistant, create a dedicated least-privileged account or token where possible, and restrict permissions on ~/.youtube-music-cast/config.sh.

Risk: The skill may run a background local web server to expose downloaded media on the local network.

Mitigation: Run it only on trusted networks, stop it when it is not needed, and verify that the configured server IP and port are not exposed beyond the intended local network.

Risk: The skill may install command-line tools globally and creates persistent local setup state.

Mitigation: Review install steps before execution, prefer local installation when appropriate, and install only on machines where persistent media-casting configuration is acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup steps, command usage, local configuration guidance, and playback troubleshooting.]

## Skill Version(s):

6.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
