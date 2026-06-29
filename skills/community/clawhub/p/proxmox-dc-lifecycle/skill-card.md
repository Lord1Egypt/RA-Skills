## Description: <br>
Infrastructure automation and an IaC-style runbook for rebuilding a Windows Active Directory domain controller hosted as a Proxmox VE VM by guiding demotion, metadata cleanup, hands-off Windows Server reinstall, rejoin, and replica promotion with replication and FSMO verification gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddygk](https://clawhub.ai/user/eddygk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Infrastructure engineers and Active Directory administrators use this skill to plan and execute lifecycle recovery for a non-last Windows Active Directory domain controller running on Proxmox VE. It helps coordinate demotion, AD DS metadata cleanup, Windows Server reinstall, domain rejoin, replica promotion, and post-change verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill addresses high-privilege Proxmox and Active Directory recovery work where demotion, metadata deletion, promotion, or disk wipe steps can damage a live directory if applied to the wrong target or at the wrong time. <br>
Mitigation: Require human confirmation before destructive actions, rebuild only one additional non-FSMO domain controller at a time, snapshot before destructive phases, and pass each replication, FSMO, and nTDSDSA verification gate before proceeding. <br>
Risk: Administrative credentials and recovery passwords can be exposed through command lines, logs, transcripts, task files, or temporary carriers. <br>
Mitigation: Use short-lived or vault-sourced credentials, pass secrets through QGA stdin, disable logging around secret entry, delete temporary credential carriers immediately, show fingerprints instead of secret values, and rotate any exposed credential. <br>
Risk: Stale environment details or an incorrect VMID, ISO, DNS, IP, or domain-controller role assumption can send automation to the wrong system. <br>
Mitigation: Confirm Proxmox and AD state from live commands before each phase, verify the target is not the last domain controller and holds no FSMO roles, and explicitly confirm the target VM before any disk wipe. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eddygk/skills/proxmox-dc-lifecycle) <br>
- [Project homepage](https://github.com/eddygk/proxmox-dc-lifecycle) <br>
- [Credential handling](references/credential-handling.md) <br>
- [Demotion](references/demotion.md) <br>
- [Metadata cleanup](references/metadata-cleanup.md) <br>
- [OS reinstall](references/os-reinstall.md) <br>
- [Promotion](references/promotion.md) <br>
- [QGA execution](references/qga-execution.md) <br>
- [Verification](references/verification.md) <br>
- [Gotchas](references/gotchas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, PowerShell, JSON configuration, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Linux Proxmox host with bash, qm, base64, QEMU guest agent access, and operator-supplied environment values and credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
