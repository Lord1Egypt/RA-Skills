## Description: <br>
Xeon TTS installs and operates local OpenVINO Qwen3-TTS services for OpenClaw QQBOT voice cloning and style-conditioned speech synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aurora2035](https://clawhub.ai/user/aurora2035) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add local text-to-speech, voice cloning, and custom tone synthesis to QQBOT workflows while keeping TTS separate from STT/ASR chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation creates persistent local user services and modifies OpenClaw QQBOT TTS configuration. <br>
Mitigation: Review install scripts before use, run on a machine where persistent user services are acceptable, and disable the xeontts systemd services when the workflow is no longer needed. <br>
Risk: The local workflow API can expose TTS and voice-cloning actions if bound too broadly. <br>
Mitigation: Keep the workflow gateway bound to localhost and avoid exposing ports 5002 or 9002 to untrusted networks. <br>
Risk: Voice cloning can process and retain user voice samples locally. <br>
Mitigation: Require consent for cloned voices, enforce the 3 to 5 second reference-audio check, and communicate the default 7 day retention window for reference and generated files. <br>
Risk: The installer downloads models and packages during setup. <br>
Mitigation: Install only in environments where those downloads are approved and review configured model and package sources before enabling the services. <br>


## Reference(s): <br>
- [ClawHub xeontts skill page](https://clawhub.ai/aurora2035/xeontts) <br>
- [Qwen3-TTS Base OpenVINO INT8 model](https://huggingface.co/aurora2035/Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8) <br>
- [Qwen3-TTS CustomVoice OpenVINO INT8 model](https://huggingface.co/aurora2035/Qwen3-TTS-12Hz-0.6B-CustomVoice-OpenVINO-INT8) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown and text guidance with shell commands, JSON configuration, local API calls, and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Voice cloning requires a 3 to 5 second reference audio sample; generated reference and output files default to 7 day local retention.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
