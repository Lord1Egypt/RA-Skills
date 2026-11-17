## Description:

Downloads videos from Twitter/X posts to a specified local location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemonpek66](https://clawhub.ai/user/lemonpek66)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download videos or GIFs from Twitter/X posts to local storage, optionally choosing an output directory, filename, quality, and proxy configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Download security is weakened because TLS certificate checks are disabled by default.

Mitigation: Review before installing and prefer a version that removes the default TLS certificate bypass.

Risk: Proxy credentials may be exposed if embedded in PROXY_URL because the proxy value can appear in logs.

Mitigation: Avoid proxy URLs with embedded credentials and keep download logs private.

Risk: The skill writes downloaded files to the chosen output path.

Mitigation: Choose and review the output directory before execution.

Risk: The yt-dlp dependency is installed externally and is not pinned by the artifact.

Mitigation: Pin and review the yt-dlp version in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lemonpek66/skills/twitter-video-download)
- [Release notes](artifact/RELEASE_NOTES.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with command examples and downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are written to the selected output directory and use yt-dlp with optional proxy configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata and RELEASE_NOTES.md, released 2026-03-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
