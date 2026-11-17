## Description:

Use when Tony says voice reply or asks to speak. Speaks the response aloud via Doubao TTS to MOMAX BS6.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olddirtybikertony](https://clawhub.ai/user/olddirtybikertony)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill when they want an agent response spoken aloud through Doubao TTS and played on a configured macOS audio output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a plaintext Doubao service token in the skill.

Mitigation: Require the publisher to remove and rotate the embedded token before installation.

Risk: Response text is sent to a third-party TTS service and played aloud.

Mitigation: Document the data flow clearly and avoid using the skill for secrets or private content.

Risk: Invocation guidance may encourage interpolating generated text into a shell command.

Mitigation: Pass speech text as a literal argument or stdin and narrow the trigger phrases before deployment.

## Reference(s):

- [Doubao TTS 2.0 API Reference](references/doubao_tts_api.md)
- [Doubao TTS API endpoint](https://openspeech.bytedance.com/api/v1/tts)
- [ClawHub skill page](https://clawhub.ai/olddirtybikertony/skills/voice-output)

## Skill Output:

**Output Type(s):** [text, shell commands, API Calls, guidance]

**Output Format:** [Spoken audio generated from text, with shell command invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends response text to Doubao TTS and plays returned MP3 audio with afplay.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
