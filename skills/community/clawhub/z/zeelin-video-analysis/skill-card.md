## Description: <br>
视频分析技能，支持本地视频文件直接上传分析。当用户说'分析视频'、'视频处理'、'分析这个视频'等并上传视频文件时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyayong000-sketch](https://clawhub.ai/user/liyayong000-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to upload local video files to Zeelin, submit video analysis jobs, poll task status, and present extracted entities, relationship graphs, and character profiles as readable Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Videos and the user's App-Key are sent to a plaintext raw-IP Zeelin service. <br>
Mitigation: Install only if the Zeelin backend is trusted, and avoid confidential, personal, or proprietary videos unless a verifiable HTTPS endpoint, retention and privacy terms, and upload confirmation are available. <br>
Risk: Video analysis can consume paid Zeelin credits when tasks are submitted and may run for an extended period. <br>
Mitigation: Confirm expected billing before upload, follow the documented polling intervals, and stop polling after the documented maximum wait time. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liyayong000-sketch/zeelin-video-analysis) <br>
- [Zeelin website](https://skills.zeelin.cn) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Shell commands, Configuration, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown file with structured video-analysis results, plus JSON and multipart API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads videos up to 500MB, polls task status for up to 60 minutes, and formats returned analysis data without inventing missing fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
