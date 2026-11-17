## Description:

Cross-platform video subtitle extraction using multi-engine ASR: it downloads audio from video URLs with yt-dlp, transcribes with SenseVoice, whisper.cpp, or openai-whisper, and can calibrate Chinese financial and technical transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forhonourlx](https://clawhub.ai/user/forhonourlx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content teams use this skill to extract subtitles or transcript files from videos that lack built-in captions, especially Chinese-language financial or technical videos. It guides agents through dependency setup, media download, ASR transcription, optional video retention, and transcript calibration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broad install, download, browser-cookie, and persistent storage behaviors.

Mitigation: Review the skill before use, run it only in a trusted environment, and approve dependency installation and media downloads deliberately.

Risk: Browser-cookie workflows can expose account session material to the local toolchain.

Mitigation: Avoid browser-cookie options unless the machine and toolchain are trusted; prefer videos that do not require cookies.

Risk: Downloaded media and generated transcripts can remain on disk after execution.

Mitigation: Use a dedicated output directory and delete media, transcripts, and metadata after they are no longer needed.

## Reference(s):

- [ASR Model Selection Guide](artifact/references/asr_models.md)
- [Text Calibration Guide for Chinese ASR Output](artifact/references/calibration_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/forhonourlx/skills/video-subtitle-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated transcript files such as TXT, SRT, VTT, and JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent media, transcript, subtitle, metadata, and calibrated transcript files in the selected output directory.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
