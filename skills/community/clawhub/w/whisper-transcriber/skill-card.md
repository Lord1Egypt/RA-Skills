## Description: <br>
Offline speech-to-text (ASR) using whisper.cpp (whisper-cli) + ffmpeg. Supports batch transcription, timestamps, SRT/TXT/JSON outputs, and model download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vvusu](https://clawhub.ai/user/vvusu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creators, and operators use this skill to transcribe local audio or video-derived audio into text, subtitles, or JSON without sending the media to a hosted transcription service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow may install local packages and download Whisper model files from Hugging Face. <br>
Mitigation: Review the installer before running it, pre-download approved models in restricted environments, and use checksum verification where available. <br>
Risk: Audio files and transcripts can contain sensitive or regulated information. <br>
Mitigation: Get consent before transcription, restrict transcript access, and avoid unnecessary retention of audio or transcript files. <br>
Risk: Automatic speech recognition can produce incorrect transcripts, especially on noisy or high-stakes audio. <br>
Mitigation: Have a human review important transcripts and compare model choices when accuracy matters. <br>


## Reference(s): <br>
- [Whisper.cpp documentation](artifact/references/WHISPER_DOCS.md) <br>
- [Available Whisper models](artifact/references/AVAILABLE_MODELS.md) <br>
- [Whisper.cpp GitHub](https://github.com/ggml-org/whisper.cpp) <br>
- [Whisper.cpp model repository](https://huggingface.co/ggerganov/whisper.cpp) <br>
- [OpenClaw Skill System](https://docs.openclaw.ai/skills) <br>
- [ClawHub release page](https://clawhub.ai/vvusu/whisper-transcriber) <br>
- [Publisher profile](https://clawhub.ai/user/vvusu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain text transcripts, SRT subtitles, JSON output, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-file and batch transcription with configurable model, language, output path, and temporary directory settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
