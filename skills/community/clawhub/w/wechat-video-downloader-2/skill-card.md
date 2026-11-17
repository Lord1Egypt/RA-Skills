## Description:

Parses WeChat Channels share links through RedFox to return the video title, cover image, and direct download URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, operations staff, and video editors use this skill to resolve one or more WeChat Channels share links into downloadable video links and metadata for permitted archiving, editing, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted WeChat video links and the RedFox API key are sent to RedFox for processing.

Mitigation: Install only if this data sharing is acceptable, and keep the API key out of chats, logs, repositories, and shared configuration files.

Risk: The skill can produce direct download links for WeChat Channels videos.

Mitigation: Use it only for videos the user owns or has permission to download.

Risk: Returned download links are temporary.

Mitigation: Save permitted downloads promptly after resolution instead of relying on the links for long-term access.

## Reference(s):

- [Server-resolved source import](https://github.com/redfox-data/redfox-community/tree/main/skills/wechat-video-downloader)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/wechat-video-downloader-2)
- [Core Workflow](references/core_workflow.md)
- [RedFox API keys](https://redfox.hk/settings/api-keys?source=github)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown response with title, cover image link, download URL, and failure messages; script output is a JSON array for agent formatting.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; WeChat Channels download links are temporary and should be saved promptly.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
