## Description:

Set up, test, benchmark, and use ElevenLabs text-to-speech as an independent TTS skill, including HTTP streaming, WebSocket streaming guidance, voice listing, model/output-format selection, latency tuning, and safe ELEVENLABS_API_KEY handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure, test, benchmark, and troubleshoot ElevenLabs text-to-speech workflows, including voice discovery, HTTP streaming synthesis, model and output-format selection, and latency tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses ElevenLabs cloud APIs and requires an ElevenLabs API key.

Mitigation: Provide the key through ELEVENLABS_API_KEY, do not put secrets in prompts or files, and only synthesize text suitable to send to ElevenLabs.

Risk: Generated audio is written to the path selected by the user.

Mitigation: Choose an explicit output path and inspect the resulting file before sharing or relying on it.

## Reference(s):

- [ElevenLabs TTS API Reference](references/elevenlabs-api.md)
- [ClawHub Skill Release](https://clawhub.ai/jerryxn/skills/xiaog-elevenlabs-tts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python script usage, and JSON command output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts can list voices and write generated audio bytes to an explicit output path when ELEVENLABS_API_KEY is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
