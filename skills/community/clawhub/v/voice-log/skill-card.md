## Description:

Background voice journaling with Soniox realtime STT for OpenClaw; it requires SONIOX_API_KEY and supports starting or stopping passive speech logging and summarizing recent conversation transcript text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easwee](https://clawhub.ai/user/easwee)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to start and stop a voice journal, keep a rolling one-hour local transcript, and ask an agent to summarize recent minutes of conversation. It is most useful when hands-free conversation recap is needed and the user is comfortable with live microphone capture and Soniox transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records microphone audio and may capture people who have not consented.

Mitigation: Start the journal only in consented settings, stop it when finished, and avoid use around bystanders who have not agreed to be recorded.

Risk: Audio is sent to Soniox for transcription and a rolling transcript is stored locally while the journal is running.

Mitigation: Use the skill only where third-party transcription and local transcript retention are acceptable, and manage the local .data directory according to the user's privacy policy.

Risk: The Soniox dependency is version-ranged in package metadata.

Mitigation: Pin and review the Soniox dependency before sensitive or regulated use.

## Reference(s):

- [Voice Log on ClawHub](https://clawhub.ai/easwee/skills/voice-log)
- [Soniox Speech-to-Text](https://soniox.com/speech-to-text)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Short text responses, optional transcript excerpts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript retrieval is capped at 1800 characters by default unless the command requests full output or a different maximum.]

## Skill Version(s):

0.1.5 (source: release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
