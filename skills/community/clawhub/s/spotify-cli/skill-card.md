## Description:

Control Spotify playback on a Linux device from the command line, including search, play, pause, resume, track navigation, status, and device listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnpana](https://clawhub.ai/user/shawnpana)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to set up and operate a Spotify command-line controller on Linux systems, especially Raspberry Pi devices, after configuring Spotify API credentials and an active Spotify session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes system-level changes such as using sudo to copy a command into /usr/local/bin.

Mitigation: Review the script before installing it, prefer a user-local or virtual-environment installation, and avoid sudo unless the exact installed file and permissions are understood.

Risk: The setup stores Spotify client credentials in a local configuration file.

Mitigation: Protect the configuration file with restrictive permissions and avoid sharing logs, screenshots, or files that expose the client secret.

Risk: Troubleshooting guidance suggests deleting broad cache file patterns.

Mitigation: Remove only the specific Spotify authentication cache after confirming the path, rather than deleting all matching cache files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawnpana/skills/spotify-cli)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- [Spotify Web Player](https://open.spotify.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Spotify Premium, Spotipy, Spotify API credentials, and an active Spotify session on another device.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
