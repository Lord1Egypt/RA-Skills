## Description:

Manage YouTube i18n regions by listing available internationalization regions through the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure yutu and list YouTube internationalization regions when working with YouTube Data API region metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party yutu CLI before use.

Mitigation: Review the skill before installing and prefer a pinned or otherwise verified yutu release.

Risk: The skill requires reusable Google OAuth credentials and cached YouTube tokens.

Mitigation: Use a dedicated Google project or account where possible, confirm OAuth scopes, keep client_secret.json and youtube.token.json out of repositories and shared folders, and restrict file permissions.

## Reference(s):

- [Yutu Setup Guide](references/setup.md)
- [I18n Region List](references/i18nRegion-list.md)
- [yutu Homepage](https://github.com/eat-pray-ai/yutu)
- [yutu Releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide setup of yutu, Google OAuth credentials, and output flags for table, JSON, or YAML results.]

## Skill Version(s):

0.10.7-dev (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
