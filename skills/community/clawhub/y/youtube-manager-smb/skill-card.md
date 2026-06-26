## Description: <br>
Comprehensive YouTube channel management with video publishing, data analytics, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chao980](https://clawhub.ai/user/chao980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and social media managers use this skill to plan YouTube uploads, inspect channel and video performance, and generate analytics reports from YouTube API data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The upload helper may report a successful YouTube upload without proving that a real API upload occurred. <br>
Mitigation: Use a dedicated YouTube test account first and require evidence of an actual uploaded video before relying on upload results. <br>
Risk: The skill handles YouTube API keys, OAuth client secrets, and refresh tokens. <br>
Mitigation: Store credentials only in protected secret storage and avoid pasting them into prompts, logs, or generated reports. <br>
Risk: Upload, report delivery, notification, or visibility-changing actions can affect a live YouTube channel. <br>
Mitigation: Require explicit user confirmation before performing channel-changing or externally visible actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chao980/youtube-manager-smb) <br>
- [YouTube Data API v3 guide](references/youtube_api_guide.md) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [YouTube Data API v3 endpoint](https://www.googleapis.com/youtube/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON reports, Python helper code, shell commands, and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided YouTube API credentials and channel identifiers; generated upload and reporting actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
