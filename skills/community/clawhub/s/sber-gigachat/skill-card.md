## Description: <br>
Integrate GigaChat (Sber AI) with OpenClaw via gpt2giga proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smvlx](https://clawhub.ai/user/smvlx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run a local gpt2giga proxy that exposes Sber GigaChat models through an OpenAI-compatible endpoint and updates OpenClaw configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TLS verification may be disabled when the Sber CA is not installed. <br>
Mitigation: Install or configure the Sber CA before startup so TLS verification remains enabled. <br>
Risk: Startup can terminate processes using port 8443. <br>
Mitigation: Check port 8443 ownership before running the startup script. <br>
Risk: The configuration patch can overwrite OpenClaw settings. <br>
Mitigation: Review the generated backup and configuration changes before using the patched OpenClaw config. <br>
Risk: GigaChat credentials are loaded from a local environment file. <br>
Mitigation: Protect the credential environment file with restrictive file permissions and avoid sharing logs or config backups that may expose secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smvlx/sber-gigachat) <br>
- [OpenClaw Russian skills homepage](https://github.com/smvlx/openclaw-ru-skills) <br>
- [GigaChat documentation](https://developers.sber.ru/docs/ru/gigachat/overview) <br>
- [gpt2giga package](https://pypi.org/project/gpt2giga/) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local proxy startup, process management, credential environment setup, and OpenClaw provider configuration.] <br>

## Skill Version(s): <br>
1.1.2 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
