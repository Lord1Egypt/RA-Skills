## Description: <br>
SSH operations skill for generating SSH keys, deploying public keys for passwordless login, testing connections, inspecting remote hosts, and running remote administration commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aowind](https://clawhub.ai/user/aowind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage SSH access and perform remote server maintenance tasks such as key setup, connection checks, host inspection, file transfer, deployment, and command execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad server-administration actions, including remote command execution. <br>
Mitigation: Install only for intended server administration, restrict use to specific hosts, avoid root accounts where possible, and review every remote command before it runs. <br>
Risk: Password-based key deployment can expose credentials if SSHPASS is persisted or reused carelessly. <br>
Mitigation: Set SSHPASS only for the deployment command, do not store it in files or chat history, unset it after use, and rotate credentials if exposure is suspected. <br>
Risk: Deploying keys to the wrong host can grant access to unintended systems. <br>
Mitigation: Verify host fingerprints before deployment and confirm the target user and host before copying public keys. <br>
Risk: The setup flow can install sshpass through the system package manager. <br>
Mitigation: Install dependencies yourself or explicitly approve package-manager changes before running deployment steps. <br>
Risk: SSH keys deployed for maintenance can remain valid after the task is complete. <br>
Mitigation: Remove or rotate deployed SSH keys when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aowind/sjht-ssh-ops) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local SSH tooling and package managers, and may affect remote servers when commands are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
