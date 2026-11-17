## Description:

Handles voice-to-voice conversations on WhatsApp by transcribing incoming audio and responding with local text-to-speech audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubenfb23](https://clawhub.ai/user/rubenfb23)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to conduct WhatsApp conversations by voice instead of typing. The agent transcribes incoming voice notes, processes them as prompts, and returns both text and local TTS audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incoming WhatsApp audio may be transcribed and answered automatically in chats where this skill is active.

Mitigation: Confirm participants expect voice notes to be processed by the agent before enabling the skill for a chat.

Risk: Using a fixed temporary output path such as /tmp/reply.ogg can overwrite prior audio or expose content across requests on shared systems.

Mitigation: Use a unique per-request temporary audio file and remove it after sending.

Risk: Sensitive conversations can be converted into text and synthetic audio during normal skill operation.

Mitigation: Avoid using the skill for sensitive conversations unless all participants understand and accept the processing behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rubenfb23/skills/walkie-talkie)
- [Publisher profile](https://clawhub.ai/user/rubenfb23)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Text and generated OGG audio voice note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local audio transcription and text-to-speech tooling; replies include both text and audio.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
