## Description:

Helps agents list YouTube channel activity through the yutu CLI and includes first-time setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent prepare yutu CLI commands for listing YouTube activities such as uploads, likes, and favorites after OAuth credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party CLI that handles YouTube OAuth credentials and cached tokens.

Mitigation: Review the yutu package or source before installing, prefer a pinned and verified release, and avoid elevated or global installation when practical.

Risk: The setup flow uses client_secret.json and youtube.token.json, which can expose Google OAuth credentials or cached access tokens if mishandled.

Mitigation: Store credential and token files outside repositories with restrictive permissions, and revoke or rotate the Google OAuth token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openwaygate/skills/youtube-activity)
- [Yutu Homepage](https://github.com/eat-pray-ai/yutu)
- [Yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [Yutu Releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [Yutu Setup Guide](references/setup.md)
- [Activity List](references/activity-list.md)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include yutu command flags, OAuth credential setup steps, and references to local credential or token file paths.]

## Skill Version(s):

0.10.7-dev (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
