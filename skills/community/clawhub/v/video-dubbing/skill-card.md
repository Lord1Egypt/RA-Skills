## Description:

VoxCPM中文配音 helps agents generate Chinese-dubbed versions of foreign-language videos with transcription, translation, VoxCPM speech synthesis, subtitle generation, optional hard-subtitle detection, and BGM support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newaiguy](https://clawhub.ai/user/newaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content localization teams use this skill to create Chinese-dubbed versions of permitted foreign-language videos. The workflow can produce translated speech, subtitles, and optionally mixed background music for localized video outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dubbing workflow may share transcripts and at least one video frame with configured translation or vision APIs.

Mitigation: Use only videos and voice samples the user is allowed to process, avoid sensitive media, and configure trusted API endpoints.

Risk: The package includes a separate authenticated Bilibili upload script.

Mitigation: Remove or isolate scripts/upload_bilibili.py unless authenticated Bilibili publishing is explicitly intended, and keep publishing credentials outside shared skill artifacts.

Risk: Dependencies and external model downloads require review before installation.

Mitigation: Pin and review dependencies and model sources, then run the workflow in an isolated environment before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newaiguy/skills/video-dubbing)
- [VoxCPM](https://github.com/modelscope/VoxCPM)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Hunyuan-MT-7B](https://huggingface.co/tencent/Hunyuan-MT-7B)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of dubbed video and subtitle files through the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
