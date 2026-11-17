## Description:

Automates YouTube video uploads and channel management with YouTube Data API v3 and OAuth 2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pdpaer](https://clawhub.ai/user/pdpaer)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to configure OAuth credentials, upload videos, set titles, descriptions, tags, thumbnails, categories, privacy status, and add uploads to playlists from an agent-assisted command workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad YouTube OAuth authority and can upload or manage channel content through the authorized account.

Mitigation: Review the Google OAuth consent scopes before authorizing and use an account or channel appropriate for automated uploads.

Risk: Refreshable OAuth tokens and client secrets are stored locally by the workflow.

Mitigation: Keep client_secret.json and token.json private with restrictive filesystem permissions, and revoke the OAuth grant if token exposure is suspected or the skill is no longer needed.

Risk: An incorrect channel, account, or privacy setting can publish content unintentionally.

Mitigation: Confirm the active YouTube channel, upload metadata, and privacy setting before each upload; use private or unlisted status for review when appropriate.

## Reference(s):

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com)
- [OAuth 2.0 for Installed Applications](https://developers.google.com/youtube/v3/guides/auth/installed-apps)
- [Videos: insert](https://developers.google.com/youtube/v3/docs/videos/insert)
- [YouTube API Quota Costs](https://developers.google.com/youtube/v3/determine_quota_cost)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate authenticated YouTube API operations when the user runs the generated commands with local OAuth credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
