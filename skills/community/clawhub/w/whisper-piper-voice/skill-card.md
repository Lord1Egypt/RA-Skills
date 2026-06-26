## Description: <br>
Whisper Piper Voice helps agents set up a local HTTP voice pipeline that transcribes audio with Whisper and generates speech with Piper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielgrobelny](https://clawhub.ai/user/danielgrobelny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure an offline speech-to-text and text-to-speech service for local voice assistants and integrations. It provides setup guidance, model choices, API examples, and a Python server for transcription and OGG speech output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The voice server is unauthenticated and listens on all network interfaces by default. <br>
Mitigation: Bind it to localhost or firewall port 9998 unless LAN access is required, and add authentication before exposing it to other machines. <br>
Risk: The setup guide documents a persistent systemd service. <br>
Mitigation: Enable the service only after reviewing how to stop or disable it in the target environment. <br>
Risk: The setup downloads Piper binaries and voice models before execution. <br>
Mitigation: Verify downloaded Piper binaries and models before running them. <br>


## Reference(s): <br>
- [Voice Pipeline Setup Guide](references/setup-guide.md) <br>
- [Piper voice samples](https://rhasspy.github.io/piper-samples/) <br>
- [Piper Linux release archive](https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz) <br>
- [Thorsten Emotional Piper voice model](https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands, API examples, configuration snippets, and Python code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for a local HTTP service with /transcribe and /speak endpoints; no API credentials are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
