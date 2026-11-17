## Description:

Complete step-by-step installation guide for OpenClaw on Windows 10/11 with WSL2, includes common pitfalls and solutions from real installation experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aslancootl](https://clawhub.ai/user/aslancootl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to install OpenClaw on Windows 10/11 through WSL2, including system-drive and custom-drive installation paths. It also helps users troubleshoot common WSL, networking, firewall, and OpenClaw startup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide runs a remote installer script in WSL.

Mitigation: Review the installer contents and verify the source before executing it.

Risk: The guide includes passwordless sudo and routine root-use options.

Mitigation: Use a normal WSL user where possible and avoid passwordless sudo unless the local threat model permits it.

Risk: The guide creates an inbound Windows firewall rule for the OpenClaw service port.

Mitigation: Limit the firewall rule to the required network scope and remove or tighten it when it is no longer needed.

Risk: Some troubleshooting steps may temporarily reduce Windows security protections.

Mitigation: Re-enable security protections immediately after troubleshooting and document any lasting configuration changes.

## Reference(s):

- [Microsoft WSL Releases](https://github.com/microsoft/WSL/releases/latest)
- [Microsoft WSL Manual Install Documentation](https://learn.microsoft.com/zh-cn/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package.)
- [OpenClaw Installer Script](https://molt.bot/install.sh)
- [OpenClaw Browser Relay Chrome Extension](https://chromewebstore.google.com/detail/openclaw-browser-relay/nglingapjinhecnfejdcpihlpneeadjp)
- [Feishu Developer Portal](https://open.feishu.cn/?lang=zh-CN)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline PowerShell, Bash, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese installation guidance]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
