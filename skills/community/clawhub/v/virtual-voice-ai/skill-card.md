## Description: <br>
Guides developers through building a Node.js pipeline that captures microphone audio, sends it through STT, LLM, and TTS services, and routes the synthesized voice to a virtual audio cable for meeting apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhas12345685-pro](https://clawhub.ai/user/suhas12345685-pro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and test a real-time voice pipeline that converts live microphone input into AI-generated speech routed into apps such as Google Meet, Zoom, or Teams. It helps with environment setup, audio device discovery, staged script execution, and kill-switch wiring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live microphone capture, third-party AI processing, and synthesized audio injection into meeting software. <br>
Mitigation: Use it only where microphone capture and generated meeting audio are appropriate and disclosed, and review provider retention settings before use. <br>
Risk: The pipeline depends on STT, LLM, and TTS API keys stored in environment configuration. <br>
Mitigation: Keep .env files out of version control and use dedicated, low-privilege API keys for each provider. <br>
Risk: The security review notes a missing core capture script and recommends review before installation. <br>
Mitigation: Verify or replace the capture script before running the full pipeline, stress-test each stage, and test the kill switch before using the skill in a real meeting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/suhas12345685-pro/virtual-voice-ai) <br>
- [README](readme.md) <br>
- [Pipeline Architecture](reference/archetecture.md) <br>
- [Environment Variables](reference/env_schema.md) <br>
- [Step-by-Step Build Guide](reference/step_by_step.md) <br>
- [VB-Audio Cable](https://vb-audio.com/Cable/) <br>
- [BlackHole 2ch](https://existential.audio/blackhole/) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>
- [Deepgram Console](https://console.deepgram.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, environment variables, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires microphone access, ffmpeg, a virtual audio cable, and API keys for STT, LLM, and TTS providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
