## Description: <br>
WebChat Voice Full Stack installs and verifies a local OpenClaw WebChat voice-input stack by orchestrating local speech-to-text, HTTPS/WSS proxy, and voice UI sub-skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neldar](https://clawhub.ai/user/neldar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add local microphone input and speech-to-text transcription to OpenClaw WebChat with a coordinated backend, proxy, and UI deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment creates persistent user-level services for transcription and HTTPS proxy behavior. <br>
Mitigation: Install only when persistent local voice transcription is desired, review the downstream sub-skills first, and keep the documented reverse-order uninstall steps available. <br>
Risk: Sub-skill scripts may change after installation or review. <br>
Mitigation: Run rehash.sh only after reviewing the installed sub-skill scripts, then use VERIFY_ONLY=true bash scripts/deploy.sh to verify checksums before deployment. <br>
Risk: Incorrect host, port, or allowed-origin settings can expose or break the local WebChat voice path. <br>
Mitigation: Verify VOICE_HOST, VOICE_HTTPS_PORT, TRANSCRIBE_PORT, and gateway allowed-origin settings before running deployment. <br>
Risk: The first local speech-to-text run requires a large model download. <br>
Mitigation: Plan for initial network access and local storage before deploying the faster-whisper backend. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/neldar/webchat-voice-full-stack) <br>
- [Publisher Profile](https://clawhub.ai/user/neldar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and environment variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment, verification, checksum, and uninstall guidance for local OpenClaw voice services.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
