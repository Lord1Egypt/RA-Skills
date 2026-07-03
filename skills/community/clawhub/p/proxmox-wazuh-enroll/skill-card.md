## Description: <br>
Install and enroll the Wazuh agent inside Windows VMs hosted on Proxmox VE using QEMU guest agent execution without requiring WinRM, SSH, RDP, GPO, or Active Directory credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddygk](https://clawhub.ai/user/eddygk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Infrastructure and security operators use this skill to enroll specific Windows Proxmox guests into a Wazuh manager through QEMU guest agent execution. It helps plan the manager-side group setup, in-guest agent installation, connection restart, and manager-side verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow performs privileged, state-changing software installation inside Windows VMs through QEMU guest agent execution. <br>
Mitigation: Use it only for intentional Wazuh deployment on confirmed VM IDs during an approved change window, and review commands before execution. <br>
Risk: Registration passwords, Proxmox API tokens, and QGA execution can expose secrets or grant administrative access if mishandled. <br>
Mitigation: Do not paste registration passwords into chat or command examples; prefer stdin-based secret passing or the documented authd.pass alternative with prompt deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eddygk/skills/proxmox-wazuh-enroll) <br>
- [Project homepage](https://github.com/eddygk/proxmox-wazuh-enroll) <br>
- [QGA execution reference](references/qga-exec.md) <br>
- [Wazuh agent enrollment reference](references/wazuh-agent-enroll.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash, Windows command, JSON, and PowerShell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [State-changing workflow that requires confirmed VM IDs, manager address, agent group, and registration-secret handling before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
