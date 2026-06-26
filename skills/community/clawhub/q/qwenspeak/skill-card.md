## Description: <br>
Text-to-speech generation via Qwen3-TTS over SSH, with preset voices, voice cloning, and voice design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyb0t](https://clawhub.ai/user/psyb0t) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to submit YAML-driven Qwen3-TTS jobs over SSH, monitor progress, manage files, and download generated speech audio. It supports preset voices, voice design, and voice cloning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup path uses an unpinned installer with sudo privileges. <br>
Mitigation: Download and inspect a pinned installer version before running it, and verify checksums when available. <br>
Risk: The service relies on persistent SSH access to the configured qwenspeak host. <br>
Mitigation: Use a dedicated SSH key and confirm QWENSPEAK_HOST and QWENSPEAK_PORT point only to a trusted service. <br>
Risk: Voice cloning can be misused with unauthorized voice samples. <br>
Mitigation: Use only voice samples that the operator is authorized to clone. <br>


## Reference(s): <br>
- [ClawHub qwenspeak release page](https://clawhub.ai/psyb0t/qwenspeak) <br>
- [Publisher profile](https://clawhub.ai/user/psyb0t) <br>
- [qwenspeak homepage](https://github.com/psyb0t/docker-qwenspeak) <br>
- [qwenspeak setup guide](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML examples, shell commands, JSON job status examples, and file-operation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for interacting with a running qwenspeak service over SSH; generated audio files are retrieved through the service.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
