## Description: <br>
Speech to text transcribes Brazilian Portuguese audio files to text with OpenAI Whisper, supporting multiple audio formats and timestamped segments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bohnwuks](https://clawhub.ai/user/Bohnwuks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe voice messages and local audio files, especially Brazilian Portuguese audio, into structured text with optional timestamps. It supports single-file transcription, batch processing, and folder watch workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio, transcripts, and logs may contain sensitive personal or business information. <br>
Mitigation: Install in a dedicated Python environment, use a dedicated private inbound folder, and treat generated transcripts and logs as sensitive. <br>
Risk: Processed audio files are moved after transcription, which can disrupt retention workflows if the original location is expected to remain unchanged. <br>
Mitigation: Keep backups of original audio when preservation is required before running batch or watch mode. <br>
Risk: Watch mode continuously monitors and processes new inbound files. <br>
Mitigation: Run watch mode only when ongoing automatic processing is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bohnwuks/stt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON transcription files and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcription output can include full text, language, timing metadata, and timestamped segments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
