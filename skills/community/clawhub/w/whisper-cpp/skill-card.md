## Description: <br>
Install and use whisper.cpp for local, offline speech-to-text in OpenClaw, including ggml model download support and OpenClaw audio configuration for inbound voice notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TrueNight](https://clawhub.ai/user/TrueNight) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install local whisper.cpp speech-to-text, download selected ggml Whisper models, and configure OpenClaw to transcribe inbound voice notes without a paid speech provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow downloads and builds whisper.cpp and downloads speech models from external sources. <br>
Mitigation: Review the scripts before running them, install from a trusted network, and consider pinning a known whisper.cpp release or verifying model sources before use. <br>
Risk: The skill changes OpenClaw audio settings and restarts the gateway. <br>
Mitigation: Confirm the wrapper path and intended OpenClaw audio configuration before applying the patch, then test with a known audio sample. <br>
Risk: Local speech-to-text quality and latency depend on the selected ggml model, language, host CPU, and audio format. <br>
Mitigation: Choose an appropriate model size, set the language explicitly when needed, and validate transcription behavior with representative voice notes. <br>


## Reference(s): <br>
- [Local Whisper ClawHub release](https://clawhub.ai/TrueNight/whisper-cpp) <br>
- [whisper.cpp upstream project](https://github.com/ggerganov/whisper.cpp) <br>
- [whisper.cpp ggml model downloads](https://huggingface.co/ggerganov/whisper.cpp/resolve/main) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell script artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup steps, wrapper behavior, model selection guidance, and OpenClaw audio configuration commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
