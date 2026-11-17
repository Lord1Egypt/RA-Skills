## Description:

Generate short sound effects via ElevenLabs SFX (text-to-sound). Use when you need SFX clips like applause, canned laughter, whooshes, ambience, or short stingers, and optionally convert to WhatsApp-friendly .ogg/opus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javicasper](https://clawhub.ai/user/javicasper)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate short sound-effect clips from text prompts through the ElevenLabs SFX API and optionally prepare the resulting audio for WhatsApp playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sound-effect prompts are sent to ElevenLabs under the user's API key.

Mitigation: Avoid including secrets or sensitive personal details in prompts and use the skill only when third-party API processing is acceptable.

Risk: The ElevenLabs API key is required for requests.

Mitigation: Store the API key in the supported environment variables or configuration and avoid exposing it in prompts, logs, or shared shell history.

Risk: Generated output can overwrite an existing file at the chosen output path.

Mitigation: Choose output paths deliberately, prefer temporary or unique filenames, and review paths before running the command.

## Reference(s):

- [ElevenLabs sound generation endpoint](https://api.elevenlabs.io/v1/sound-generation)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MP3 audio by default and can guide conversion to OGG/Opus for WhatsApp playback.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
