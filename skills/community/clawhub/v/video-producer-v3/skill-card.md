## Description:

短视频一键生成器 v3.0。输入主题+要点，AI自动完成分镜、生图、配音、字幕、渲染，输出1080×1920竖屏MP4。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyjaixiao](https://clawhub.ai/user/hyjaixiao)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate short vertical videos from a topic and structured talking points, including storyboard JSON, images, TTS audio, subtitles, and MP4 render outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided video text or output paths can reach shell command execution during media generation.

Mitigation: Run only in a sandboxed working directory and avoid untrusted video text or output paths.

Risk: API credentials and generated content can be sent to configurable external MiniMax, OpenAI, or Edge services.

Mitigation: Use trusted API hosts only, do not set OPENAI_BASE to an untrusted proxy, and document what content and credentials are sent to each backend.

Risk: The security verdict is suspicious and calls for review before installation.

Mitigation: Review before installing and prefer a version that removes shell=True and validates API hosts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyjaixiao/skills/video-producer-v3)
- [MiniMax API base](https://api.minimaxi.com/v1)
- [OpenAI API base](https://api.openai.com/v1)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, files]

**Output Format:** [Python script behavior with JSON storyboard, generated media files, MP4 video, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, FFmpeg, and optional MiniMax, OpenAI, or Edge TTS credentials depending on selected backends.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact files self-identify as 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
