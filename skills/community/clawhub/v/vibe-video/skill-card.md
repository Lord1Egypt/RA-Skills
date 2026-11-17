## Description:

根据主题制作 Vibe 风格无旁白知识视频，完成核查、代码动画、音乐卡点，交付竖屏 2K MP4。

This skill is ready for commercial/non-commercial use.

## Publisher:

[immurray](https://clawhub.ai/user/immurray)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和视频制作人员使用此技能，将知识主题制作成经过事实核查、按音乐节奏剪辑的中文无旁白竖屏动画视频。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local rendering runs commands and writes project and output files.

Mitigation: Run in an isolated project environment and review generated files before delivery.

Risk: User-supplied music and fonts may have licensing restrictions.

Mitigation: Use only audio and fonts you have rights to use.

Risk: Installing npm and pip dependencies can affect the local environment.

Mitigation: Install dependencies in an isolated project environment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/immurray/skills/vibe-video)
- [视觉与叙事标准](references/direction.md)
- [跨运行环境渲染](references/rendering.md)
- [兼容性与调用](references/compatibility.md)

## Skill Output:

**Output Type(s):** [Video files, Markdown, Code, Configuration]

**Output Format:** [MP4 video with supporting project files and technical QA report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default: 60 seconds, 9:16, 1440×2560, 30 fps, H.264 video and AAC audio; no narration.]

## Skill Version(s):

1.1.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
