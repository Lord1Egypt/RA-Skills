## Description:

Unified speech-to-text skill for transcribing audio or video, generating subtitles, identifying speakers, translating speech, searching transcripts, diarizing meetings, and handling other speech-to-text tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theplasmak](https://clawhub.ai/user/theplasmak)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to route speech-to-text requests through bundled Parakeet or faster-whisper backends, producing transcripts, subtitles, diarization, translation, and transcript search outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process voice messages or recordings that may include sensitive or third-party speech.

Mitigation: Confirm user intent and appropriate consent before transcribing, diarizing, translating, or exporting speaker audio from recordings.

Risk: URL and RSS transcription can fetch content from untrusted links.

Mitigation: Use URL and RSS inputs only from trusted sources and review fetched media before processing sensitive workflows.

Risk: Setup and runtime paths may install or upgrade packages, including unpinned dependencies.

Mitigation: Review setup behavior before installation, prefer explicit setup, and pin or mirror dependencies in managed environments.

Risk: Generated HTML transcript output may include untrusted metadata.

Mitigation: Treat generated HTML as untrusted until metadata escaping is verified or fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theplasmak/skills/super-transcribe)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [faster-whisper models](https://huggingface.co/collections/Systran/faster-whisper)
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [pyannote speaker diarization 3.1](https://hf.co/pyannote/speaker-diarization-3.1)
- [pyannote segmentation 3.0](https://hf.co/pyannote/segmentation-3.0)
- [NVIDIA CUDA on WSL User Guide](https://docs.nvidia.com/cuda/wsl-user-guide/)
- [Parakeet reference paper](https://arxiv.org/abs/2311.00430)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional transcript files such as text, JSON, SRT, VTT, ASS, LRC, TTML, CSV, and HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transcript metadata, speaker labels, timestamps, search hits, chapter markers, confidence cues, and output file paths depending on selected options.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
