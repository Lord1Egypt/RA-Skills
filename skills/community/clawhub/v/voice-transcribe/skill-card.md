## Description: <br>
Transcribe audio files using OpenAI's gpt-4o-mini-transcribe model with vocabulary hints and text replacements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darinkishore](https://clawhub.ai/user/darinkishore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to transcribe voice memos and other supported audio files, then respond based on the transcript. It also supports custom vocabulary hints and deterministic text replacements for recurring transcription errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an unbundled hard-coded local transcription script. <br>
Mitigation: Install or use it only after reviewing and trusting the referenced local script. <br>
Risk: Voice audio can be uploaded to OpenAI using a local API key. <br>
Mitigation: Use a dedicated OpenAI API key and avoid processing sensitive or third-party recordings without consent. <br>
Risk: Transcripts or cached audio-derived data may be stored locally by the transcription workflow. <br>
Mitigation: Check where transcripts and cache files are stored and confirm how to clear them before processing sensitive audio. <br>


## Reference(s): <br>
- [Voice Transcribe ClawHub page](https://clawhub.ai/darinkishore/voice-transcribe) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript with optional Markdown guidance and configuration file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports custom vocabulary hints, post-processing replacements, supported audio formats, and SHA-256-based audio caching.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
