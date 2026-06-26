## Description: <br>
Uploads one or many MP4 videos to YouTube using OAuth, metadata from UPLOAD_META.md or command-line flags, resumable uploads, and proxy-aware retries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and operators use this skill to upload finished MP4 files or final/ directories to YouTube while preserving titles, descriptions, tags, privacy settings, playlist placement, and scheduled publishing choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Google OAuth access and stores a reusable YouTube upload token. <br>
Mitigation: Create the OAuth client yourself, keep credentials.json and token.json private with user-only file access, and avoid syncing or committing them. <br>
Risk: Batch uploads can publish incorrect files or metadata to a YouTube account. <br>
Mitigation: Run --dry-run for batches, review files and metadata first, and keep uploads unlisted until they have been checked. <br>


## Reference(s): <br>
- [Google Cloud OAuth setup for YouTube upload](references/credentials-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/jianshuo/wjs-uploading-video) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [YouTube upload OAuth scope](https://www.googleapis.com/auth/youtube.upload) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands and upload result summaries; the upload script writes JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Google OAuth credentials and token files, supports dry-run mode, and defaults uploads to unlisted.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
