## Description:

Guides agents in generating speech, dialogue, and sound or transcribing audio with ElevenLabs through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to produce or transcribe audio through RunAPI and to integrate ElevenLabs into applications using an SDK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private prompts, text, or audio may be sent to RunAPI and ElevenLabs.

Mitigation: Review request contents and confirm that sharing sensitive material is acceptable before submission.

Risk: Audio generation and transcription may incur paid usage.

Mitigation: Confirm the operation and expected cost before submitting a task; avoid duplicate submissions.

Risk: Authentication credentials may be exposed through unsafe handling.

Mitigation: Prefer an environment API key or explicit token import rather than placing credentials in requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/runapi-ai/skills/runapi-elevenlabs)
- [RunAPI ElevenLabs models and pricing](https://runapi.ai/models/elevenlabs.md)
- [RunAPI ElevenLabs provider](https://runapi.ai/providers/elevenlabs.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI ElevenLabs SDK integration](https://github.com/runapi-ai/elevenlabs-sdk)

## Skill Output:

**Output Type(s):** [Audio files, Text, Code, Shell commands]

**Output Format:** [Audio files, JSON, text, SRT or VTT; code for app integrations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected operation; downloaded media must be verified.]

## Skill Version(s):

0.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
