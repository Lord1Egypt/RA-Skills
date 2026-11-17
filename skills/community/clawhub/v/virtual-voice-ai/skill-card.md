## Description:

Wires a real microphone through an AI brain (STT to LLM to TTS) and routes the output to a virtual audio cable so meeting apps hear the processed voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suhas12345685-pro](https://clawhub.ai/user/suhas12345685-pro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build and test a Node.js real-time voice pipeline that captures microphone audio, sends it through STT, LLM, and TTS services, and routes generated audio to a virtual microphone for meeting apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live microphone audio and transcripts may be sent to external STT, LLM, and TTS providers.

Mitigation: Use only where all participants and the organization permit AI voice processing, and choose providers whose data handling terms match the intended use.

Risk: Generated audio is routed into meeting applications as a virtual microphone.

Mitigation: Keep the real microphone and virtual cable routing explicit, test in a dummy call first, and wire the provided stop function to an immediately accessible control.

Risk: API keys are required for external providers and could be exposed through local files or debug output.

Mitigation: Keep .env local and untracked, avoid PIPELINE_DEBUG during real conversations, and prefer provider integrations that keep API keys out of URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suhas12345685-pro/skills/virtual-voice-ai)
- [Pipeline Architecture](artifact/reference/archetecture.md)
- [Environment Variables](artifact/reference/env_schema.md)
- [Step-by-Step Build Guide](artifact/reference/step_by_step.md)
- [Deepgram console](https://console.deepgram.com)
- [VB-Audio Cable](https://vb-audio.com/Cable/)
- [BlackHole 2ch](https://existential.audio/blackhole/)
- [ffmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript code snippets, shell commands, and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup of a Node.js audio pipeline that uses local ffmpeg processes and external STT, LLM, and TTS providers.]

## Skill Version(s):

1.0.0 (source: release evidence and scripts/Package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
