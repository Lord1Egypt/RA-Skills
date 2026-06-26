## Description: <br>
Transcribe audio files (WAV/MP3/M4A/FLAC) to timestamped text using SenseVoice-Small + FSMN-VAD, with single-file and batch modes for VAD-anchored per-segment timestamps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylongw](https://clawhub.ai/user/ylongw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe speech recordings into timestamped text, either one file at a time or across daylog batches. It is especially oriented toward Chinese audio transcription with SenseVoice-Small and FSMN-VAD timestamp anchoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch re-transcription with --force-dates can replace existing transcript outputs. <br>
Mitigation: Run --dry-run first and use --force-dates only for dates that should be regenerated. <br>
Risk: Optional Discord webhook notifications share progress metadata such as dates, counts, and possible failure filenames with the configured endpoint. <br>
Mitigation: Provide a Discord webhook only when sharing that metadata externally is acceptable. <br>
Risk: First use installs Python ML dependencies and downloads transcription and VAD models. <br>
Mitigation: Install in the documented virtual environment and proceed only if the dependency and model downloads are acceptable for the target system. <br>


## Reference(s): <br>
- [SenseVoice Transcribe on ClawHub](https://clawhub.ai/ylongw/sensevoice-transcribe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with shell commands and timestamped text transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch mode can write transcript files, progress JSON, and optional Discord webhook notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
