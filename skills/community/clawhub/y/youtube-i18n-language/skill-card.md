## Description:

Manage YouTube i18n languages by helping agents list available internationalization languages with the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare YouTube API credentials and ask an agent for commands to list YouTube internationalization languages through yutu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a mutable third-party yutu CLI package could expose users to unreviewed package changes.

Mitigation: Review the package and publisher before installing, prefer a pinned version or verified release, and scan updates before deployment.

Risk: OAuth client secrets and cached YouTube tokens can grant account access if exposed.

Mitigation: Keep client_secret.json and youtube.token.json out of source control and shared folders, use narrow OAuth scopes, and revoke or rotate tokens if exposed.

Risk: Enabling optional YouTube APIs can broaden account and project access beyond the language-listing task.

Mitigation: Enable only the YouTube APIs needed for the intended workflow and remove optional APIs when they are not required.

## Reference(s):

- [I18n Language List](references/i18nLanguage-list.md)
- [Yutu Setup Guide](references/setup.md)
- [yutu project](https://github.com/eat-pray-ai/yutu)
- [yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference yutu command flags and required local credential or token files.]

## Skill Version(s):

0.10.7-dev (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
