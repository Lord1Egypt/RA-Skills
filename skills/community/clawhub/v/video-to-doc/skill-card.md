## Description: <br>
将操作视频自动转换为图文并茂的 Word 操作指南，支持智能截图、语音转录、LLM 内容提炼和流程图生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siyou315](https://clawhub.ai/user/siyou315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to convert software demonstrations, system walkthroughs, training videos, and product demos into Word operation guides with screenshots, transcribed narration, structured steps, flow diagrams, and notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic dependency installation may fetch unpinned packages or system tools. <br>
Mitigation: Review the install commands first and prefer installing pinned dependencies from trusted package sources. <br>
Risk: License and usage checks may contact xiaping.coze.site when XIAPING_TOKEN is used. <br>
Mitigation: Confirm the network call and token handling are acceptable for the deployment environment before running the skill. <br>
Risk: Transcripts or generated content may be sent to Anthropic or OpenAI when those API paths and keys are configured. <br>
Mitigation: Use only videos and transcripts you are allowed to process, and prefer local transcription or local review when remote processing is not acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/siyou315/video-to-doc) <br>
- [Video to Doc README](README.md) <br>
- [视频转文档操作指南](references/guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands plus generated .docx, JSON, audio, and image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill accepts a video path and can produce extracted frame images, audio transcription JSON, screenshot analysis JSON, and a Word operation guide.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
