## Description:

Manage YouTube channel members by guiding agents to list member information with the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list YouTube channel members through yutu after configuring Google Cloud OAuth credentials and a cached YouTube API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party yutu CLI package and installation path.

Mitigation: Verify the yutu package publisher before installing and avoid running installation with unnecessary administrator privileges.

Risk: The skill uses Google OAuth client secrets and cached YouTube API tokens.

Mitigation: Keep client_secret.json and youtube.token.json out of source control and shared folders, and revoke or rotate tokens if either file is exposed.

## Reference(s):

- [Yutu Setup Guide](references/setup.md)
- [Member List](references/member-list.md)
- [Yutu Homepage](https://github.com/eat-pray-ai/yutu)
- [Yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [Yutu Releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)
- [ClawHub Skill Page](https://clawhub.ai/openwaygate/skills/youtube-member)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yutu, Google Cloud OAuth credentials, and a cached YouTube API token.]

## Skill Version(s):

0.10.7-dev (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
