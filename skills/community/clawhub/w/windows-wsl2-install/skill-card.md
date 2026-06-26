## Description: <br>
Complete step-by-step installation guide for OpenClaw on Windows 10/11 with WSL2, includes common pitfalls and solutions from real installation experience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aslancootl](https://clawhub.ai/user/aslancootl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Windows users use this skill to guide OpenClaw installation on Windows 10/11 via WSL2, including system-drive and custom-drive setup plus troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide includes broad privilege changes, including administrator commands and optional passwordless sudo. <br>
Mitigation: Review commands before execution, prefer a normal WSL user, and avoid blanket passwordless sudo unless the environment is isolated and temporary. <br>
Risk: The guide opens TCP port 18789 for OpenClaw access. <br>
Mitigation: Create firewall access only when needed and restrict exposure to trusted networks or local access. <br>
Risk: The guide installs OpenClaw by running a remote shell script. <br>
Mitigation: Inspect or verify the remote install script before running it and use trusted network paths. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aslancootl/windows-wsl2-install) <br>
- [Microsoft WSL releases](https://github.com/microsoft/WSL/releases/latest) <br>
- [Microsoft WSL manual install kernel update](https://learn.microsoft.com/zh-cn/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package) <br>
- [OpenClaw install script](https://molt.bot/install.sh) <br>
- [OpenClaw browser relay extension](https://chromewebstore.google.com/detail/openclaw-browser-relay/nglingapjinhecnfejdcpihlpneeadjp) <br>
- [Feishu developer portal](https://open.feishu.cn/?lang=zh-CN) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with PowerShell, Bash, and INI code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese installation guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
