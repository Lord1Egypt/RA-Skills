## Description: <br>
Voice Bridge Light provides a lightweight local HTTP service for OpenAI-compatible speech-to-text and text-to-speech using Whisper, Piper, or Edge TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangbb-coder](https://clawhub.ai/user/fangbb-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install, configure, and run a local voice bridge that exposes OpenAI-compatible audio endpoints for speech synthesis and transcription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service exposes unauthenticated HTTP endpoints and defaults to listening on 0.0.0.0. <br>
Mitigation: Bind the service to 127.0.0.1 or firewall it, and add authentication or trusted-origin restrictions before exposing it beyond a local host. <br>
Risk: Edge TTS may send text to Microsoft online services. <br>
Mitigation: Use Piper for sensitive text or confirm that sending text to the online TTS provider is acceptable for the deployment. <br>
Risk: The bundled service-management example recommends running the persistent service as root. <br>
Mitigation: Run any systemd service as a dedicated unprivileged user with only the filesystem and network access it needs. <br>


## Reference(s): <br>
- [Voice Bridge Light on ClawHub](https://clawhub.ai/fangbb-coder/voice-bridge-light) <br>
- [fangbb-coder publisher profile](https://clawhub.ai/user/fangbb-coder) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration, and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local service configuration, curl examples, and installation commands for a Python voice API service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release; artifact skill.yaml lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
