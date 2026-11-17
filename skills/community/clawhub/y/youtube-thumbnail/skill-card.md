## Description:

Helps agents manage YouTube video thumbnails by setting custom thumbnails through the yutu CLI and pointing first-time users to setup steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agents use this skill to install and configure yutu, authenticate with YouTube API credentials, and set a custom thumbnail file on a specified YouTube video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses a third-party yutu CLI for account-changing YouTube actions, and the security evidence notes the CLI is unpinned.

Mitigation: Review the yutu CLI source before installing, pin and verify the CLI version where possible, and confirm the target video ID and thumbnail file before running commands.

Risk: The skill uses persistent OAuth client secrets and cached YouTube tokens.

Mitigation: Keep client_secret.json and youtube.token.json out of repositories and logs, restrict file permissions, avoid raw secrets in environment variables where possible, and revoke OAuth tokens if exposure is suspected.

## Reference(s):

- [Yutu Setup Guide](references/setup.md)
- [Thumbnail Set Reference](references/thumbnail-set.md)
- [yutu project homepage](https://github.com/eat-pray-ai/yutu)
- [yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [Google Cloud Console](https://console.cloud.google.com/)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include yutu CLI commands that require local OAuth credentials, a thumbnail file path, and a target YouTube video ID.]

## Skill Version(s):

0.10.7-dev (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
