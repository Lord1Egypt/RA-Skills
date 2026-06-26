## Description: <br>
Security suite for OpenClaw agents that provides encrypted secret storage, real-time activity monitoring, policy enforcement, and an optional x402 payment wallet through a macOS desktop app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DLhugly](https://clawhub.ai/user/DLhugly) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and operate Vault-0 for hardening local agent secrets, monitoring agent activity, applying security policies, and managing optional x402 wallet workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an unnotarized desktop app from GitHub releases that will handle API keys, agent activity, and optional wallet material. <br>
Mitigation: Proceed only if the publisher and release process are trusted, verify the DMG hash against the release page, and consider building from source. <br>
Risk: Hardening and wallet features interact with sensitive local OpenClaw secrets and vault data. <br>
Mitigation: Back up OpenClaw .env and vault data before hardening or uninstalling, and avoid exposing full secret files during verification. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DLhugly/vault0) <br>
- [Publisher Profile](https://clawhub.ai/user/DLhugly) <br>
- [Vault-0 v1.5.0 Release](https://github.com/0-Vault/Vault-0/releases/tag/v1.5.0) <br>
- [Vault-0 Project Page](https://github.com/0-Vault/Vault-0) <br>
- [Vault-0 Demo Video](https://youtu.be/FGGWJdeyY9g) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides macOS installation, integrity checking, OpenClaw hardening, local monitoring, and uninstall steps.] <br>

## Skill Version(s): <br>
1.5.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
