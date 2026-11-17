## Description:

Handles voice-to-voice conversations on WhatsApp by automatically transcribing incoming audio and responding with local TTS audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubenfb23](https://clawhub.ai/user/rubenfb23)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to conduct WhatsApp conversations by voice instead of typing. It transcribes incoming voice notes, processes them as prompts, and returns both text and generated voice-note replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically process private WhatsApp audio and generated replies.

Mitigation: Require explicit opt-in for voice mode, avoid logging transcripts, use private per-response temporary files, and delete audio files after sending.

Risk: TTS command execution can be unsafe if generated text is interpolated into a shell command.

Mitigation: Pass TTS text safely as an argument or via stdin and avoid shell interpolation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Audio files, Shell commands, Guidance]

**Output Format:** [Text responses with generated OGG voice-note files and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local transcription and local TTS tools; expected to return both text and audio.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
