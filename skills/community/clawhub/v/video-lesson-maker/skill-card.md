## Description:

从教材、课件或科普文章提炼视频主题，并组织白板动画、配音与同步字幕的制作流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[8288hit](https://clawhub.ai/user/8288hit)

### License/Terms of Use:

MIT-0

## Use Case:

教师、教育内容创作者和视频制作人员可用此 skill 将教材或科普文章拆解为视频主题，并制作白板动画、口播配音及同步字幕。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes watermark removal, which may be outside the expected video-making purpose.

Mitigation: Confirm you have the rights to modify the source media and remove its watermark before using that capability.

Risk: Narration text is processed by an external text-to-speech service, which may expose private document content.

Mitigation: Do not send confidential or personal material to external TTS unless its use is approved; use non-sensitive narration text when possible.

Risk: The security scan reports a risky file-writing path and was only partial.

Mitigation: Review the output paths before execution, use a dedicated working directory, and preserve source files; treat uninspected behavior as not fully assessed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/8288hit/skills/video-lesson-maker)
- [主题凝练指南](artifact/references/theme-refinement.md)
- [视频制作流水线](artifact/references/pipeline.md)
- [口播脚本与字幕规范](artifact/references/srt-guidelines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown, SRT, JSON, Python scripts, shell commands, and narrated video files with synchronized subtitles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary with the source document and video project.]

## Skill Version(s):

1.4.1 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
