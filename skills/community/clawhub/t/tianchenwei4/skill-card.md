## Description: <br>
Integracja KeePassXC z Cursorem do bezpiecznego zarządzania sekretami (hasła, tokeny API, klucze SSH) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theanswerss](https://clawhub.ai/user/theanswerss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and operate KeePassXC-backed secret management for Cursor across Windows and WSL, including retrieving, adding, updating, and organizing passwords, API tokens, and SSH keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to access sensitive KeePassXC vault secrets. <br>
Mitigation: Use a separate minimal vault and require explicit approval before any secret is read, added, edited, or deleted. <br>
Risk: The security summary identifies an unsafe and inconsistently described master-password fallback. <br>
Mitigation: Review the referenced local helper scripts before use and avoid storing the vault master password inside the same vault. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/theanswerss/tianchenwei4) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational instructions for KeePassXC, keyring setup, SSH Agent use, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
