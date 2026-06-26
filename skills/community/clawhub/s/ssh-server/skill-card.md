## Description: <br>
SSH remote connection and operation for servers (Linux/Unix cloud servers, etc.) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XingFaLin](https://clawhub.ai/user/XingFaLin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to connect to Linux or Unix servers over SSH, configure saved server entries, inspect system status, view logs, and run common service or Docker operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents an SSH command that disables strict host key checking, which can expose users to server impersonation. <br>
Mitigation: Prefer verified host keys and avoid StrictHostKeyChecking=no for normal connections. <br>
Risk: The skill asks users to store powerful server credentials through helper code that is not included for review in the artifact. <br>
Mitigation: Prefer SSH keys or an SSH agent, and inspect or avoid the helper before entering server passwords. <br>
Risk: The skill includes service, Docker, sudo, and file-changing command patterns that can affect remote systems. <br>
Mitigation: Require explicit user approval and review command impact before running privileged or state-changing operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/XingFaLin/ssh-server) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SSH, systemctl, Docker, log inspection, and local configuration commands that require review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
