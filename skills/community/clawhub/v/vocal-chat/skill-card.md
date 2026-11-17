## Description:

Handles voice-to-voice conversations on WhatsApp by transcribing incoming audio and responding with local text-to-speech audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubenfb23](https://clawhub.ai/user/rubenfb23)

### License/Terms of Use:


## Use Case:

Agents use this skill to support WhatsApp voice-note conversations for users who prefer speaking instead of typing. It transcribes incoming voice messages, processes the text as a normal prompt, and returns both text and an OGG voice reply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may not expect WhatsApp voice notes to be transcribed and answered by the agent.

Mitigation: Confirm the voice-note behavior before installing or enabling the skill.

Risk: Generated audio can create a temporary-file safety concern.

Mitigation: Use a private unique temporary file for generated audio and delete it after sending.

## Reference(s):

- [Vocal Chat on ClawHub](https://clawhub.ai/rubenfb23/skills/vocal-chat)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Text instructions with inline shell commands and generated OGG audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local transcription and local text-to-speech tools; generated audio should be handled as conversational user data.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-01-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
