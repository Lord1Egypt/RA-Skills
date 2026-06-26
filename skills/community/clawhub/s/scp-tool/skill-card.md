## Description: <br>
Securely copy files between local and remote hosts over SSH for file transfers, remote backups, and deployment tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare SCP-based file transfer commands between local and remote systems over SSH. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SCP transfers can overwrite files or copy data to the wrong host or directory. <br>
Mitigation: Verify source and destination paths before running transfer commands. <br>
Risk: Transfers may use existing SSH keys, SSH agent state, or SSH configuration. <br>
Mitigation: Confirm the SSH identity, host, and trust boundary before installing or using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/scp-tool) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted system scp binary and valid SSH access for the chosen source and destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
