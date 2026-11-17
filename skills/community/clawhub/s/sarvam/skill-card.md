## Description:

Use Sarvam AI for Indian language Text-to-Speech (TTS), Speech-to-Text (STT), Translation, and Chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iammhk](https://clawhub.ai/user/iammhk)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to invoke Sarvam AI for Indian-language speech generation, audio transcription or translation, text translation, and chat from a local CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected text, recordings, and chat prompts are sent to Sarvam AI.

Mitigation: Use the skill only with content approved for Sarvam AI processing, and avoid confidential or regulated audio or text unless that service use is approved.

Risk: The skill depends on SARVAM_API_KEY for API access.

Mitigation: Keep SARVAM_API_KEY scoped and protected, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iammhk/skills/sarvam)
- [ClawHub publisher profile](https://clawhub.ai/user/iammhk)
- [Sarvam AI API endpoint](https://api.sarvam.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [CLI output as plain text or JSON, with optional generated WAV audio files for text-to-speech.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SARVAM_API_KEY and sends selected text, audio, and chat prompts to Sarvam AI.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
