## Description:

Uploads single MP4 files or batches from a final/ directory to YouTube, using metadata from UPLOAD_META.md or command-line flags and resumable uploads that can run through a proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianshuo](https://clawhub.ai/user/jianshuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to publish finished MP4 videos or batch-upload a final/ directory to YouTube with titles, descriptions, tags, privacy settings, playlists, and optional scheduled publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses long-lived YouTube OAuth credentials and tokens that can upload videos to the user's account.

Mitigation: Store credentials.json and token.json with restrictive permissions, limit who can access the machine, and delete or re-authorize the token when upload access should be revoked.

Risk: Proxy URLs may contain embedded credentials and the uploader can print the selected proxy value.

Mitigation: Prefer proxy URLs without embedded passwords, keep upload logs private, and redact proxy values before sharing logs.

Risk: Incorrect privacy, playlist, or scheduling flags can publish or organize videos differently than intended.

Mitigation: Run --dry-run before batch uploads and verify --privacy, --playlist, and --publish-at before live upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jianshuo/skills/wjs-uploading-video)
- [Google Cloud OAuth setup for YouTube upload](artifact/references/credentials-setup.md)
- [Google Cloud Console](https://console.cloud.google.com)
- [YouTube upload endpoint](https://www.googleapis.com/upload/youtube/v3/videos)
- [YouTube upload OAuth scope](https://www.googleapis.com/auth/youtube.upload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON upload-result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the YouTube Data API, cache OAuth tokens locally, use proxy environment variables, and write per-video upload results.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
