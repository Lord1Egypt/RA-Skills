## Description:

Full YouTube Data API v3 CLI covering all 20 resources, including search, channels, videos, playlists, comments, subscriptions, captions, thumbnails, activities, channel sections, banners, members, membership levels, watermarks, and related management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and creator-support agents use this skill to search YouTube and manage YouTube channels, videos, playlists, comments, subscriptions, captions, thumbnails, banners, and channel settings through the YouTube Data API v3 CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install and use an unpinned CLI that handles YouTube API credentials.

Mitigation: Use a pinned, inspected, local or isolated install before connecting a real YouTube account.

Risk: OAuth credentials and refresh tokens can grant access to private YouTube data and account-changing operations.

Mitigation: Grant the narrowest OAuth scope needed and protect API keys, client secrets, and refresh tokens in secure storage.

Risk: The documented commands can upload, update, delete, moderate, subscribe, and change channel configuration.

Mitigation: Require explicit confirmation before executing uploads, deletes, moderation changes, subscription changes, or channel configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bin-huang/skills/youtube-data-cli)
- [youtube-data-cli documentation](https://github.com/Bin-Huang/youtube-data-cli)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [YouTube OAuth full-access scope](https://www.googleapis.com/auth/youtube)
- [YouTube upload OAuth scope](https://www.googleapis.com/auth/youtube.upload)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read public data or change YouTube account resources depending on credentials and OAuth scope.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
