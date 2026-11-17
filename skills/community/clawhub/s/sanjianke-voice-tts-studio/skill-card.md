## Description:

Helps agents use a7w voice services for speech synthesis, voice cloning, transcription, and voice discovery through documented API calls and a bundled command-line client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creators use this skill to configure their own a7w API key and guide an agent in generating speech, transcribing audio, cloning authorized voices, and checking available voice models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The client can use a spend-capable API key to invoke other a7w marketplace plugins, not just voice services.

Mitigation: Use a limited or separate key when possible, restrict agent access to intended calls, and monitor charges.

Risk: Submitted text and audio are processed by the external provider.

Mitigation: Avoid sensitive content unless you trust the provider's data handling.

Risk: Voice cloning can reproduce a speaker's voice without consent.

Mitigation: Clone voices only with clear authorization from the speaker.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-voice-tts-studio)
- [a7w API platform](https://api.a7w.cn/)
- [Getting started](references/getting-started.md)
- [Voice synthesis API](references/api-tts.md)
- [Voice cloning API](references/api-clone_voice.md)
- [Speech transcription API](references/api-stt.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API calls may return audio URLs, transcripts, voice model IDs, or asynchronous task IDs.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata; bundled frontmatter lists 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
