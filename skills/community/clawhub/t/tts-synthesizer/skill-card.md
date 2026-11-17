## Description:

Converts text to speech using Microsoft edge-tts or an OpenAI-compatible TTS API, with support for OGG/Opus output for Feishu voice messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to synthesize spoken audio from text, choose TTS voices, and generate Feishu-ready OGG/Opus files or general MP3 output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TTS input text may be sent to Microsoft edge-tts or to the configured OpenAI-compatible API endpoint.

Mitigation: Avoid sending secrets or private regulated data for synthesis, and install the skill only when the configured provider is acceptable for the intended data.

Risk: API mode sends credentials and requests to the configured TTS endpoint.

Mitigation: Use a trusted HTTPS API URL and prefer environment variables over command-line API keys.

Risk: Dependency changes could affect runtime behavior or provider communication.

Mitigation: Pin dependencies in a virtual environment before use when reproducibility or change control matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moroiser/skills/tts-synthesizer)
- [Publisher profile](https://clawhub.ai/user/moroiser)
- [OpenAI-compatible API base URL example](https://api.openai.com/v1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OGG/Opus audio for Feishu voice messages through tts_simple.py and MP3 audio through tts_edge.py.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
