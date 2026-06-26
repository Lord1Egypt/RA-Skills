## Description: <br>
Provides a local OpenClaw QQBOT text-to-speech workflow for Qwen3-TTS voice cloning and styled speech generation using OpenVINO models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aurora2035](https://clawhub.ai/user/aurora2035) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install and run local QQBOT speech generation workflows, including short reference-audio voice cloning and styled TTS output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated local network services may be reachable on shared or network-accessible machines. <br>
Mitigation: Bind the workflow gateway to localhost or firewall port 9002, and add authentication before exposing it beyond the local host. <br>
Risk: The direct clone-speak path API can use filesystem paths for reference audio. <br>
Mitigation: Avoid that endpoint until it is restricted to server-managed reference audio IDs. <br>
Risk: Installation creates persistent background services and stores voice reference files and generated audio locally. <br>
Mitigation: Review service installation and retention settings before deployment, and confirm local storage practices match the target environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aurora2035/xeonasr) <br>
- [Qwen3-TTS Base OpenVINO INT8 model](https://huggingface.co/aurora2035/Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8) <br>
- [Qwen3-TTS CustomVoice OpenVINO INT8 model](https://huggingface.co/aurora2035/Qwen3-TTS-12Hz-0.6B-CustomVoice-OpenVINO-INT8) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration; runtime endpoints produce local audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference audio and generated outputs are stored locally and default to a 7-day retention period.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
