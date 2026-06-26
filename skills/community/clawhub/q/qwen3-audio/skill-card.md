## Description: <br>
High-performance audio library for Apple Silicon with text-to-speech (TTS) and speech-to-text (STT). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarkNoah](https://clawhub.ai/user/DarkNoah) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and audio workflow builders use this skill on Apple Silicon Macs to run Qwen3-based text-to-speech, speech-to-text, voice cloning, voice profile management, and subtitle generation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install external prerelease code during normal use. <br>
Mitigation: Review before installing; create the uv environment yourself and preinstall a pinned mlx-audio version instead of relying on the automatic install path. <br>
Risk: Voice profiles, transcripts, subtitles, and generated audio can contain sensitive local data. <br>
Mitigation: Only clone voices you are authorized to use and treat saved voices/, transcript, subtitle, and audio files as sensitive local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DarkNoah/qwen3-audio) <br>
- [Environment checklist](references/env-check-list.md) <br>
- [Hugging Face](https://huggingface.co) <br>
- [Qwen3 ASR sample audio](https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav) <br>
- [Hugging Face mirror endpoint](https://hf-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown usage guidance with shell commands and JSON-producing CLI workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can generate WAV audio files, text transcripts, SRT subtitles, ASS subtitles, and reusable local voice profiles.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
