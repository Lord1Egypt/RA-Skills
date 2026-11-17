## Description:

Converts supplied text into WAV podcast audio with Tencent Cloud TTS, using automatic chunking and parallel processing for longer inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[islinxu](https://clawhub.ai/user/islinxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to convert prepared text into single-voice podcast audio through Tencent Cloud TTS. It supports short text directly and chunks longer text for multi-part generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input text is sent to Tencent Cloud TTS for audio generation.

Mitigation: Avoid sensitive source text unless the deployment has approved Tencent Cloud processing and credential handling.

Risk: Optional COS upload can make generated audio public.

Mitigation: Keep COS upload disabled unless needed, and use private objects or signed URLs for generated audio.

Risk: The implementation may install the COS SDK at runtime if it is missing.

Mitigation: Install and review dependencies ahead of deployment instead of relying on runtime package installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/islinxu/skills/tencent-tts-podcast)

## Skill Output:

**Output Type(s):** [text, audio, code, configuration, guidance]

**Output Format:** [JSON response with status fields and an AudioUrl path or URL; AgentScope wrapper returns text plus a WAV audio block.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [WAV output only; optional Tencent COS upload may return a cloud object URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
