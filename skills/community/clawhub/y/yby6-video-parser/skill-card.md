## Description: <br>
Parses short-video and image-post links from major platforms, extracts video metadata, and can transcribe video audio to text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangbuyiya](https://clawhub.ai/user/yangbuyiya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation users use this skill to parse social video or image-post links, retrieve metadata such as media URLs, cover images, titles, and authors, and optionally produce text transcripts and Markdown reports from video audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch loosely validated video URLs and follow platform redirects. <br>
Mitigation: Use trusted input sources, prefer allowlisted platform domains, and review links before running the parser or transcription workflow. <br>
Risk: The transcription workflow can upload extracted audio to SiliconFlow. <br>
Mitigation: Avoid processing sensitive or private media unless that external transcription service is approved for the data involved. <br>
Risk: Generated reports and temporary media may be retained locally. <br>
Mitigation: Enable temporary-file cleanup for sensitive content and review generated files under demos/ and tmp/ before sharing or deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yangbuyiya/yby6-video-parser) <br>
- [SiliconFlow audio transcription API documentation](https://docs.siliconflow.cn/api-reference/audio) <br>
- [parse-video-py project credited by skill documentation](https://github.com/wujunwei928/parse-video-py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [JSON metadata responses, plain text transcription, Markdown reports, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write Markdown reports under demos/ and temporary media files under tmp/ unless cleanup is enabled.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
