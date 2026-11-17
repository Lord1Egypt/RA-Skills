## Description:

Manage your YouTube account from the command line. Complete CLI for YouTube Data API v3 - list/search videos, upload, manage playlists, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerveband](https://clawhub.ai/user/nerveband)

### License/Terms of Use:


## Use Case:

Developers, creators, and automation agents use this skill to install and operate a YouTube Data API v3 CLI for listing, searching, uploading, and managing YouTube videos, playlists, channels, and subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions use an unpinned external executable path and optional system-wide sudo installation.

Mitigation: Review the upstream CLI before installing, prefer a pinned version with verified checksums or signatures, and use a user-local install path when possible.

Risk: Upload, playlist, and channel update commands can modify YouTube account content.

Mitigation: Use least-privilege Google credentials, test with noncritical or private/unlisted targets first, and confirm intended changes before running modifying commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerveband/skills/yt-api-cli)
- [Google Cloud Console](https://console.cloud.google.com)
- [YouTube API CLI source link from skill content](https://github.com/nerveband/youtube-api-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, command references, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI defaults to JSON output and supports table, YAML, and CSV output formats.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
