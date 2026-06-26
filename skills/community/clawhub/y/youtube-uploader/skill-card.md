## Description: <br>
Upload videos and custom thumbnails to YouTube with OAuth2 authentication, metadata, scheduling, channel selection, and thumbnail support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nachx639](https://clawhub.ai/user/Nachx639) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and agent operators use this skill to authenticate YouTube channels, upload videos with metadata, schedule releases, and attach custom thumbnails through the YouTube Data API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable YouTube OAuth credentials on disk. <br>
Mitigation: Install only for trusted workflows, keep ~/.openclaw/youtube/channels.json private, use explicit --channel-id values for multi-channel setups, and revoke or delete credentials when no longer needed. <br>
Risk: The skill installs Python packages at runtime. <br>
Mitigation: Review the package list and run the skill in an environment where runtime dependency installation is acceptable. <br>
Risk: Uploads may publish or schedule content on an authenticated YouTube channel. <br>
Mitigation: Upload privately first, verify video metadata and thumbnail output, then change privacy or scheduled publishing settings intentionally. <br>


## Reference(s): <br>
- [YouTube Data API v3](https://developers.google.com/youtube/v3) <br>
- [YouTube Video Category IDs](references/categories.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Nachx639/youtube-uploader) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; upload actions return JSON with videoId and url.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, a Google Cloud OAuth desktop client secret, YouTube Data API access, and local credential storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
