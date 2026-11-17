## Description:

Upload videos and custom thumbnails to YouTube. Use when the user wants to publish, upload, or post a video to YouTube, set a thumbnail, or manage YouTube channel authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nachx639](https://clawhub.ai/user/nachx639)

### License/Terms of Use:


## Use Case:

External users and creators use this skill to authenticate YouTube channels, upload videos with metadata, schedule private uploads, and set custom thumbnails through the YouTube Data API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores long-lived YouTube OAuth credentials for authenticated channels.

Mitigation: Use a dedicated YouTube account or channel where possible, review granted OAuth access, and revoke or delete stored credentials when the skill is no longer needed.

Risk: The helper script installs Google API Python packages at runtime without pinned versions.

Mitigation: Run the skill in a controlled environment and prefer a release that pins dependency versions before production use.

Risk: The requested YouTube scopes are broad enough to manage channel uploads and related account operations.

Mitigation: Grant access only for channels intended for automated uploads and confirm the video, metadata, privacy, and scheduled publish settings before making content public.

## Reference(s):

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [YouTube Video Category IDs](references/categories.md)
- [ClawHub Skill Page](https://clawhub.ai/nachx639/skills/youtube-uploader)
- [Publisher Profile](https://clawhub.ai/user/nachx639)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may authenticate channels, upload videos, upload thumbnails, list channels, or refresh OAuth tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
