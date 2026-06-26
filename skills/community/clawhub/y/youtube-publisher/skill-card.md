## Description: <br>
Automates YouTube video uploads with title, description, tags, thumbnail, privacy, channel, and playlist management through the YouTube Data API v3 and OAuth 2.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pdpaer](https://clawhub.ai/user/pdpaer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and developers use this skill to let an agent upload local videos to YouTube, set publication metadata, manage thumbnails and playlists, and inspect channel upload state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain reusable OAuth access to a YouTube channel. <br>
Mitigation: Grant access only to the intended Google account, store credentials locally, and revoke or delete the token when the skill is no longer needed. <br>
Risk: An agent could publish or modify YouTube content without a separate required confirmation step. <br>
Mitigation: Confirm the video path, channel, title, description, tags, thumbnail, playlist, and privacy setting before every upload or modification. <br>
Risk: Uploads may become public if privacy options are changed from the default private setting. <br>
Mitigation: Use private uploads for review first, then manually switch to unlisted or public only after checking the uploaded video. <br>


## Reference(s): <br>
- [YouTube Data API v3](https://developers.google.com/youtube/v3) <br>
- [OAuth 2.0 for installed applications](https://developers.google.com/youtube/v3/guides/auth/installed-apps) <br>
- [Videos: insert](https://developers.google.com/youtube/v3/docs/videos/insert) <br>
- [YouTube API quota costs](https://developers.google.com/youtube/v3/determine_quota_cost) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [ClawHub skill page](https://clawhub.ai/pdpaer/youtube-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text] <br>
**Output Format:** [Markdown guidance with shell commands and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create OAuth token files and upload, list, or modify YouTube channel content through Google APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
