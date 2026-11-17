## Description:

Manage YouTube search by helping agents use the yutu CLI to search videos, channels, playlists, and other resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search YouTube resources through the yutu CLI after configuring YouTube API OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on installing and running a mutable third-party yutu CLI.

Mitigation: Review the yutu publisher and install source before use, and prefer a pinned and verified version.

Risk: The skill requires YouTube OAuth client secrets and cached tokens.

Mitigation: Grant only the minimum YouTube API scopes needed for search, store credential and token files outside repositories with restrictive permissions, and revoke or rotate tokens if exposed.

## Reference(s):

- [Search List](references/search-list.md)
- [Yutu Setup Guide](references/setup.md)
- [yutu Project Homepage](https://github.com/eat-pray-ai/yutu)
- [yutu Releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and CLI flag guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include yutu command examples, OAuth setup steps, and output format guidance for table, JSON, or YAML results.]

## Skill Version(s):

0.10.7-dev (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
