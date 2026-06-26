## Description: <br>
Full YouTube Data API v3 CLI covering search, channels, videos, playlists, comments, subscriptions, captions, thumbnails, activities, channel sections, channel banners, members, memberships levels, watermarks, and related YouTube resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and automation agents use this skill to search YouTube data and manage channels, videos, playlists, comments, captions, thumbnails, subscriptions, and related account workflows through the YouTube Data API v3 CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth credentials can allow live YouTube account changes, including uploads, updates, deletes, comments, ratings, subscriptions, moderation, and channel branding changes. <br>
Mitigation: Prefer read-only API-key use for public searches, use the narrowest OAuth scopes that work, and require explicit confirmation before any write or moderation command. <br>
Risk: OAuth refresh tokens and API credentials are sensitive and can grant access to private account data or write operations. <br>
Mitigation: Protect credential files and environment variables, avoid logging secrets, and rotate or revoke tokens if they may have been exposed. <br>
Risk: A global npm installation could install an unexpected package version. <br>
Mitigation: Verify and pin the npm package version before global installation. <br>


## Reference(s): <br>
- [youtube-data-cli documentation](https://github.com/Bin-Huang/youtube-data-cli) <br>
- [YouTube Data API v3](https://developers.google.com/youtube/v3) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may perform live YouTube account reads or writes when OAuth credentials are supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
