## Description:

Manage YouTube channel watermarks by guiding set and unset operations through the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and channel operators use this skill to prepare YouTube API credentials and run yutu commands that set or remove a watermark on channel videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube OAuth credential and token files can expose account or channel access if stored insecurely.

Mitigation: Store client_secret.json and youtube.token.json outside shared or git-tracked folders and restrict file permissions.

Risk: The skill depends on the external yutu CLI.

Mitigation: Verify the yutu CLI source and version before installation and avoid running installs with elevated privileges.

Risk: Watermark set or unset commands can affect the wrong channel if the channel ID is incorrect.

Mitigation: Confirm the target channel ID before running yutu watermark set or unset commands.

## Reference(s):

- [Yutu Setup Guide](references/setup.md)
- [Watermark Set](references/watermark-set.md)
- [Watermark Unset](references/watermark-unset.md)
- [yutu project homepage](https://github.com/eat-pray-ai/yutu)
- [yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)
- [ClawHub skill page](https://clawhub.ai/openwaygate/skills/youtube-watermark)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yutu, Google Cloud OAuth client credentials, and a cached YouTube token.]

## Skill Version(s):

0.10.7-dev (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
