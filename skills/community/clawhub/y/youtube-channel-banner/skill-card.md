## Description:

Helps agents prepare and run yutu CLI commands to upload a banner image to a YouTube channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, channel managers, and developers use this skill to configure yutu credentials and generate commands for uploading a banner image to a specified YouTube channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party yutu CLI.

Mitigation: Install yutu only from a trusted source and prefer a pinned, reviewed version when available.

Risk: OAuth credential and token files can grant access to a YouTube account.

Mitigation: Keep client_secret.json and youtube.token.json out of source control and shared folders.

Risk: Running the insert command modifies the selected YouTube channel banner.

Mitigation: Review the OAuth consent screen, grant only the access needed, and verify the target channel ID and banner file before execution.

## Reference(s):

- [Channel Banner Insert](references/channelBanner-insert.md)
- [Yutu Setup Guide](references/setup.md)
- [Yutu project homepage](https://github.com/eat-pray-ai/yutu)
- [Yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and CLI flag tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yutu, Google Cloud OAuth credentials, and a cached YouTube token before banner upload commands can run.]

## Skill Version(s):

0.10.7-dev (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
