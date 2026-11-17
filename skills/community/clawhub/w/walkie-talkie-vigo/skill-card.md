## Description:

Handles voice-to-voice conversations on WhatsApp by transcribing incoming audio and responding with local TTS audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubenfb23](https://clawhub.ai/user/rubenfb23)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they want WhatsApp voice-note conversations: the agent transcribes incoming audio, processes it as a prompt, and returns both text and voice output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WhatsApp voice notes may contain sensitive spoken content that is transcribed and processed by the agent.

Mitigation: Use an explicit opt-in and disable flow for walkie-talkie mode, and make it clear when incoming audio will be transcribed.

Risk: The manual TTS example writes synthesized audio to a fixed temporary path, which can overwrite or expose prior responses on shared systems.

Mitigation: Generate a unique private temporary .ogg file for each response and delete it after the voice note is sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rubenfb23/skills/walkie-talkie-vigo)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown/plain text guidance with bash commands and OGG audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local .ogg voice-note files alongside text responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
