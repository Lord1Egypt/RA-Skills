## Description:

Create a custom voice and synthesize speech from either a user-provided reference recording or a written voice description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through cloning a permitted voice sample or designing a new voice, then generating speech with the selected custom voice model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice samples can contain sensitive personal or biometric information when sent to model provider workflows.

Mitigation: Use recordings the user owns or has explicit permission to process, keep samples short and clean, and review provider retention and deletion terms before upload.

Risk: Cloning a real person's voice without rights can enable impersonation or consent violations.

Mitigation: Confirm likeness consent before cloning and refuse requests to clone third-party voices without permission.

Risk: Poor reference audio can produce inaccurate, garbled, or inconsistent speech.

Mitigation: Use clean single-speaker recordings, validate the returned audio before delivery, and retry with lower-risk settings or better references when quality issues appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runware/skills/voice-cloning)
- [runware publisher profile](https://clawhub.ai/user/runware)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls]

**Output Format:** [Markdown guidance with request fields, model choices, and quality checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides asynchronous audio generation and consent checks; it does not itself produce audio files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
