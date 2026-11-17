## Description:

Helps an agent guide users through installing and running spotify-download to save Spotify playlist tracks as local MP3 files with ffmpeg and optional Spotify API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgzesg](https://clawhub.ai/user/wgzesg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can ask an agent to prepare commands for downloading tracks from Spotify playlist URLs to a local MP3 library, including setup, output options, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to run mutable third-party package code.

Mitigation: Review the upstream spotify-download package before use and prefer a pinned, verified version or reviewed commit.

Risk: Spotify client secrets may be exposed if passed directly on the command line.

Mitigation: Use safer secret handling, such as environment variables or a secret manager, and avoid storing credentials in shell history.

Risk: Playlist metadata, track names, and downloaded audio are stored locally and sent to Spotify or YouTube-related services during operation.

Mitigation: Run the tool in a limited environment with only the intended output directory exposed and confirm the data flow is acceptable before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wgzesg/skills/spotify-download)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- [ffmpeg](https://ffmpeg.org)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, playlist URLs, installation commands, and credential-handling guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
