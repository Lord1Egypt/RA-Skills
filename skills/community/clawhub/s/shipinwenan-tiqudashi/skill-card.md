## Description:

将视频内容转写为文本，支持网络视频链接和本地视频文件，并可按提示词生成总结、改写文案及其他内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要处理已录制视频的内容创作者、教师、采访整理者和会议参与者，可将 MP4 语音转成文稿，并按提示词提炼总结、改写文案、提取金句或翻译。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a third-party token requirement and promotional flow.

Mitigation: Confirm the provider and billing terms before use, and keep GUAIKEI_API_TOKEN private in the intended execution environment.

Risk: The security review reports possible file deletion during downloads or startup cleanup, and notes that only 9 of 20 components were fully inspected.

Mitigation: Review cleanup behavior and affected paths before broader use; test with disposable inputs and keep backups of important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/shipinwenan-tiqudashi)
- [Provider website](https://www.guaikei.com)
- [changelog.md](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Plain text or Markdown; shell commands for running a transcription or prompt-based task]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one MP4 at a time; returns a transcription by default or prompt-directed content such as a summary, rewrite, quotes, storyboard, or translation.]

## Skill Version(s):

1.1.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
