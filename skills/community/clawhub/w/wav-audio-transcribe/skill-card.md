## Description: <br>
Audio Transcribe helps agents transcribe local audio with Whisper into plain text, SRT subtitles, or JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-tesing](https://clawhub.ai/user/ai-tesing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and other users can use this skill to transcribe meetings, podcasts, voice notes, or media files into readable text, subtitle, or structured JSON outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script may automatically install or upgrade openai-whisper with pip, modifying the local Python environment. <br>
Mitigation: Preinstall reviewed, pinned dependencies in a virtual environment and remove or gate automatic installation before sensitive or managed use. <br>
Risk: Whisper model loading may download external model files even though the skill is framed as offline and private. <br>
Mitigation: Pre-cache approved models or run only where external downloads are allowed; avoid strict offline or highly sensitive environments until downloads are explicitly controlled. <br>
Risk: Audio transcription accuracy depends on source quality and selected model size. <br>
Mitigation: Review generated transcripts before relying on them, especially for noisy recordings, secondary recordings, or decision-critical uses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ai-tesing/wav-audio-transcribe) <br>
- [README](README.md) <br>
- [Troubleshooting Notes](ISSUES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcripts, SRT subtitle text, JSON transcription data, and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script writes transcript files next to the input audio with a _transcript suffix.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
