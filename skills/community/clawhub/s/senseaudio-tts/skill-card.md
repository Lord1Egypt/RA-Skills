## Description: <br>
Build and debug SenseAudio text-to-speech integrations on `/v1/t2a_v2` and `/ws/v1/t2a_v2`, including sync HTTP, SSE stream, WebSocket event sequencing, hex audio decoding, and voice/audio parameter tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build or troubleshoot SenseAudio text-to-speech integrations, including HTTP, SSE, and WebSocket synthesis flows. It helps with request construction, response parsing, audio hex decoding, voice and audio parameters, and production hardening guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SenseAudio API key and sends synthesis text to the SenseAudio service. <br>
Mitigation: Use a dedicated or scoped API key where available, avoid exposing the key in prompts or logs, and review SenseAudio privacy and retention terms before processing sensitive text. <br>
Risk: Generated integration guidance could mishandle streaming events, empty chunks, or transient network failures. <br>
Mitigation: Review proposed code before deployment, validate request parameters, handle terminal and failure events explicitly, and use bounded retry or backoff for transient errors. <br>


## Reference(s): <br>
- [TTS Reference](references/tts.md) <br>
- [SenseAudio Homepage](https://senseaudio.cn) <br>
- [SenseAudio API Key](https://senseaudio.cn/platform/api-key) <br>
- [ClawHub Skill Page](https://clawhub.ai/scikkk/senseaudio-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, streaming event sequences, audio decoding steps, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
