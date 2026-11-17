## Description:

Text-to-speech with Qwen3-TTS VoiceDesign. Design custom voices via natural language descriptions and seed-based timbre fixation, with an OpenAI-compatible API server, setup script, and batch seed exploration tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to generate speech, design custom voices with natural-language voice prompts, fix timbre through seeds, and connect a local TTS server to OpenClaw or OpenAI-compatible clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The TTS server is unauthenticated and may expose costly model inference if bound to a reachable network interface.

Mitigation: Bind the service to 127.0.0.1 unless intentionally exposing it, and add authentication plus request limits for remote use.

Risk: Startup and configuration patterns need review before installation, including elevated scheduled-task examples and environment file sourcing.

Mitigation: Do not run setup or startup as administrator, avoid elevated scheduled tasks, and harden environment loading before using the scripts with untrusted inputs.

Risk: Shell-built JSON can mishandle untrusted text passed into batch seed generation.

Mitigation: Replace shell-built JSON with structured JSON generation before accepting untrusted text inputs.

## Reference(s):

- [Qwen3-TTS VoiceDesign on ClawHub](https://clawhub.ai/xiaoyaner0201/skills/qwen3-tts-voicedesign)
- [Publisher profile: xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, API examples, and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for generating mp3 or wav speech through a local TTS API and helper scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
