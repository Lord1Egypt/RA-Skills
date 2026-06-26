## Description: <br>
Free local speech-to-text transcription using OpenAI Whisper for converting audio and video files into text or subtitle formats without cloud API costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickylin](https://clawhub.ai/user/nickylin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and other external users use this skill to run local speech-to-text transcription, convert voice recordings to text, and generate SRT or VTT subtitles from audio or video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcripts can expose sensitive audio contents in terminal output or generated text and subtitle files. <br>
Mitigation: Only transcribe files the user is comfortable processing locally, and review or delete generated transcript files according to the user's data handling needs. <br>
Risk: Whisper models may require downloads and significant disk, RAM, or GPU resources. <br>
Mitigation: Install dependencies in a virtual environment, choose a model size appropriate for the machine, and expect local model storage and compute usage. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://github.com/openai/whisper) <br>
- [Whisper STT ClawHub page](https://clawhub.ai/nickylin/whisper-stt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated transcripts may be JSON, plain text, SRT, or VTT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports selectable Whisper model size, optional language code, and output format selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
