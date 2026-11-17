## Description:

视频分析技能，支持本地视频文件直接上传分析。当用户说'分析视频'、'视频处理'、'分析这个视频'等并上传视频文件时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyayong000-sketch](https://clawhub.ai/user/liyayong000-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to upload local video files to the Zeelin service for analysis, then receive structured entities, relationship graphs, and character profiles formatted for review. The skill is suited to video content analysis workflows where sending video files to the third-party service is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads private video files and an App-Key to a hard-coded plain-HTTP service.

Mitigation: Use only with videos approved for transfer to the Zeelin service, avoid placing valuable long-lived credentials in the template config, and wait for HTTPS plus clear upload, retention, and credential-handling assurances before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyayong000-sketch/skills/zeelin-video-analysis)
- [Zeelin service website](https://skills.zeelin.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with API workflow guidance, configuration JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a Markdown file containing formatted video analysis results after upload, task submission, and status polling complete.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
