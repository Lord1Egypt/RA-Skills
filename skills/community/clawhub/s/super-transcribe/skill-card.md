## Description: <br>
Unified speech-to-text skill for transcribing audio or video, generating subtitles, identifying speakers, translating speech, searching transcripts, diarizing meetings, and handling clearly requested voice-message transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThePlasmak](https://clawhub.ai/user/ThePlasmak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to convert local or linked audio/video into transcripts, subtitles, translations, speaker-labeled meeting notes, and searchable transcript artifacts. Agents can use it when user intent to transcribe voice or audio content is explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime setup can create local virtual environments and download ML packages or model weights. <br>
Mitigation: Review setup behavior before installation, use the documented dry-run or check flow where available, and approve expected downloads before running setup or transcription. <br>
Risk: The skill can fetch user-provided URLs for transcription. <br>
Mitigation: Only process URLs that the user explicitly provides or authorizes, and avoid using the skill as a general-purpose URL fetcher. <br>
Risk: Voice and audio content may contain sensitive personal or confidential information. <br>
Mitigation: Require clear user intent before transcribing voice notes or recordings, and avoid processing sensitive audio unless the user has authorized that use. <br>
Risk: The documented ./scripts/transcribe launcher is missing from the published artifact according to security evidence. <br>
Mitigation: Confirm the launcher exists or use a corrected package version before relying on documented commands in production workflows. <br>
Risk: HuggingFace tokens may be needed for gated diarization models. <br>
Mitigation: Prefer cached or interactive authentication and avoid passing HuggingFace tokens directly on the command line. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ThePlasmak/super-transcribe) <br>
- [NVIDIA CUDA on WSL User Guide](https://docs.nvidia.com/cuda/wsl-user-guide/) <br>
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) <br>
- [faster-whisper model collection](https://huggingface.co/collections/Systran/faster-whisper) <br>
- [pyannote speaker diarization 3.1](https://hf.co/pyannote/speaker-diarization-3.1) <br>
- [pyannote segmentation 3.0](https://hf.co/pyannote/segmentation-3.0) <br>
- [pyannote.audio](https://github.com/pyannote/pyannote-audio) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [Referenced arXiv paper](https://arxiv.org/abs/2311.00430) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; transcription outputs may be plain text, JSON, subtitle files, CSV, HTML, podcast RSS-derived transcript files, or extracted speaker audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports agent-oriented compact JSON output, batch processing, backend selection, transcript search, diarization, translation, chapter detection, and multiple subtitle/export formats.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence, skill.json, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
