## Description:

Speech Recognition Local transcribes supported audio files into text locally with faster-whisper, using automatic language detection or Chinese, English, and Japanese language hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zktufo](https://clawhub.ai/user/zktufo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to turn local voice messages, recordings, meetings, and podcast audio into readable text without sending audio to a hosted speech-to-text API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first run may retrieve external dependencies or speech recognition model files unless they are already cached.

Mitigation: Install and cache required dependencies and model files in a reviewed environment before using the skill in restricted or production workflows.

Risk: Voice-message transcription can place sensitive spoken content into an agent conversation.

Mitigation: Only auto-transcribe audio that users are comfortable processing locally and injecting into the active conversation.

Risk: Unsupported formats or audio files larger than 25MB will not be transcribed by the provided script.

Mitigation: Convert audio to .ogg, .m4a, .mp3, or .wav and keep files within the documented 25MB limit before invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zktufo/skills/speech-recognition-local)
- [ClawHub publisher profile](https://clawhub.ai/user/zktufo)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text transcription with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a local audio file path and optional language hint; supports .ogg, .m4a, .mp3, and .wav files up to 25MB.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
