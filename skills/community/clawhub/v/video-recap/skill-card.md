## Description:

从输入视频生成中文解说成片或原声剧情短片。用户提供 .mp4 / .mov / .mkv / .webm，并要求剪辑、添加旁白、配音、总结或制作短剧/电视剧/电影/纪录片/科普解说时使用。在同一个自包含技能内完成视频理解、导演立意与选镜剪辑、解说撰稿与校验、TTS 配音及音画混音合成。触发词：视频解说、视频旁白、生成解说、视频 recap、video recap、voiceover、narration、recap。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and editing agents use this skill to turn source videos into Chinese recaps or original-audio story cuts, with optional narration, voice synthesis, subtitles, and final assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-controlled file paths may reach outside the dashboard root.

Mitigation: Review paths and use a dedicated dashboard root containing only the projects intended for review.

Risk: When remote analysis or speech services are enabled, media, context, narration text, or voice references may be sent to those providers.

Mitigation: Choose providers deliberately, confirm their data handling and voice authorization, and use local-only processing where it fits the task.

Risk: The security review is incomplete because some components or analysis stages were not fully interpreted.

Mitigation: Review the remaining files and behavior before installation or use with sensitive projects.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/worldwonderer/skills/video-recap)
- [Creative editing playbook](artifact/references/creative-editing-playbook.md)
- [Audio modes](artifact/references/audio-modes.md)
- [Configuration playbook](artifact/references/config-playbook.md)
- [Output data schema](artifact/references/data-schema.md)
- [Resource library](artifact/references/resource-library.md)

## Skill Output:

**Output Type(s):** [Video files, Subtitles, JSON, Markdown]

**Output Format:** [MP4 video, SRT/ASS subtitles, JSON production artifacts, and Markdown briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected workflow and may include intermediate plans, audio, and quality-control reports.]

## Skill Version(s):

1.0.23 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
