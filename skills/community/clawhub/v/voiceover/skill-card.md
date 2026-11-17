## Description:

Generate spoken voiceover and narration from a script for one speaker, with control over emotion, pacing, and voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to guide an agent in turning scripts into single-speaker spoken narration for videos, ads, audiobooks, IVR greetings, explainers, and other voiceover workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided scripts may contain copyrighted, private, or sensitive material that is inappropriate for third-party text-to-speech processing.

Mitigation: Review scripts before synthesis and only send material that the user is authorized to process under the relevant account and provider terms.

Risk: Raw numbers, dates, prices, abbreviations, or model-specific tags can be spoken incorrectly if normalization and model schema settings are not checked.

Mitigation: Confirm the live model schema, enable the appropriate normalization setting, and pre-expand ambiguous values before generating audio.

## Reference(s):

- [Voiceover worked recipes](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model-selection guidance, voice and delivery settings, text-normalization guidance, and asynchronous audio result handling.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
