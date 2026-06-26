## Description: <br>
Installs and manages an OpenClaw Weixin connection through admin chat commands, including QR refresh, status checks, and cancellation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donotwannatry](https://clawhub.ai/user/donotwannatry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw administrators use this skill in private admin chats to install and enable the Tencent WeChat plugin, generate or refresh login QR codes, check pairing state, and cancel an active pairing task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR code exposure could allow the wrong party to link a WeChat account. <br>
Mitigation: Use only in a private administrator chat and do not expose QR outputs in groups. <br>
Risk: The workflow installs and enables a WeChat plugin and can briefly interrupt the OpenClaw gateway after connection. <br>
Mitigation: Install only if you administer the OpenClaw instance, trust the Tencent WeChat plugin, and can tolerate a short gateway interruption. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/donotwannatry/weixin-plugin-installer) <br>
- [Installation Guide](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON status handling and optional MEDIA file references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce QR PNG, text, and JSON artifacts under the skill .out directory and may schedule a delayed OpenClaw gateway restart after confirmed login.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
