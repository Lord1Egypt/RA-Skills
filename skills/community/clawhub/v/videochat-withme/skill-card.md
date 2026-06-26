## Description: <br>
Real-time AI video chat that routes microphone audio, camera frames, and conversation through an OpenClaw agent using Groq Whisper for speech recognition and edge-tts for spoken responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxu75374](https://clawhub.ai/user/sxu75374) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to start a browser-based video or voice call with an OpenClaw agent that can hear speech, see camera frames, and respond with the agent's configured personality and memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an always-on local video-chat service that handles microphone and camera data. <br>
Mitigation: Prefer manual startup or unload the LaunchAgent when not actively using the skill, and restrict access to trusted networks. <br>
Risk: Voice data is sent to Groq for speech recognition and text is sent to Microsoft edge-tts for speech output. <br>
Mitigation: Use the skill only when cloud speech processing is acceptable for the conversation content. <br>
Risk: Camera frames may leave the device if the OpenClaw gateway is configured to use a cloud LLM provider. <br>
Mitigation: Configure OpenClaw with a local or self-hosted model when camera frames must stay local. <br>
Risk: The skill reads the OpenClaw gateway token and a Groq API key from local configuration or secret files. <br>
Mitigation: Harden API-key storage, limit file permissions, rotate exposed credentials, and review token scope before installation. <br>
Risk: Temporary audio and image files are written under the system temp directory during processing. <br>
Mitigation: Periodically clear the temporary media directory and avoid using the skill for sensitive conversations without additional cleanup controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sxu75374/videochat-withme) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Groq API Keys](https://console.groq.com/keys) <br>
- [Groq Whisper API Endpoint](https://api.groq.com/openai/v1) <br>
- [edge-tts](https://github.com/rany2/edge-tts) <br>
- [mkcert](https://github.com/FiloSottile/mkcert) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown instructions with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and call-control guidance for a local video-chat service.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
