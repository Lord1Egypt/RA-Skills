## Description: <br>
短视频一键生成器 v3.0。输入主题+要点，AI自动完成分镜、生图、配音、字幕、渲染，输出1080×1920竖屏MP4。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyjaixiao](https://clawhub.ai/user/hyjaixiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and developers use this skill to generate short vertical videos from a topic and structured talking points. It produces storyboard data, generated scene images, TTS audio, subtitles, and an MP4 suitable for short-video platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The normal video-generation path can run unsafe local shell commands from user-supplied text or paths. <br>
Mitigation: Review or sandbox the Python script before installation, avoid untrusted topics, scripts, titles, subtitles, and output paths, and fix shell command construction before broader use. <br>
Risk: The skill requires sensitive provider credentials and may send video prompts, scripts, or audio text to selected AI providers. <br>
Mitigation: Use limited-scope provider keys, keep OPENAI_BASE pointed at a trusted host, and avoid submitting confidential content unless the selected provider is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hyjaixiao/video-producer-v3) <br>
- [Publisher profile](https://clawhub.ai/user/hyjaixiao) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [Directory of generated media files, JSON storyboard, SRT subtitles, and MP4 video output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, FFmpeg, and provider credentials for full MiniMax or OpenAI-backed media generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports product version 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
