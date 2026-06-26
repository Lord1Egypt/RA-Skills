## Description: <br>
Extracts subtitles from video URLs or audio files by downloading media with yt-dlp, transcribing with SenseVoice, whisper.cpp, or openai-whisper, and optionally applying rule-based calibration for Chinese financial and technical content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forhonourlx](https://clawhub.ai/user/forhonourlx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and content operators use this skill to generate transcripts and subtitle files for videos that do not already provide captions, especially Chinese-language videos that need ASR transcription and terminology cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-cookie based downloads can expose logged-in account sessions. <br>
Mitigation: Use cookie options only when necessary, prefer a dedicated browser profile, and delete exported cookies or downloaded session-derived artifacts after use. <br>
Risk: The skill downloads media, dependencies, and ASR models and stores audio, optional video, transcripts, and metadata locally. <br>
Mitigation: Run it in a dedicated output directory, avoid saving full video unless needed, and review or remove local artifacts when processing is complete. <br>
Risk: ASR transcripts and rule-based calibration can contain transcription errors or terminology corrections that do not match the source audio. <br>
Mitigation: Review low-confidence or important transcript sections against the source media before relying on the generated subtitles. <br>


## Reference(s): <br>
- [Video Subtitle Extractor on ClawHub](https://clawhub.ai/forhonourlx/video-subtitle-extractor) <br>
- [ASR Model Selection Guide](references/asr_models.md) <br>
- [Text Calibration Guide for Chinese ASR Output](references/calibration_guide.md) <br>
- [PyTorch CPU wheel index](https://download.pytorch.org/whl/cpu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated agent artifacts include TXT, SRT, VTT, JSON, optional MP4/M4A media files, and pipeline metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The pipeline writes artifacts to a local output directory and may download ASR models or dependencies on first use.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
