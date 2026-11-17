## Description:

speech2text transcribes attached ogg, wav, mp3, or m4a voice messages to Chinese text using local Faster-Whisper recognition and ffmpeg conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lqwall26](https://clawhub.ai/user/lqwall26)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to turn voice-message attachments into text for downstream conversation, especially Chinese speech in common audio formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When no current audio attachment is present, the skill can fall back to the newest local inbound audio file, which may expose another user's recording.

Mitigation: Process only audio explicitly attached to the current request before treating the skill as low risk.

Risk: The skill can return local filesystem paths for processed audio.

Mitigation: Avoid returning local paths to users unless an operator explicitly needs them for debugging.

Risk: Audio conversion may create derived wav files beside source files.

Mitigation: Use safe temporary files for conversion and clean them up after transcription.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lqwall26/skills/speech2text)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text transcription or JSON status object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires faster-whisper and ffmpeg; configured for Chinese recognition by default.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
