## Description:

Video Dubbing helps agents guide users through converting foreign-language videos into Chinese-dubbed videos with subtitles, VoxCPM text-to-speech, Whisper transcription, translation, and optional background music.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newaiguy](https://clawhub.ai/user/newaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content localization teams use this skill to prepare Chinese-dubbed versions of foreign-language videos, including transcription, translation, TTS generation, subtitle generation, video merging, and optional background music.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote translation and vision APIs may receive media-derived content during dubbing workflows.

Mitigation: Use separate, narrowly scoped API keys and only configure trusted translation and vision API endpoints.

Risk: The artifact bundles account-based Bilibili publishing behavior that may be unnecessary for ordinary dubbing use.

Mitigation: Review or remove scripts/upload_bilibili.py unless Bilibili publishing is explicitly required.

Risk: Configurable API URLs and unpinned external dependencies or model revisions can increase supply-chain and credential-forwarding risk.

Mitigation: Avoid overriding API URLs to untrusted hosts, pin dependencies and model revisions, and run the skill in an isolated workspace with limited file and network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newaiguy/skills/voxcpm-chinese-dubbing)
- [VoxCPM](https://github.com/modelscope/VoxCPM)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Hunyuan-MT-7B](https://huggingface.co/tencent/Hunyuan-MT-7B)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dubbed MP4 video, WAV audio, SRT subtitles, and optional BGM-mixed video files when the referenced scripts are run.]

## Skill Version(s):

1.2.0 (source: server release evidence; artifact frontmatter and manifest remain 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
