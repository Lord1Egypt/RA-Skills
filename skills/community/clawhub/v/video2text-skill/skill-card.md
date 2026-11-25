## Description:

将本地 MP4 或可直接下载的 MP4 转写为文字，并可按提示生成摘要、改写、金句、分镜脚本或翻译。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

内容创作者、会议参与者和学习者可用它从 MP4 视频中提取转写文本，并整理会议、课程、采访或直播内容，或生成摘要、翻译和改写文案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video files are uploaded to the service for processing, and scan coverage was incomplete.

Mitigation: Only submit videos you are comfortable sending to the service; the release documentation says processed videos are deleted after 24 hours.

Risk: Using the skill requires an activated service token and may incur per-video charges or consume a daily allowance.

Mitigation: Confirm the token plan and current pricing before processing a video, especially before retrying with a different prompt.

Risk: The skill removes expired downloaded files from its temporary storage during execution.

Mitigation: Review the temporary download directory and retain any files you need before they expire.

## Reference(s):

- [视频文案智能提取官网](https://www.guaikei.com)
- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/video2text-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown, depending on the requested transformation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one MP4 per command; supports transcription and prompt-directed summaries, rewrites, quotes, storyboards, and translation.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
