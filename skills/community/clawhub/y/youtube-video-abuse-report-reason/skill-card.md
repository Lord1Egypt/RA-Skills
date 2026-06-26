## Description: <br>
Manage YouTube video abuse report reasons by guiding agents to list available reasons through the yutu CLI, with setup steps for first-time users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover valid YouTube video abuse report reasons through the yutu CLI before making or validating related YouTube API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires YouTube OAuth credential and token files that can grant account access if exposed. <br>
Mitigation: Treat client_secret.json and youtube.token.json as secrets; keep them out of commits, logs, and shared messages, store them with restricted permissions, and rotate or revoke access if exposure is suspected. <br>
Risk: The skill depends on the third-party yutu CLI for YouTube API operations. <br>
Mitigation: Install yutu only from trusted sources and review the package or binary source before using it with OAuth credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/OpenWaygate/youtube-video-abuse-report-reason) <br>
- [Yutu Homepage](https://github.com/eat-pray-ai/yutu) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Video Abuse Report Reason List](references/videoAbuseReportReason-list.md) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference yutu output modes such as table, JSON, or YAML when listing abuse report reasons.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
