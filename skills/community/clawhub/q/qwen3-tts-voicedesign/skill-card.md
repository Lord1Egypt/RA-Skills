## Description: <br>
Qwen3-TTS VoiceDesign helps agents generate text-to-speech audio with natural language voice descriptions, seed-fixed timbre, an OpenAI-compatible API server, setup scripts, and batch seed exploration tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to add local Qwen3-TTS speech generation, design voices through natural language prompts, compare timbre seeds, and expose speech generation through a local OpenAI-compatible API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included TTS server is network-facing by default. <br>
Mitigation: Bind TTS_HOST to 127.0.0.1 unless the service is intentionally exposed, and use firewall and authentication controls before allowing remote access. <br>
Risk: The setup flow loads .env as shell input. <br>
Mitigation: Treat .env as trusted executable configuration, restrict who can edit it, and replace shell sourcing with a safer parser before using untrusted configuration. <br>
Risk: The artifact includes highest-privilege scheduled-task guidance for Windows auto-restart. <br>
Mitigation: Use a least-privilege service account or a supervised process manager instead of the highest-privilege scheduled-task example. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoyaner0201/qwen3-tts-voicedesign) <br>


## Skill Output: <br>
**Output Type(s):** [audio, shell commands, configuration, guidance] <br>
**Output Format:** [MP3 or WAV audio files, API responses, and Markdown guidance with bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Voice output depends on the text, voice description, seed, server settings, and selected audio format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
