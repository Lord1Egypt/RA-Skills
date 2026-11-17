## Description:

Offline speech-to-text conversion using a local Vosk model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gs431047](https://clawhub.ai/user/gs431047)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can use this skill to transcribe a provided WAV audio file into text with a local Vosk model. It is useful when audio transcription should run offline and return a simple transcript object.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the audio file path supplied by the user.

Mitigation: Run it in an isolated, unprivileged environment and provide only intended audio files.

Risk: The runtime dependency is not pinned in the artifact requirements.

Mitigation: Pin and review dependency versions before deployment.

Risk: The skill requires a local Vosk model directory and a 16 kHz mono 16-bit WAV input.

Mitigation: Provision the model directory and validate audio format before invoking the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gs431047/skills/voice2text)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON object containing transcript text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-provided WAV file path and requires a local Vosk model directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
