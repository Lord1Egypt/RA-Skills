## Description: <br>
Voice Transcriber Toolkit supports speech recognition with Whisper and Vosk engines, batch audio transcription, audio conversion, and SRT/VTT subtitle export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to transcribe local audio files, process batches of recordings, convert audio to WAV, and generate subtitle files for meetings, media, or documentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill requires ffmpeg and Python media/transcription packages, which introduce ordinary dependency and media-processing risks. <br>
Mitigation: Install only in an environment where those dependencies are acceptable, and use pinned dependencies or a sandbox when reproducible or isolated execution is required. <br>
Risk: Audio files may contain sensitive speech content. <br>
Mitigation: Process sensitive audio only in an approved local environment and review storage, retention, and sharing practices for generated transcripts and subtitles. <br>
Risk: Audio conversion outputs can overwrite existing files when directed at an important output path. <br>
Mitigation: Choose non-critical output paths and review conversion targets before running ffmpeg-based conversion. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/voice-transcriber-toolkit) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [requirements.txt](requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets, shell commands, and structured transcription outputs such as text, JSON-like dictionaries, SRT, and WebVTT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local transcription results and optional subtitle exports; audio conversion depends on ffmpeg.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
