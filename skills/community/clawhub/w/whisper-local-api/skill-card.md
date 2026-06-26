## Description: <br>
Whisper Local Api helps agents install and run a local OpenAI-compatible Whisper transcription endpoint for speech-to-text workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hantok](https://clawhub.ai/user/Hantok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to install, start, health-check, and smoke-test a local Whisper ASR service for OpenClaw-compatible voice transcription workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs unpinned external backend code and dependencies. <br>
Mitigation: Review the backend repository and dependencies before installation, and prefer pinning WHISPER_REPO_URL to a trusted commit or controlled fork. <br>
Risk: Offline and privacy claims may be overstated if the service or configured URLs are exposed beyond the local host. <br>
Mitigation: Keep the service local unless remote access is intentional, and add firewalling, HTTPS, and authentication before exposing it. <br>
Risk: Environment overrides can redirect repository or API traffic to untrusted hosts. <br>
Mitigation: Set WHISPER_REPO_URL and WHISPER_API_URL only to hosts that have been reviewed and trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Hantok/whisper-local-api) <br>
- [Configured backend repository](https://github.com/Hantok/local-whisper-backend.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and local HTTP endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scripts for bootstrap, service startup, health checks, and audio-file smoke testing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
