## Description: <br>
Real-time voice assistant for OpenClaw that streams microphone audio through configurable STT providers, sends transcripts to an OpenClaw agent, and speaks responses through configurable TTS providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charantejmandali18](https://clawhub.ai/user/charantejmandali18) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to add a browser-based voice interface to an OpenClaw agent, with configurable speech-to-text and text-to-speech providers for real-time conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill streams live microphone audio and assistant content through external STT and TTS providers. <br>
Mitigation: Use only approved provider accounts and avoid speaking sensitive information unless those providers are approved for that data. <br>
Risk: The local voice server depends on a trusted OpenClaw gateway and network environment. <br>
Mitigation: Run the server only on trusted networks and point it only at a trusted OpenClaw gateway. <br>
Risk: Server evidence reports missing privacy notice or consent flow, origin/auth controls, transcript rendering fixes, and .env.example metadata. <br>
Mitigation: Address those issues before broad deployment and review the release before installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charantejmandali18/voice-assistant) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operating guidance for a local browser voice assistant server.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, artifact _meta.json, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
