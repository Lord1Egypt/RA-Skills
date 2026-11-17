## Description:

Manage YouTube video categories. Use this skill to list available video categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users working with YouTube metadata use this skill to list available YouTube video categories through the yutu CLI after configuring YouTube API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party yutu CLI.

Mitigation: Verify the yutu package source and version before installation.

Risk: The skill relies on persistent YouTube OAuth credential and token files.

Mitigation: Keep client_secret.json and youtube.token.json private, avoid exposing raw JSON or base64 secrets in shell exports or CI logs, and prefer restrictive file permissions.

Risk: Using the CLI grants access to a user's YouTube account.

Mitigation: Install and run the skill only if you are comfortable granting yutu access to the account.

## Reference(s):

- [Yutu GitHub repository](https://github.com/eat-pray-ai/yutu)
- [Yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [Yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [Yutu Setup Guide](references/setup.md)
- [Video Category List](references/videoCategory-list.md)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include yutu CLI flags and credential setup steps.]

## Skill Version(s):

0.10.7-dev (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
