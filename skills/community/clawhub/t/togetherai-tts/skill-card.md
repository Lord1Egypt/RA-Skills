## Description:

Convert text to speech using the TogetherAI API with the MiniMax speech-2.6-turbo model and save the generated audio as an MP3 file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcus20232023](https://clawhub.ai/user/marcus20232023)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to turn supplied text into speech through TogetherAI and write the generated audio to a chosen MP3 output file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input text is sent to TogetherAI for speech generation.

Mitigation: Use only non-sensitive text and review external API handling requirements before use.

Risk: API-key handling and error logging could expose sensitive credentials.

Mitigation: Use a narrowly scoped TogetherAI key with spending limits and sanitize error logging before deployment.

Risk: Caller-supplied output paths may overwrite files or write in unintended locations.

Mitigation: Run the skill in a dedicated non-privileged folder, restrict output paths, and prevent accidental overwrites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcus20232023/skills/togetherai-tts)
- [TogetherAI speech API endpoint](https://api.together.ai/v1/audio/speech)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Text]

**Output Format:** [MP3 audio file with terminal status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TogetherAI API key and writes to the output path supplied by the caller.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
